"""Tests for src/sensor_toolkit/analytics.py."""

import pytest

from sensor_toolkit.analytics import moving_average


@pytest.fixture
def temp_readings() -> list[dict]:
    """Five clean temperature readings."""
    return [{"temperature": float(t)} for t in [20, 22, 21, 23, 24]]


class TestMovingAverageBasic:
    def test_window_3_returns_none_until_full(self, temp_readings):
        result = moving_average(temp_readings, "temperature", window=3)
        assert result[0] is None
        assert result[1] is None

    def test_window_3_correct_values(self, temp_readings):
        result = moving_average(temp_readings, "temperature", window=3)
        assert result[2] == pytest.approx((20 + 22 + 21) / 3)
        assert result[3] == pytest.approx((22 + 21 + 23) / 3)
        assert result[4] == pytest.approx((21 + 23 + 24) / 3)

    def test_window_1_returns_each_value(self, temp_readings):
        result = moving_average(temp_readings, "temperature", window=1)
        assert result == [20.0, 22.0, 21.0, 23.0, 24.0]

    def test_output_length_matches_input(self, temp_readings):
        result = moving_average(temp_readings, "temperature", window=3)
        assert len(result) == len(temp_readings)

    def test_window_larger_than_data_all_none(self, temp_readings):
        result = moving_average(temp_readings, "temperature", window=10)
        assert all(v is None for v in result)

    def test_empty_readings_returns_empty(self):
        assert moving_average([], "temperature") == []


class TestMovingAverageFields:
    def test_pressure_field(self):
        readings = [{"pressure": p} for p in [1000.0, 1005.0, 1010.0]]
        result = moving_average(readings, "pressure", window=2)
        assert result[0] is None
        assert result[1] == pytest.approx(1002.5)
        assert result[2] == pytest.approx(1007.5)

    def test_humidity_field(self):
        readings = [{"humidity": h} for h in [50.0, 60.0, 55.0]]
        result = moving_average(readings, "humidity", window=2)
        assert result[2] == pytest.approx(57.5)


class TestMovingAverageEdgeCases:
    def test_invalid_window_raises(self, temp_readings):
        with pytest.raises(ValueError, match="window must be >= 1"):
            moving_average(temp_readings, "temperature", window=0)

    def test_missing_field_yields_none(self):
        readings = [{"temperature": 20.0}, {"pressure": 5.0}, {"temperature": 22.0}]
        result = moving_average(readings, "temperature", window=2)
        assert result[1] is None  # gap resets the window

    def test_non_numeric_value_yields_none(self):
        readings = [{"temperature": "bad"}, {"temperature": 20.0}]
        result = moving_average(readings, "temperature", window=1)
        assert result[0] is None
        assert result[1] == 20.0

    def test_string_numeric_value_is_coerced(self):
        readings = [{"temperature": "21.5"}, {"temperature": "22.5"}]
        result = moving_average(readings, "temperature", window=2)
        assert result[1] == pytest.approx(22.0)
