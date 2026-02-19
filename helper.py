import shlex
import datetime
import classes
from classes import MeterReading


def parse_line_shlex(line: str) -> classes.MeterReading:
    """
    Функция, которая разделяет строку по пробелам, игнорируя пробелы в подстроках
    :param line: строка
    :return: Класс MeterReading (показания счетчиков)
    """
    parts = shlex.split(line)
    # ['Электро 123', '2024-11-20', '150.75']
    resource = parts[0]
    date = datetime.datetime.strptime(parts[1], '%Y.%m.%d').date()
    value = float(parts[2])
    return MeterReading(resource= resource, date=date, value=value)

def add_record(data: list[MeterReading], resource: str, date: datetime.date, value: float) -> list[MeterReading]:
    """Добавляет новую запись в список"""
    data.append(MeterReading(resource, date, value))
    return data

def delete_record(data: list[MeterReading], index: int) -> list[MeterReading]:
    """Удаляет запись по индексу"""
    if 0 <= index < len(data):
        data.pop(index)
    return data