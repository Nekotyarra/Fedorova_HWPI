from typing import List, Optional
import datetime
from classes import MeterReading

def add_record(data: List[MeterReading], resource: str, date: datetime.date, value: float, quality: str) -> List[MeterReading]:
    data.append(MeterReading(resource, date, value, quality))
    return data

def delete_record(data: List[MeterReading], index: int) -> List[MeterReading]:
    if 0 <= index < len(data):
        data.pop(index)
    return data

def find_record(data: List[MeterReading], resource: Optional[str] = None, date: Optional[datetime.date] = None, quality:Optional[str] = None) -> List[MeterReading]:
    result = data[:]
    if resource:
        result = [r for r in result if r.resource == resource]
    if date:
        result = [r for r in result if r.date == date]
    if quality:
        result = [r for r in result if r.quality == quality]
    return result