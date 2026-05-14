"""Тесты для модели данных."""
import pytest
import datetime
from classes import MeterReading


class TestMeterReading:
    """Тесты для класса MeterReading."""

    def test_create_reading(self):
        """Тест создания объекта показания."""
        reading = MeterReading(
            resource="Электроэнергия",
            date=datetime.date(2024, 11, 20),
            value=150.75,
            quality="good"
        )

        assert reading.resource == "Электроэнергия"
        assert reading.date == datetime.date(2024, 11, 20)
        assert reading.value == 150.75

    def test_reading_with_zero_value(self):
        """Тест с нулевым значением."""
        reading = MeterReading("Отопление", datetime.date(2024, 10, 1), 0.0, "good")
        assert reading.value == 0.0

    def test_reading_with_negative_value(self):
        """Тест с отрицательным значением (может быть перерасчёт)."""
        reading = MeterReading("Газ", datetime.date(2024, 12, 1), -50.5, "good")
        assert reading.value == -50.5
