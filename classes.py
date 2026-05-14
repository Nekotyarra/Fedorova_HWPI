import datetime
import logging
from dataclasses import dataclass, asdict
from typing import List, Optional

logger = logging.getLogger(__name__)


class MeterParseError(Exception):
    """Ошибка парсинга строки."""
    pass


class MeterValidationError(Exception):
    """Ошибка валидации данных."""
    pass


# ──────────────────────────────────────────────
# Валидаторы
# ──────────────────────────────────────────────

def validate_date(date_str: str) -> str:
    """
    Проверяет формат даты: ГГГГ.ММ.ДД или ГГГГ-ММ-ДД.
    Возвращает дату в формате ГГГГ.ММ.ДД.
    """
    for fmt in ('%Y.%m.%d', '%Y-%m-%d'):
        try:
            dt = datetime.datetime.strptime(date_str, fmt)
            return dt.strftime('%Y.%m.%d')
        except ValueError:
            continue
    raise MeterValidationError(
        f'Дата должна быть в формате ГГГГ.ММ.ДД или ГГГГ-ММ-ДД, получено: {date_str}'
    )


def validate_radius(value: float) -> float:
    """Проверяет, что значение показания неотрицательное."""
    if value < 0:
        raise MeterValidationError(f'Значение должно быть >= 0, получено: {value}')
    return value


# ──────────────────────────────────────────────
# Класс показания счётчика
# ──────────────────────────────────────────────

@dataclass
class MeterReading:
    """Показание счётчика."""
    resource: str      # Название ресурса
    date: datetime.date   # Дата в формате ГГГГ.ММ.ДД
    value: float       # Значение показания
    quality: str       # Качество (good, normal, bad и т.д.)

    def to_line(self) -> str:
        """Преобразует объект в строку для сохранения в файл."""
        return f'"{self.resource}" {self.date} {self.value} {self.quality}\n'


# ──────────────────────────────────────────────
# Парсинг строки
# ──────────────────────────────────────────────

def parse_line(line: str) -> MeterReading:
    """
    Разбирает строку вида:
        "Ресурс" 2024.11.20 150.75 good
    или
        Ресурс; 2024.11.20; 150.75; good
    """
    line = line.strip()
    if not line:
        raise MeterParseError('Пустая строка')

    # Пробуем CSV формат (для ADD команды)
    if ';' in line:
        parts = [p.strip() for p in line.split(';')]
        if len(parts) == 4:
            resource, date_str, value_str, quality = parts
        else:
            raise MeterParseError(f'CSV формат: ожидается 4 поля, получено {len(parts)}')
    else:
        # Оригинальный формат с кавычками и пробелами
        import shlex
        parts = shlex.split(line)
        if len(parts) == 4:
            resource, date_str, value_str, quality = parts
        elif len(parts) == 3:
            # Для обратной совместимости (без качества)
            resource, date_str, value_str = parts
            quality = 'normal'
        else:
            raise MeterParseError(f'Ожидается 3 или 4 поля, получено {len(parts)}')

    try:
        value = float(value_str)
    except ValueError:
        raise MeterParseError(f'Значение должно быть числом: {value_str}')

    # Валидация
    date = validate_date(date_str)
    value = validate_radius(value)

    return MeterReading(resource=resource, date=date, value=value, quality=quality)


# ──────────────────────────────────────────────
# Модель для работы с данными
# ──────────────────────────────────────────────

class MeterModel:
    """Модель данных с загрузкой/сохранением из файла."""

    def __init__(self, filename: str):
        self.filename = filename
        self.readings: List[MeterReading] = []
        self._load()

    def _load(self) -> None:
        """Загружает данные из файла."""
        self.readings = []
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        self.readings.append(parse_line(line))
                    except (MeterParseError, MeterValidationError) as e:
                        logger.warning('Строка %d пропущена: %s', line_num, e)
        except FileNotFoundError:
            logger.warning('Файл не найден: %s, будет создан новый', self.filename)
        except OSError as e:
            logger.error('Ошибка чтения файла %s: %s', self.filename, e)

    def save(self) -> None:
        """Сохраняет данные в файл."""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                for reading in self.readings:
                    f.write(reading.to_line())
        except OSError as e:
            logger.error('Ошибка сохранения файла %s: %s', self.filename, e)
            raise

    def get_all(self) -> List[MeterReading]:
        """Возвращает все показания."""
        return self.readings.copy()

    def add_reading(self, resource: str, date: str, value: float, quality: str) -> None:
        """Добавляет новое показание."""
        date = validate_date(date)
        value = validate_radius(value)
        reading = MeterReading(resource, date, value, quality)
        self.readings.append(reading)
        self.save()

    def delete_reading(self, index: int) -> None:
        """Удаляет показание по индексу."""
        if 0 <= index < len(self.readings):
            del self.readings[index]
            self.save()
        else:
            raise IndexError(f'Индекс {index} вне диапазона (0..{len(self.readings)-1})')