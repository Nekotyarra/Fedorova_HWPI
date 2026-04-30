import shlex
import datetime
from classes import MeterReading

def parse_date( date_str: str) -> datetime.date:
    """Пытается распарсить дату в форматах ГГГГ.ММ.ДД или ГГГГ-ММ-ДД."""
    for fmt in ('%Y.%m.%d', '%Y-%m-%d'):
        try:
            return datetime.datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError('Дата должна быть в формате гггг.мм.дд или гггг-мм-дд')

def parse_line_shlex(line: str) -> MeterReading:
    """
    Функция, которая разделяет строку по пробелам, игнорируя пробелы в подстроках
    :param line: строка
    :return: Класс MeterReading (показания счетчиков)
    """
    parts = shlex.split(line.strip())
    if len(parts) != 4:
        raise ValueError(f'Ожидалось 4 части, получено {len(parts)}: {line}')
    resource, date_str, value_str, quality = parts
    try:
        # Преобразование даты
        date = parse_date(date_str)
        value = float(value_str)
    except ValueError as e:
        raise ValueError(f'Ошибка преобразования: {e}') from e
    return MeterReading(resource, date, value, quality)

def file_open(filename: str):
    data = []
    with open((filename or "data.txt"), 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(parse_line_shlex(line))
    return data
