"""Tests for src/sensor_toolkit/cleaners.py."""


from sensor_toolkit.cleaners import (
    clean_humidity,
    clean_pressure,
    clean_reading,
    clean_sensor_id,
    clean_temperature,
    clean_timestamp,
)


class TestCleanTemperature:
    def test_valid_temperature(self):
        assert clean_temperature(25.5) == 25.5

    def test_string_temperature(self):
        assert clean_temperature("25.5") == 25.5

    def test_rounding(self):
        assert clean_temperature(25.567) == 25.57

    def test_boundary_minimum(self):
        assert clean_temperature(-40) == -40.0

    def test_boundary_maximum(self):
        assert clean_temperature(150) == 150.0

    def test_out_of_range_low(self):
        assert clean_temperature(-41) is None

    def test_out_of_range_high(self):
        assert clean_temperature(151) is None

    def test_none_value(self):
        assert clean_temperature(None) is None

    def test_empty_string(self):
        assert clean_temperature("") is None

    def test_invalid_string(self):
        assert clean_temperature("hot") is None


class TestCleanPressure:
    def test_valid_pressure(self):
        assert clean_pressure(987.32) == 987.32

    def test_string_pressure(self):
        assert clean_pressure("987.32") == 987.32

    def test_rounding(self):
        assert clean_pressure(987.321) == 987.32

    def test_boundary_minimum(self):
        assert clean_pressure(0) == 0.0

    def test_boundary_maximum(self):
        assert clean_pressure(1000) == 1000.0

    def test_out_of_range_low(self):
        assert clean_pressure(-0.1) is None

    def test_out_of_range_high(self):
        assert clean_pressure(1001) is None

    def test_none_value(self):
        assert clean_pressure(None) is None

    def test_empty_string(self):
        assert clean_pressure("") is None

    def test_invalid_string(self):
        assert clean_pressure("high") is None


class TestCleanHumidity:
    def test_valid_humidity(self):
        assert clean_humidity(65.5) == 65.5

    def test_string_humidity(self):
        assert clean_humidity("65.5") == 65.5

    def test_rounding(self):
        assert clean_humidity(65.556) == 65.56

    def test_boundary_minimum(self):
        assert clean_humidity(0) == 0.0

    def test_boundary_maximum(self):
        assert clean_humidity(100) == 100.0

    def test_out_of_range_low(self):
        assert clean_humidity(-0.1) is None

    def test_out_of_range_high(self):
        assert clean_humidity(101) is None

    def test_none_value(self):
        assert clean_humidity(None) is None

    def test_empty_string(self):
        assert clean_humidity("") is None

    def test_invalid_string(self):
        assert clean_humidity("wet") is None


class TestCleanSensorId:
    def test_valid_sensor_id(self):
        assert clean_sensor_id("TI-A001") == "TI-A001"

    def test_lowercase_converted(self):
        assert clean_sensor_id("ti-a001") == "TI-A001"

    def test_mixed_case_converted(self):
        assert clean_sensor_id("Ti-A001") == "TI-A001"

    def test_with_whitespace(self):
        assert clean_sensor_id("  TI-A001  ") == "TI-A001"

    def test_numeric_suffix(self):
        assert clean_sensor_id("TI-9999") == "TI-9999"

    def test_too_short(self):
        assert clean_sensor_id("TI-A00") is None

    def test_too_long(self):
        assert clean_sensor_id("TI-A0001") is None

    def test_wrong_prefix(self):
        assert clean_sensor_id("TX-A001") is None

    def test_none_value(self):
        assert clean_sensor_id(None) is None

    def test_empty_string(self):
        assert clean_sensor_id("") is None

    def test_non_string(self):
        assert clean_sensor_id(123) is None


class TestCleanTimestamp:
    def test_valid_iso8601(self):
        result = clean_timestamp("2025-06-01T08:00:00")
        assert result == "2025-06-01T08:00:00"

    def test_iso8601_with_z(self):
        result = clean_timestamp("2025-06-01T08:00:00Z")
        assert result is not None

    def test_invalid_format(self):
        assert clean_timestamp("2025/06/01") is None

    def test_none_value(self):
        assert clean_timestamp(None) is None

    def test_empty_string(self):
        assert clean_timestamp("") is None

    def test_non_string(self):
        assert clean_timestamp(1234567890) is None


class TestCleanReading:
    def test_all_valid_fields(self):
        reading = {
            "timestamp": "2025-06-01T08:00:00",
            "sensor_id": "TI-A001",
            "temperature": 25.5,
            "pressure": 987.32,
            "humidity": 65.5,
        }
        result = clean_reading(reading)
        assert result["timestamp"] == "2025-06-01T08:00:00"
        assert result["sensor_id"] == "TI-A001"
        assert result["temperature"] == 25.5
        assert result["pressure"] == 987.32
        assert result["humidity"] == 65.5

    def test_some_fields_dirty(self):
        reading = {
            "timestamp": "2025-06-01T08:00:00",
            "sensor_id": "ti-a001",
            "temperature": "25.5",
            "pressure": 987.32,
            "humidity": "not-a-number",
        }
        result = clean_reading(reading)
        assert result["sensor_id"] == "TI-A001"
        assert result["temperature"] == 25.5
        assert result["humidity"] is None

    def test_all_fields_missing(self):
        reading = {}
        result = clean_reading(reading)
        assert result["timestamp"] is None
        assert result["sensor_id"] is None
        assert result["temperature"] is None
        assert result["pressure"] is None
        assert result["humidity"] is None

    def test_all_fields_invalid(self):
        reading = {
            "timestamp": "invalid",
            "sensor_id": "bad",
            "temperature": 999,
            "pressure": -100,
            "humidity": 999,
        }
        result = clean_reading(reading)
        assert result["timestamp"] is None
        assert result["sensor_id"] is None
        assert result["temperature"] is None
        assert result["pressure"] is None
        assert result["humidity"] is None

    def test_mixed_valid_invalid(self):
        reading = {
            "timestamp": "2025-06-01T08:00:00",
            "sensor_id": "TI-B002",
            "temperature": 25.0,
            "pressure": None,
            "humidity": 65.0,
        }
        result = clean_reading(reading)
        assert result["timestamp"] is not None
        assert result["sensor_id"] == "TI-B002"
        assert result["temperature"] == 25.0
        assert result["pressure"] is None
        assert result["humidity"] == 65.0
