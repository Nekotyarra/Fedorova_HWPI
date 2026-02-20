import shlex
import datetime
from classes import MeterReading


def parse_line_shlex(line: str) -> MeterReading:
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

def file_open():
    data = []
    with open('data.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(parse_line_shlex(line))
    return data
