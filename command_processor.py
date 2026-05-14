"""
Модуль обработки команд для приложения "Учёт показаний счётчиков".

Поддерживаемые команды:
    ADD <ресурс>; <дата>; <значение>; <качество>
    REM <поле> <оператор> <значение>
    SAVE <путь к файлу>

Поля для REM: resource, date, value, quality
Операторы:    =  !=  <  >  <=  >=
  - для value все операторы (числовое сравнение)
  - для resource, date, quality только = и != (строковое сравнение)
"""

import logging
from typing import List, Callable

from classes import (
    MeterModel, MeterReading, MeterValidationError,
    parse_line, validate_date, validate_radius
)

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Исключение команд
# ──────────────────────────────────────────────

class CommandError(Exception):
    """Ошибка разбора или выполнения команды."""
    pass


# ──────────────────────────────────────────────
# Разбор отдельных команд
# ──────────────────────────────────────────────

def _parse_add(args: str) -> MeterReading:
    """
    Разбирает аргумент команды ADD в формате CSV:
        ресурс; дата; значение; качество
    Возвращает объект MeterReading.
    """
    parts = [p.strip() for p in args.split(';')]

    if len(parts) != 4:
        raise CommandError(
            f'ADD ожидает 4 поля через ";", получено {len(parts)}: {args!r}'
        )

    resource, date_str, value_str, quality = parts

    if not resource:
        raise CommandError('ADD: название ресурса не может быть пустым')
    if not quality:
        raise CommandError('ADD: качество не может быть пустым')

    try:
        value = float(value_str)
    except ValueError:
        raise CommandError(f'ADD: значение должно быть числом, получено: {value_str!r}')

    try:
        date = validate_date(date_str)
        value = validate_radius(value)
    except MeterValidationError as e:
        raise CommandError(f'ADD: {e}')

    return MeterReading(resource=resource, date=date, value=value, quality=quality)


def _parse_rem(args: str) -> tuple:
    """
    Разбирает условие команды REM:
        <поле> <оператор> <значение>
    Возвращает кортеж (поле, оператор, значение).
    """
    operators = ['<=', '>=', '!=', '<', '>', '=']

    for op in operators:
        if op in args:
            left, right = args.split(op, maxsplit=1)
            field = left.strip().lower()
            value = right.strip()

            allowed_fields = {'resource', 'date', 'value', 'quality'}
            if field not in allowed_fields:
                raise CommandError(
                    f'REM: неизвестное поле {field!r}. '
                    f'Допустимые: {", ".join(sorted(allowed_fields))}'
                )
            return field, op, value

    raise CommandError(f'REM: не найден оператор в условии: {args!r}')


def _matches(reading: MeterReading, field: str, op: str, value: str) -> bool:
    """
    Проверяет соответствует ли показание условию field op value.
    Для value — числовое сравнение, для остальных — строковое.
    """
    reading_value = {
        'resource': reading.resource,
        'date': reading.date,
        'value': reading.value,
        'quality': reading.quality,
    }[field]

    if field == 'value':
        try:
            value_num = float(value)
        except ValueError:
            raise CommandError(
                f'REM: для поля value ожидается число, получено: {value!r}'
            )
        ops: dict[str, Callable] = {
            '=':  lambda a, b: a == b,
            '!=': lambda a, b: a != b,
            '<':  lambda a, b: a < b,
            '>':  lambda a, b: a > b,
            '<=': lambda a, b: a <= b,
            '>=': lambda a, b: a >= b,
        }
        return ops[op](reading_value, value_num)

    # Строковые поля — только = и !=
    if op not in ('=', '!='):
        raise CommandError(
            f'REM: оператор {op!r} не поддерживается для поля {field!r}. '
            f'Используйте = или !='
        )
    return reading_value == value if op == '=' else reading_value != value


# ──────────────────────────────────────────────
# Класс CommandProcessor
# ──────────────────────────────────────────────

class CommandProcessor:
    def __init__(self, model: MeterModel):
        self.model = model

    def run_file(self, filename: str) -> None:
        """
        Читает файл команд и выполняет их построчно.
        Некорректные команды пропускаются с записью в лог.
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            logger.error('Файл команд не найден: %s', filename)
            return
        except OSError as e:
            logger.error('Не удалось прочитать файл команд %s: %s', filename, e)
            return

        logger.info('Начало выполнения файла команд: %s', filename)

        for line_num, line in enumerate(lines, start=1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            try:
                self._execute(line)
            except CommandError as e:
                logger.warning(
                    'Строка %d пропущена — %s | Команда: %r', line_num, e, line
                )

        logger.info('Файл команд выполнен: %s', filename)

    def _execute(self, line: str) -> None:
        """Определяет тип команды и выполняет её."""
        parts = line.split(maxsplit=1)
        command = parts[0].upper()
        args = parts[1] if len(parts) > 1 else ''

        if command == 'ADD':
            self._cmd_add(args)
        elif command == 'REM':
            self._cmd_rem(args)
        elif command == 'SAVE':
            self._cmd_save(args)
        else:
            raise CommandError(f'Неизвестная команда: {command!r}')

    def _cmd_add(self, args: str) -> None:
        reading = _parse_add(args)
        self.model.readings.append(reading)
        self.model.save()
        logger.info('ADD: добавлено показание %r', reading)

    def _cmd_rem(self, args: str) -> None:
        field, op, value = _parse_rem(args)
        before = len(self.model.readings)
        self.model.readings = [
            r for r in self.model.readings
            if not _matches(r, field, op, value)
        ]
        removed = before - len(self.model.readings)
        if removed > 0:
            self.model.save()
        logger.info('REM %s %s %s: удалено %d показаний', field, op, value, removed)

    def _cmd_save(self, args: str) -> None:
        path = args.strip()
        if not path:
            raise CommandError('SAVE: не указан путь к файлу')

        # Временно меняем имя файла, сохраняем, возвращаем обратно
        original = self.model.filename
        self.model.filename = path
        try:
            self.model.save()
        finally:
            self.model.filename = original

        logger.info('SAVE: данные сохранены в %s', path)