import shlex
from datetime import datetime

def parse_line_shlex(line: str):
    """
    Функция, которая разделяет строку по пробелам, игнорируя пробелы в подстроках
    :param line: строка
    :return: (тип ресурса (строка), дата, значение (дробное)) кортеж из 3
    """
    parts = shlex.split(line)
    # ['Электро 123', '2024-11-20', '150.75']
    resource = parts[0]
    date = datetime.strptime(parts[1], '%Y.%m.%d').date()
    value = float(parts[2])
    return (
        resource,
        date,
        value
    )



