"""Tests for src/sensor_toolkit/validators.py."""

import pytest

from sensor_toolkit.validators import (
    validate_humidity,
    validate_pressure,
    validate_reading,
    validate_sensor_id,
    validate_temperature,
    validate_timestamp,
)


class TestValidateTimestamp:
    def test_valid_iso8601(self):
        valid, msg = validate_timestamp("2025-06-01T08:00:00")
        assert valid is True
        assert msg == ""

    def test_valid_iso8601_with_z(self):
        valid, msg = validate_timestamp("2025-06-01T08:00:00Z")
        assert valid is True

    def test_invalid_format(self):
        valid, msg = validate_timestamp("2025/06/01 08:00:00")
        assert valid is False
        assert "invalid ISO 8601" in msg

    def test_non_string_type(self):
        valid, msg = validate_timestamp(1234567890)
        assert valid is False
        assert "must be string" in msg

    def test_empty_string(self):
        valid, msg = validate_timestamp("")
        assert valid is False


class TestValidateSensorId:
    def test_valid_sensor_id(self):
        valid, msg = validate_sensor_id("TI-A001")
        assert valid is True
        assert msg == ""

    def test_valid_numeric_suffix(self):
        valid, msg = validate_sensor_id("TI-9999")
        assert valid is True

    def test_lowercase_invalid(self):
        valid, msg = validate_sensor_id("ti-a001")
        assert valid is False
        assert "TI-XXXX format" in msg

    def test_wrong_prefix(self):
        valid, msg = validate_sensor_id("TX-A001")
        assert valid is False

    def test_too_short(self):
        valid, msg = validate_sensor_id("TI-A00")
        assert valid is False

    def test_non_string_type(self):
        valid, msg = validate_sensor_id(123)
        assert valid is False
        assert "must be string" in msg


class TestValidateTemperature:
    def test_valid_minimum(self):
        valid, msg = validate_temperature(-40)
        assert valid is True

    def test_valid_maximum(self):
        valid, msg = validate_temperature(150)
        assert valid is True

    def test_valid_middle(self):
        valid, msg = validate_temperature(25.5)
        assert valid is True

    def test_below_range(self):
        valid, msg = validate_temperature(-41)
        assert valid is False
        assert "out of range" in msg

    def test_above_range(self):
        valid, msg = validate_temperature(151)
        assert valid is False

    def test_string_numeric(self):
        valid, msg = validate_temperature("25.5")
        assert valid is True

    def test_non_numeric(self):
        valid, msg = validate_temperature("cold")
        assert valid is False
        assert "must be numeric" in msg


class TestValidatePressure:
    def test_valid_minimum(self):
        valid, msg = validate_pressure(0)
        assert valid is True

    def test_valid_maximum(self):
        valid, msg = validate_pressure(1000)
        assert valid is True

    def test_valid_middle(self):
        valid, msg = validate_pressure(985.5)
        assert valid is True

    def test_below_range(self):
        valid, msg = validate_pressure(-1)
        assert valid is False

    def test_above_range(self):
        valid, msg = validate_pressure(1001)
        assert valid is False

    def test_string_numeric(self):
        valid, msg = validate_pressure("987.32")
        assert valid is True

    def test_non_numeric(self):
        valid, msg = validate_pressure("high")
        assert valid is False


class TestValidateHumidity:
    def test_valid_minimum(self):
        valid, msg = validate_humidity(0)
        assert valid is True

    def test_valid_maximum(self):
        valid, msg = validate_humidity(100)
        assert valid is True

    def test_valid_middle(self):
        valid, msg = validate_humidity(65.5)
        assert valid is True

    def test_below_range(self):
        valid, msg = validate_humidity(-0.1)
        assert valid is False

    def test_above_range(self):
        valid, msg = validate_humidity(101)
        assert valid is False

    def test_string_numeric(self):
        valid, msg = validate_humidity("50.25")
        assert valid is True

    def test_non_numeric(self):
        valid, msg = validate_humidity("wet")
        assert valid is False


class TestValidateReading:
    @pytest.fixture
    def good_reading(self):
        return {
            "timestamp": "2025-06-01T08:00:00",
            "sensor_id": "TI-A001",
            "temperature": 25.0,
            "pressure": 990.0,
            "humidity": 60.0,
        }

    def test_all_valid(self, good_reading):
        valid, errors = validate_reading(good_reading)
        assert valid is True
        assert errors == {}

    def test_missing_field(self, good_reading):
        del good_reading["temperature"]
        valid, errors = validate_reading(good_reading)
        assert valid is False
        assert "temperature" in errors
        assert "missing required field" in errors["temperature"]

    def test_invalid_temperature(self, good_reading):
        good_reading["temperature"] = 200
        valid, errors = validate_reading(good_reading)
        assert valid is False
        assert "temperature" in errors

    def test_invalid_humidity(self, good_reading):
        good_reading["humidity"] = -5
        valid, errors = validate_reading(good_reading)
        assert valid is False
        assert "humidity" in errors

    def test_multiple_errors(self, good_reading):
        good_reading["temperature"] = 200
        good_reading["sensor_id"] = "invalid"
        valid, errors = validate_reading(good_reading)
        assert valid is False
        assert "temperature" in errors
        assert "sensor_id" in errors

    def test_all_fields_invalid(self, good_reading):
        good_reading = {
            "timestamp": "not-a-date",
            "sensor_id": "bad-id",
            "temperature": 500,
            "pressure": -100,
            "humidity": 999,
        }
        valid, errors = validate_reading(good_reading)
        assert valid is False
        assert len(errors) == 5
