from typing import List, Optional
import datetime
from classes import MeterReading

def add_record(data: List[MeterReading], resource: str, date: datetime.date, value: float) -> List[MeterReading]:
    data.append(MeterReading(resource, date, value))
    return data

def delete_record(data: List[MeterReading], index: int) -> List[MeterReading]:
    if 0 <= index < len(data):
        data.pop(index)
    return data

def find_record(data: List[MeterReading], resource: Optional[str] = None, date: Optional[datetime.date] = None) -> List[MeterReading]:
    result = data[:]
    if resource:
        result = [r for r in result if r.resource == resource]
    if date:
        result = [r for r in result if r.date == date]
    return result