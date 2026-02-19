import datetime
from dataclasses import dataclass

@dataclass
class MeterReading:
    resource: str
    date: datetime.date
    value: float

