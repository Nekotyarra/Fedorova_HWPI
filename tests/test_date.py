"""Тесты для утилит работы с датами."""
import pytest
import datetime
import sys
import os

# Добавляем корневую директорию в путь для импорта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from file_parser import parse_date


class TestParseDate:
    """Тесты для функции parse_date."""

    def test_parse_date_with_dots(self):
        """Тест парсинга даты с точками."""
        date = parse_date("2024.11.20")
        assert date == datetime.date(2024, 11, 20)

    def test_parse_date_with_dashes(self):
        """Тест парсинга даты с дефисами."""
        date = parse_date("2024-11-20")
        assert date == datetime.date(2024, 11, 20)

    def test_parse_date_with_single_digits(self):
        """Тест парсинга даты с однозначными числами."""
        date = parse_date("2024.01.05")
        assert date == datetime.date(2024, 1, 5)

    def test_parse_date_leap_year(self):
        """Тест високосного года."""
        date = parse_date("2024.02.29")
        assert date == datetime.date(2024, 2, 29)

    def test_parse_date_invalid_format_raises_error(self):
        """Тест неверного формата даты."""
        with pytest.raises(ValueError, match="Дата должна быть в формате гггг.мм.дд или гггг-мм-дд"):
            parse_date("20.11.2024")

    def test_parse_date_invalid_day_raises_error(self):
        """Тест неверного дня."""
        with pytest.raises(ValueError):
            parse_date("2024.02.30")

    def test_parse_date_invalid_month_raises_error(self):
        """Тест неверного месяца."""
        with pytest.raises(ValueError):
            parse_date("2024.13.01")

    def test_parse_date_invalid_year_raises_error(self):
        """Тест неверного года."""
        with pytest.raises(ValueError):
            parse_date("abcd.11.20")