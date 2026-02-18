import shlex
from datetime import datetime

def parse_line_shlex(line: str):
    parts = shlex.split(line)
    # ['Электро 123', '2024-11-20', '150.75']
    resource = parts[0]
    date = datetime.strptime(parts[1], '%Y.%m.%d').date()
    value = float(parts[2])
    return {
        'resource': resource,
        'date': date,
        'value': value
    }

