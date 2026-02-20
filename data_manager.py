import datetime
from classes import MeterReading


def add_record(data: list[MeterReading], resource: str, date: datetime.date, value: float) -> list[MeterReading]:
    """Добавляет новую запись в список"""
    data.append(MeterReading(resource, date, value))
    return data

def delete_record(data: list[MeterReading], index: int) -> list[MeterReading]:
    """Удаляет запись по индексу"""
    if 0 <= index < len(data):
        data.pop(index)
    return data
