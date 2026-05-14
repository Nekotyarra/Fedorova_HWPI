"""Тесты для функций управления данными."""

import pytest
import datetime
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_manager import add_record, delete_record, find_record
from classes import MeterReading


class TestDataManager:
    """Тесты для функций управления данными."""

    def setup_method(self):
        """Подготовка данных перед каждым тестом."""
        self.data = [
            MeterReading("Электроэнергия", datetime.date(2024, 11, 20), 150.75, "good"),
            MeterReading("Водоснабжение", datetime.date(2024, 12, 1), 95.0, "normal"),
            MeterReading("Газ", datetime.date(2025, 1, 15), 1234.56, "excellent"),
        ]

    def test_add_record(self):
        """Тест добавления записи."""
        new_record = MeterReading("Отопление", datetime.date(2024, 10, 1), 0.0, "bad")
        result = add_record(self.data, "Отопление", datetime.date(2024, 10, 1), 0.0, "bad")

        assert len(result) == 4
        assert result[-1] == new_record

    def test_delete_record_valid_index(self):
        """Тест удаления записи по корректному индексу."""
        result = delete_record(self.data, 0)

        assert len(result) == 2
        assert result[0].resource == "Водоснабжение"

    def test_delete_record_invalid_index(self):
        """Тест удаления по неверному индексу."""
        result = delete_record(self.data, 10)

        assert len(result) == 3

    def test_find_records_by_resource(self):
        """Тест поиска записей по ресурсу."""
        results = find_record(self.data, resource="Электроэнергия")

        assert len(results) == 1
        assert results[0].resource == "Электроэнергия"

    def test_find_records_by_date(self):
        """Тест поиска записей по дате."""
        results = find_record(self.data, date=datetime.date(2024, 12, 1))

        assert len(results) == 1
        assert results[0].resource == "Водоснабжение"

    def test_find_records_by_resource_and_date(self):
        """Тест поиска по ресурсу и дате."""
        results = find_record(
            self.data,
            resource="Газ",
            date=datetime.date(2025, 1, 15)
        )

        assert len(results) == 1
        assert results[0].value == 1234.56

    def test_find_records_no_match(self):
        """Тест поиска без совпадений."""
        results = find_record(self.data, resource="Несуществующий ресурс")

        assert results == []