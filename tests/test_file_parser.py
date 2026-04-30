"""Тесты для парсинга файлов."""

import pytest
import datetime
import tempfile
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from file_parser import parse_line_shlex, file_open
from classes import MeterReading


class TestParseLine:
    """Тесты для функции parse_line_shlex."""

    def test_parse_valid_line_with_dots(self):
        """Тест парсинга корректной строки с точками."""
        line = '"Электроэнергия" 2024.11.20 150.75'
        result = parse_line_shlex(line)

        assert result.resource == "Электроэнергия"
        assert result.date == datetime.date(2024, 11, 20)
        assert result.value == 150.75

    def test_parse_valid_line_with_dashes(self):
        """Тест парсинга корректной строки с дефисами."""
        line = '"Электроэнергия" 2024-11-20 150.75'
        result = parse_line_shlex(line)

        assert result.resource == "Электроэнергия"
        assert result.date == datetime.date(2024, 11, 20)
        assert result.value == 150.75

    def test_parse_line_with_multiple_spaces(self):
        """Тест парсинга строки с несколькими пробелами."""
        line = '"Газ"   2024.01.15   1234.56'
        result = parse_line_shlex(line)

        assert result.resource == "Газ"
        assert result.date == datetime.date(2024, 1, 15)
        assert result.value == 1234.56

    def test_parse_line_with_quoted_resource_having_spaces(self):
        """Тест парсинга ресурса с пробелами внутри кавычек."""
        line = '"Природный газ" 2024.12.01 95.5'
        result = parse_line_shlex(line)

        assert result.resource == "Природный газ"
        assert result.value == 95.5

    def test_parse_line_with_float_int(self):
        """Тест парсинга целого числа как float."""
        line = '"Вода" 2024.12.01 100'
        result = parse_line_shlex(line)

        assert result.value == 100.0

    def test_parse_line_raises_error_on_invalid_format(self):
        """Тест ошибки при неверном формате строки."""
        with pytest.raises(ValueError):
            parse_line_shlex("Неверная строка")

    def test_parse_line_raises_error_on_invalid_date(self):
        """Тест ошибки при неверной дате."""
        with pytest.raises(ValueError):
            parse_line_shlex('"Тест" 2024.13.45 100.0')


class TestLoadFromFile:
    """Тесты для функции load_from_file."""

    def test_load_from_valid_file(self):
        """Тест загрузки из корректного файла."""
        # Создаём временный файл с тестовыми данными
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
            f.write('"Электроэнергия" 2024.11.20 150.75\n')
            f.write('"Водоснабжение" 2024.12.01 95.0\n')
            f.write('"Газ" 2025.01.15 1234.56\n')
            temp_file = f.name

        try:
            data = file_open(temp_file)

            assert len(data) == 3
            assert data[0].resource == "Электроэнергия"
            assert data[1].date == datetime.date(2024, 12, 1)
            assert data[2].value == 1234.56
        finally:
            os.unlink(temp_file)

    def test_load_from_empty_file(self):
        """Тест загрузки из пустого файла."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
            temp_file = f.name

        try:
            data = file_open(temp_file)
            assert data == []
        finally:
            os.unlink(temp_file)

    def test_load_from_file_with_empty_lines(self):
        """Тест загрузки из файла с пустыми строками."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
            f.write('"Тест1" 2024.01.01 10.0\n')
            f.write('\n')
            f.write('"Тест2" 2024.01.02 20.0\n')
            temp_file = f.name

        try:
            data = file_open(temp_file)
            assert len(data) == 2
        finally:
            os.unlink(temp_file)

    def test_file_not_found_raises_error(self):
        """Тест ошибки при отсутствии файла."""
        with pytest.raises(FileNotFoundError):
            file_open("non_existent_file.txt")