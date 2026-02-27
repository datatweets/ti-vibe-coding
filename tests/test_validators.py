"""Tests for src/sensor_toolkit/validators.py using BICEP framework.

BICEP Framework Coverage:
- Boundary: All range limits for temp, pressure, humidity, sensor_id
- Inverse: Valid input gives no errors, invalid gives errors
- Cross-check: Batch totals are internally consistent
- Error: None, wrong types, missing fields, empty strings
- Performance: Batch of 10K readings under 1 second
"""

import time
from datetime import datetime

import pytest

from sensor_toolkit.validators import (
    SensorReading,
    validate_batch,
    validate_reading,
)

# =============================================================================
# BOUNDARY TESTS - Test all range limits systematically
# =============================================================================


class TestBoundaryTemperature:
    """Boundary tests for temperature field: valid range [-40, 150] °C."""

    @pytest.fixture
    def base_reading(self) -> SensorReading:
        return SensorReading(
            timestamp=datetime(2025, 6, 1, 8, 0, 0),
            sensor_id="TI-A001-B002",
            temperature=25.0,
            pressure=500.0,
            humidity=50.0,
        )

    @pytest.mark.parametrize(
        "temp,expected_valid",
        [
            # Below minimum boundary
            (-41.0, False),
            (-40.1, False),
            (-40.01, False),
            # At minimum boundary (inclusive)
            (-40.0, True),
            # Just inside minimum
            (-39.99, True),
            (-39.0, True),
            # Middle of range
            (0.0, True),
            (25.0, True),
            (55.0, True),
            # Just inside maximum
            (149.0, True),
            (149.99, True),
            # At maximum boundary (inclusive)
            (150.0, True),
            # Above maximum boundary
            (150.01, False),
            (150.1, False),
            (151.0, False),
        ],
        ids=[
            "temp=-41.0_below_min",
            "temp=-40.1_below_min",
            "temp=-40.01_below_min",
            "temp=-40.0_at_min",
            "temp=-39.99_inside_min",
            "temp=-39.0_inside",
            "temp=0.0_middle",
            "temp=25.0_middle",
            "temp=55.0_middle",
            "temp=149.0_inside",
            "temp=149.99_inside_max",
            "temp=150.0_at_max",
            "temp=150.01_above_max",
            "temp=150.1_above_max",
            "temp=151.0_above_max",
        ],
    )
    def test_temperature_boundaries(
        self, base_reading: SensorReading, temp: float, expected_valid: bool
    ):
        base_reading.temperature = temp
        errors = validate_reading(base_reading)
        if expected_valid:
            assert not any("temperature" in e for e in errors), f"Temp {temp} should be valid"
        else:
            assert any("temperature out of range" in e for e in errors), (
                f"Temp {temp} should be invalid"
            )


class TestBoundaryPressure:
    """Boundary tests for pressure field: valid range [0, 1000] hPa."""

    @pytest.fixture
    def base_reading(self) -> SensorReading:
        return SensorReading(
            timestamp=datetime(2025, 6, 1, 8, 0, 0),
            sensor_id="TI-A001-B002",
            temperature=25.0,
            pressure=500.0,
            humidity=50.0,
        )

    @pytest.mark.parametrize(
        "pressure,expected_valid",
        [
            # Below minimum boundary
            (-1.0, False),
            (-0.1, False),
            (-0.01, False),
            # At minimum boundary (inclusive)
            (0.0, True),
            # Just inside minimum
            (0.01, True),
            (0.1, True),
            # Middle of range
            (500.0, True),
            (750.0, True),
            # Just inside maximum
            (999.9, True),
            (999.99, True),
            # At maximum boundary (inclusive)
            (1000.0, True),
            # Above maximum boundary
            (1000.01, False),
            (1000.1, False),
            (1001.0, False),
        ],
        ids=[
            "pressure=-1.0_below_min",
            "pressure=-0.1_below_min",
            "pressure=-0.01_below_min",
            "pressure=0.0_at_min",
            "pressure=0.01_inside_min",
            "pressure=0.1_inside",
            "pressure=500.0_middle",
            "pressure=750.0_middle",
            "pressure=999.9_inside",
            "pressure=999.99_inside_max",
            "pressure=1000.0_at_max",
            "pressure=1000.01_above_max",
            "pressure=1000.1_above_max",
            "pressure=1001.0_above_max",
        ],
    )
    def test_pressure_boundaries(
        self, base_reading: SensorReading, pressure: float, expected_valid: bool
    ):
        base_reading.pressure = pressure
        errors = validate_reading(base_reading)
        if expected_valid:
            assert not any("pressure" in e for e in errors), f"Pressure {pressure} should be valid"
        else:
            assert any("pressure out of range" in e for e in errors), (
                f"Pressure {pressure} should be invalid"
            )


class TestBoundaryHumidity:
    """Boundary tests for humidity field: valid range [0, 100] %."""

    @pytest.fixture
    def base_reading(self) -> SensorReading:
        return SensorReading(
            timestamp=datetime(2025, 6, 1, 8, 0, 0),
            sensor_id="TI-A001-B002",
            temperature=25.0,
            pressure=500.0,
            humidity=50.0,
        )

    @pytest.mark.parametrize(
        "humidity,expected_valid",
        [
            # Below minimum boundary
            (-1.0, False),
            (-0.1, False),
            (-0.01, False),
            # At minimum boundary (inclusive)
            (0.0, True),
            # Just inside minimum
            (0.01, True),
            (0.1, True),
            # Middle of range
            (50.0, True),
            (75.0, True),
            # Just inside maximum
            (99.9, True),
            (99.99, True),
            # At maximum boundary (inclusive)
            (100.0, True),
            # Above maximum boundary
            (100.01, False),
            (100.1, False),
            (101.0, False),
        ],
        ids=[
            "humidity=-1.0_below_min",
            "humidity=-0.1_below_min",
            "humidity=-0.01_below_min",
            "humidity=0.0_at_min",
            "humidity=0.01_inside_min",
            "humidity=0.1_inside",
            "humidity=50.0_middle",
            "humidity=75.0_middle",
            "humidity=99.9_inside",
            "humidity=99.99_inside_max",
            "humidity=100.0_at_max",
            "humidity=100.01_above_max",
            "humidity=100.1_above_max",
            "humidity=101.0_above_max",
        ],
    )
    def test_humidity_boundaries(
        self, base_reading: SensorReading, humidity: float, expected_valid: bool
    ):
        base_reading.humidity = humidity
        errors = validate_reading(base_reading)
        if expected_valid:
            assert not any("humidity" in e for e in errors), f"Humidity {humidity} should be valid"
        else:
            assert any("humidity out of range" in e for e in errors), (
                f"Humidity {humidity} should be invalid"
            )


class TestBoundarySensorId:
    """Boundary tests for sensor_id format: TI-XXXX-YYYY (X,Y alphanumeric uppercase)."""

    @pytest.fixture
    def base_reading(self) -> SensorReading:
        return SensorReading(
            timestamp=datetime(2025, 6, 1, 8, 0, 0),
            sensor_id="TI-A001-B002",
            temperature=25.0,
            pressure=500.0,
            humidity=50.0,
        )

    @pytest.mark.parametrize(
        "sensor_id,expected_valid",
        [
            # Valid formats
            ("TI-A001-B002", True),
            ("TI-0000-0000", True),
            ("TI-9999-9999", True),
            ("TI-AAAA-AAAA", True),
            ("TI-ZZZZ-ZZZZ", True),
            ("TI-A1B2-C3D4", True),
            ("TI-1A2B-3C4D", True),
            # Invalid: wrong prefix
            ("TX-A001-B002", False),
            ("TT-A001-B002", False),
            ("II-A001-B002", False),
            ("ti-A001-B002", False),
            ("Ti-A001-B002", False),
            # Invalid: wrong separators
            ("TI_A001_B002", False),
            ("TI.A001.B002", False),
            ("TIA001-B002", False),
            ("TI-A001B002", False),
            # Invalid: wrong length
            ("TI-A01-B002", False),
            ("TI-A0012-B002", False),
            ("TI-A001-B02", False),
            ("TI-A001-B0023", False),
            ("TI-A001", False),
            ("TI-A001-B002-C003", False),
            # Invalid: lowercase alphanumeric
            ("TI-a001-B002", False),
            ("TI-A001-b002", False),
            ("TI-abcd-efgh", False),
            # Invalid: special characters
            ("TI-A00!-B002", False),
            ("TI-A001-B00@", False),
            ("TI-A#01-B002", False),
            # Invalid: empty/whitespace
            ("", False),
            ("   ", False),
            ("TI-    -    ", False),
        ],
        ids=[
            "valid_alphanumeric",
            "valid_all_zeros",
            "valid_all_nines",
            "valid_all_A",
            "valid_all_Z",
            "valid_mixed_1",
            "valid_mixed_2",
            "invalid_TX_prefix",
            "invalid_TT_prefix",
            "invalid_II_prefix",
            "invalid_ti_lowercase_prefix",
            "invalid_Ti_mixed_prefix",
            "invalid_underscore_sep",
            "invalid_dot_sep",
            "invalid_missing_first_sep",
            "invalid_missing_second_sep",
            "invalid_first_part_short",
            "invalid_first_part_long",
            "invalid_second_part_short",
            "invalid_second_part_long",
            "invalid_missing_second_part",
            "invalid_extra_third_part",
            "invalid_lowercase_first_part",
            "invalid_lowercase_second_part",
            "invalid_all_lowercase",
            "invalid_exclamation",
            "invalid_at_symbol",
            "invalid_hash_symbol",
            "invalid_empty_string",
            "invalid_whitespace",
            "invalid_spaces_in_parts",
        ],
    )
    def test_sensor_id_format(
        self, base_reading: SensorReading, sensor_id: str, expected_valid: bool
    ):
        base_reading.sensor_id = sensor_id
        errors = validate_reading(base_reading)
        if expected_valid:
            assert not any("sensor_id" in e for e in errors), (
                f"Sensor ID '{sensor_id}' should be valid"
            )
        else:
            assert any("TI-XXXX-YYYY format" in e for e in errors), (
                f"Sensor ID '{sensor_id}' should be invalid"
            )


# =============================================================================
# INVERSE TESTS - Valid input gives no errors, invalid gives errors
# =============================================================================


class TestInverseValidation:
    """Inverse tests: verify symmetry of valid/invalid detection."""

    def test_all_fields_valid_returns_empty_errors(self):
        """Valid input should produce no errors."""
        reading = SensorReading(
            timestamp=datetime(2025, 6, 1, 8, 0, 0),
            sensor_id="TI-A001-B002",
            temperature=25.0,
            pressure=500.0,
            humidity=50.0,
        )
        errors = validate_reading(reading)
        assert errors == [], "Valid reading should return empty error list"

    def test_all_fields_at_min_boundary_valid(self):
        """All fields at minimum boundary should be valid."""
        reading = SensorReading(
            timestamp=datetime(2025, 6, 1, 8, 0, 0),
            sensor_id="TI-0000-0000",
            temperature=-40.0,
            pressure=0.0,
            humidity=0.0,
        )
        errors = validate_reading(reading)
        assert errors == [], "All fields at minimum boundary should be valid"

    def test_all_fields_at_max_boundary_valid(self):
        """All fields at maximum boundary should be valid."""
        reading = SensorReading(
            timestamp=datetime(2025, 6, 1, 8, 0, 0),
            sensor_id="TI-ZZZZ-9999",
            temperature=150.0,
            pressure=1000.0,
            humidity=100.0,
        )
        errors = validate_reading(reading)
        assert errors == [], "All fields at maximum boundary should be valid"

    def test_single_field_invalid_produces_one_error(self):
        """Single invalid field should produce exactly one error."""
        reading = SensorReading(
            timestamp=datetime(2025, 6, 1, 8, 0, 0),
            sensor_id="TI-A001-B002",
            temperature=200.0,  # Invalid
            pressure=500.0,
            humidity=50.0,
        )
        errors = validate_reading(reading)
        assert len(errors) == 1
        assert "temperature" in errors[0]

    def test_all_fields_invalid_produces_four_errors(self):
        """All invalid fields should produce four errors."""
        reading = SensorReading(
            timestamp=datetime(2025, 6, 1, 8, 0, 0),
            sensor_id="INVALID",
            temperature=200.0,
            pressure=-100.0,
            humidity=150.0,
        )
        errors = validate_reading(reading)
        assert len(errors) == 4

    @pytest.mark.parametrize(
        "invalid_field,field_value,valid_fields",
        [
            ("sensor_id", "INVALID", {"temperature": 25.0, "pressure": 500.0, "humidity": 50.0}),
            ("temperature", 200.0, {"sensor_id": "TI-A001-B002", "pressure": 500.0, "humidity": 50.0}),
            ("pressure", -10.0, {"sensor_id": "TI-A001-B002", "temperature": 25.0, "humidity": 50.0}),
            ("humidity", 150.0, {"sensor_id": "TI-A001-B002", "temperature": 25.0, "pressure": 500.0}),
        ],
        ids=["only_sensor_id_invalid", "only_temperature_invalid", "only_pressure_invalid", "only_humidity_invalid"],
    )
    def test_inverse_single_field_isolation(
        self, invalid_field: str, field_value, valid_fields: dict
    ):
        """Each invalid field should only produce its own error."""
        data = {
            "timestamp": datetime(2025, 6, 1, 8, 0, 0),
            "sensor_id": valid_fields.get("sensor_id", "INVALID"),
            "temperature": valid_fields.get("temperature", field_value if invalid_field == "temperature" else 25.0),
            "pressure": valid_fields.get("pressure", field_value if invalid_field == "pressure" else 500.0),
            "humidity": valid_fields.get("humidity", field_value if invalid_field == "humidity" else 50.0),
        }
        if invalid_field == "sensor_id":
            data["sensor_id"] = field_value
        elif invalid_field == "temperature":
            data["temperature"] = field_value
        elif invalid_field == "pressure":
            data["pressure"] = field_value
        elif invalid_field == "humidity":
            data["humidity"] = field_value

        reading = SensorReading(**data)
        errors = validate_reading(reading)
        assert len(errors) == 1, f"Only {invalid_field} should produce an error"


# =============================================================================
# CROSS-CHECK TESTS - Batch totals are internally consistent
# =============================================================================


class TestCrossCheckBatch:
    """Cross-check tests: ensure batch validation totals are consistent."""

    def test_total_equals_valid_plus_invalid(self):
        """Total should always equal valid + invalid."""
        readings = [
            SensorReading(datetime.now(), "TI-A001-B001", 25.0, 500.0, 50.0),
            SensorReading(datetime.now(), "INVALID", 200.0, 500.0, 50.0),
            SensorReading(datetime.now(), "TI-A003-B003", 35.0, 700.0, 70.0),
            SensorReading(datetime.now(), "TI-A004-B004", -50.0, 500.0, 50.0),  # Invalid temp
        ]
        result = validate_batch(readings)
        assert result["total"] == result["valid"] + result["invalid"]

    def test_error_count_equals_invalid_count(self):
        """Number of error entries should equal invalid count."""
        readings = [
            SensorReading(datetime.now(), "TI-A001-B001", 25.0, 500.0, 50.0),
            SensorReading(datetime.now(), "INVALID", 200.0, 500.0, 50.0),
            SensorReading(datetime.now(), "TI-A003-B003", 35.0, 1500.0, 70.0),  # Invalid pressure
        ]
        result = validate_batch(readings)
        assert len(result["errors"]) == result["invalid"]

    def test_error_indices_unique_and_valid(self):
        """Error indices should be unique and within bounds."""
        readings = [
            SensorReading(datetime.now(), "INVALID1", 200.0, 500.0, 50.0),
            SensorReading(datetime.now(), "TI-A002-B002", 25.0, 500.0, 50.0),
            SensorReading(datetime.now(), "INVALID3", 25.0, 500.0, 150.0),
            SensorReading(datetime.now(), "INVALID4", -50.0, -10.0, 50.0),
        ]
        result = validate_batch(readings)
        indices = [e["index"] for e in result["errors"]]

        # All indices should be unique
        assert len(indices) == len(set(indices)), "Error indices should be unique"

        # All indices should be valid (0 to total-1)
        for idx in indices:
            assert 0 <= idx < result["total"], f"Index {idx} out of bounds"

    def test_empty_batch_consistency(self):
        """Empty batch should have all zeros."""
        result = validate_batch([])
        assert result["total"] == 0
        assert result["valid"] == 0
        assert result["invalid"] == 0
        assert result["errors"] == []
        assert result["total"] == result["valid"] + result["invalid"]

    def test_all_valid_batch_consistency(self):
        """All valid batch should have zero invalid and no errors."""
        readings = [
            SensorReading(datetime.now(), f"TI-A00{i}-B00{i}", 25.0, 500.0, 50.0)
            for i in range(5)
        ]
        result = validate_batch(readings)
        assert result["total"] == 5
        assert result["valid"] == 5
        assert result["invalid"] == 0
        assert result["errors"] == []

    def test_all_invalid_batch_consistency(self):
        """All invalid batch should have zero valid."""
        readings = [
            SensorReading(datetime.now(), f"INVALID{i}", 200.0, 500.0, 50.0)
            for i in range(5)
        ]
        result = validate_batch(readings)
        assert result["total"] == 5
        assert result["valid"] == 0
        assert result["invalid"] == 5
        assert len(result["errors"]) == 5

    @pytest.mark.parametrize(
        "valid_count,invalid_count",
        [
            (0, 0),
            (1, 0),
            (0, 1),
            (5, 5),
            (10, 3),
            (3, 10),
            (100, 50),
        ],
        ids=[
            "empty",
            "one_valid",
            "one_invalid",
            "equal_valid_invalid",
            "more_valid",
            "more_invalid",
            "large_mixed",
        ],
    )
    def test_batch_consistency_parametrized(self, valid_count: int, invalid_count: int):
        """Parametrized test for batch consistency across various sizes."""
        readings = []
        # Add valid readings
        for i in range(valid_count):
            readings.append(
                SensorReading(datetime.now(), f"TI-V{i:03d}-V{i:03d}", 25.0, 500.0, 50.0)
            )
        # Add invalid readings
        for i in range(invalid_count):
            readings.append(
                SensorReading(datetime.now(), f"INVALID{i}", 200.0, 500.0, 50.0)
            )

        result = validate_batch(readings)

        assert result["total"] == valid_count + invalid_count
        assert result["valid"] == valid_count
        assert result["invalid"] == invalid_count
        assert len(result["errors"]) == invalid_count
        assert result["total"] == result["valid"] + result["invalid"]


# =============================================================================
# ERROR TESTS - None, wrong types, missing fields, empty strings
# =============================================================================


class TestErrorHandlingNone:
    """Error tests for None values."""

    def test_none_sensor_id_raises_attribute_error(self):
        """None sensor_id should raise AttributeError when accessing match."""
        reading = SensorReading(
            timestamp=datetime(2025, 6, 1, 8, 0, 0),
            sensor_id=None,  # type: ignore
            temperature=25.0,
            pressure=500.0,
            humidity=50.0,
        )
        with pytest.raises(TypeError):
            validate_reading(reading)

    def test_none_temperature_raises_type_error(self):
        """None temperature should raise TypeError in comparison."""
        reading = SensorReading(
            timestamp=datetime(2025, 6, 1, 8, 0, 0),
            sensor_id="TI-A001-B002",
            temperature=None,  # type: ignore
            pressure=500.0,
            humidity=50.0,
        )
        with pytest.raises(TypeError):
            validate_reading(reading)

    def test_none_pressure_raises_type_error(self):
        """None pressure should raise TypeError in comparison."""
        reading = SensorReading(
            timestamp=datetime(2025, 6, 1, 8, 0, 0),
            sensor_id="TI-A001-B002",
            temperature=25.0,
            pressure=None,  # type: ignore
            humidity=50.0,
        )
        with pytest.raises(TypeError):
            validate_reading(reading)

    def test_none_humidity_raises_type_error(self):
        """None humidity should raise TypeError in comparison."""
        reading = SensorReading(
            timestamp=datetime(2025, 6, 1, 8, 0, 0),
            sensor_id="TI-A001-B002",
            temperature=25.0,
            pressure=500.0,
            humidity=None,  # type: ignore
        )
        with pytest.raises(TypeError):
            validate_reading(reading)


class TestErrorHandlingWrongTypes:
    """Error tests for wrong types."""

    def test_string_temperature_raises_type_error(self):
        """String temperature should raise TypeError."""
        reading = SensorReading(
            timestamp=datetime(2025, 6, 1, 8, 0, 0),
            sensor_id="TI-A001-B002",
            temperature="hot",  # type: ignore
            pressure=500.0,
            humidity=50.0,
        )
        with pytest.raises(TypeError):
            validate_reading(reading)

    def test_string_pressure_raises_type_error(self):
        """String pressure should raise TypeError."""
        reading = SensorReading(
            timestamp=datetime(2025, 6, 1, 8, 0, 0),
            sensor_id="TI-A001-B002",
            temperature=25.0,
            pressure="high",  # type: ignore
            humidity=50.0,
        )
        with pytest.raises(TypeError):
            validate_reading(reading)

    def test_string_humidity_raises_type_error(self):
        """String humidity should raise TypeError."""
        reading = SensorReading(
            timestamp=datetime(2025, 6, 1, 8, 0, 0),
            sensor_id="TI-A001-B002",
            temperature=25.0,
            pressure=500.0,
            humidity="damp",  # type: ignore
        )
        with pytest.raises(TypeError):
            validate_reading(reading)

    def test_int_sensor_id_treated_as_invalid_format(self):
        """Integer sensor_id should fail format validation."""
        reading = SensorReading(
            timestamp=datetime(2025, 6, 1, 8, 0, 0),
            sensor_id=12345,  # type: ignore
            temperature=25.0,
            pressure=500.0,
            humidity=50.0,
        )
        with pytest.raises(TypeError):
            validate_reading(reading)

    def test_list_values_raise_type_error(self):
        """List values should raise TypeError."""
        reading = SensorReading(
            timestamp=datetime(2025, 6, 1, 8, 0, 0),
            sensor_id="TI-A001-B002",
            temperature=[25.0],  # type: ignore
            pressure=500.0,
            humidity=50.0,
        )
        with pytest.raises(TypeError):
            validate_reading(reading)


class TestErrorHandlingEmptyAndSpecial:
    """Error tests for empty strings and special values."""

    def test_empty_sensor_id_invalid(self):
        """Empty sensor_id should be invalid."""
        reading = SensorReading(
            timestamp=datetime(2025, 6, 1, 8, 0, 0),
            sensor_id="",
            temperature=25.0,
            pressure=500.0,
            humidity=50.0,
        )
        errors = validate_reading(reading)
        assert any("TI-XXXX-YYYY format" in e for e in errors)

    def test_whitespace_sensor_id_invalid(self):
        """Whitespace sensor_id should be invalid."""
        reading = SensorReading(
            timestamp=datetime(2025, 6, 1, 8, 0, 0),
            sensor_id="   ",
            temperature=25.0,
            pressure=500.0,
            humidity=50.0,
        )
        errors = validate_reading(reading)
        assert any("TI-XXXX-YYYY format" in e for e in errors)

    def test_inf_temperature_invalid(self):
        """Infinity temperature should be out of range."""
        reading = SensorReading(
            timestamp=datetime(2025, 6, 1, 8, 0, 0),
            sensor_id="TI-A001-B002",
            temperature=float("inf"),
            pressure=500.0,
            humidity=50.0,
        )
        errors = validate_reading(reading)
        assert any("temperature out of range" in e for e in errors)

    def test_negative_inf_temperature_invalid(self):
        """Negative infinity temperature should be out of range."""
        reading = SensorReading(
            timestamp=datetime(2025, 6, 1, 8, 0, 0),
            sensor_id="TI-A001-B002",
            temperature=float("-inf"),
            pressure=500.0,
            humidity=50.0,
        )
        errors = validate_reading(reading)
        assert any("temperature out of range" in e for e in errors)

    def test_nan_temperature_invalid(self):
        """NaN temperature should be out of range (NaN comparisons return False)."""
        reading = SensorReading(
            timestamp=datetime(2025, 6, 1, 8, 0, 0),
            sensor_id="TI-A001-B002",
            temperature=float("nan"),
            pressure=500.0,
            humidity=50.0,
        )
        errors = validate_reading(reading)
        # NaN comparisons with <= return False, so it should fail validation
        assert any("temperature out of range" in e for e in errors)


class TestErrorHandlingBatch:
    """Error tests for batch validation edge cases."""

    def test_batch_with_none_reading_raises_error(self):
        """Batch containing None should raise AttributeError."""
        readings = [
            SensorReading(datetime.now(), "TI-A001-B001", 25.0, 500.0, 50.0),
            None,  # type: ignore
        ]
        with pytest.raises(AttributeError):
            validate_batch(readings)

    def test_batch_with_wrong_type_raises_error(self):
        """Batch containing wrong type should raise AttributeError."""
        readings = [
            SensorReading(datetime.now(), "TI-A001-B001", 25.0, 500.0, 50.0),
            "not a reading",  # type: ignore
        ]
        with pytest.raises(AttributeError):
            validate_batch(readings)

    def test_batch_with_dict_raises_error(self):
        """Batch containing dict instead of SensorReading should raise AttributeError."""
        readings = [
            {"sensor_id": "TI-A001-B001", "temperature": 25.0},  # type: ignore
        ]
        with pytest.raises(AttributeError):
            validate_batch(readings)


# =============================================================================
# PERFORMANCE TESTS - Batch of 10K readings under 1 second
# =============================================================================


class TestPerformance:
    """Performance tests for batch validation."""

    @pytest.mark.slow
    def test_batch_10k_readings_under_1_second(self):
        """Batch of 10,000 readings should validate under 1 second."""
        readings = [
            SensorReading(
                datetime.now(),
                f"TI-{i % 10000:04X}-{(i * 7) % 10000:04X}",
                (i % 190) - 40.0,  # Range from -40 to 149
                (i % 1000),  # Range from 0 to 999
                (i % 100),  # Range from 0 to 99
            )
            for i in range(10000)
        ]

        start_time = time.time()
        result = validate_batch(readings)
        elapsed_time = time.time() - start_time

        assert elapsed_time < 1.0, f"Batch validation took {elapsed_time:.2f}s, expected < 1s"
        assert result["total"] == 10000

    @pytest.mark.slow
    def test_batch_10k_all_invalid_under_1_second(self):
        """Batch of 10,000 invalid readings should validate under 1 second."""
        readings = [
            SensorReading(
                datetime.now(),
                f"INVALID{i}",  # All invalid sensor IDs
                200.0 + i,  # All invalid temperatures
                -10.0 - i,  # All invalid pressures
                150.0 + i,  # All invalid humidities
            )
            for i in range(10000)
        ]

        start_time = time.time()
        result = validate_batch(readings)
        elapsed_time = time.time() - start_time

        assert elapsed_time < 1.0, f"Batch validation took {elapsed_time:.2f}s, expected < 1s"
        assert result["total"] == 10000
        assert result["invalid"] == 10000
        assert len(result["errors"]) == 10000

    @pytest.mark.slow
    def test_batch_50k_readings_under_5_seconds(self):
        """Batch of 50,000 readings should validate under 5 seconds."""
        readings = [
            SensorReading(
                datetime.now(),
                f"TI-{i % 10000:04X}-{(i * 3) % 10000:04X}",
                (i % 190) - 40.0,
                (i % 1000),
                (i % 100),
            )
            for i in range(50000)
        ]

        start_time = time.time()
        result = validate_batch(readings)
        elapsed_time = time.time() - start_time

        assert elapsed_time < 5.0, f"Batch validation took {elapsed_time:.2f}s, expected < 5s"
        assert result["total"] == 50000

    def test_single_validation_is_fast(self):
        """Single validation should be sub-millisecond."""
        reading = SensorReading(
            datetime.now(),
            "TI-A001-B002",
            25.0,
            500.0,
            50.0,
        )

        start_time = time.time()
        for _ in range(1000):
            validate_reading(reading)
        elapsed_time = time.time() - start_time

        avg_time_ms = (elapsed_time / 1000) * 1000
        assert avg_time_ms < 1.0, f"Average validation took {avg_time_ms:.3f}ms, expected < 1ms"


# =============================================================================
# LEGACY TESTS - Original tests maintained for backward compatibility
# =============================================================================


class TestSensorReading:
    """Tests for the SensorReading dataclass."""

    def test_create_reading(self):
        reading = SensorReading(
            timestamp=datetime(2025, 6, 1, 8, 0, 0),
            sensor_id="TI-A001-B002",
            temperature=25.0,
            pressure=990.0,
            humidity=60.0,
        )
        assert reading.sensor_id == "TI-A001-B002"
        assert reading.temperature == 25.0


class TestValidateReading:
    """Tests for validate_reading function."""

    @pytest.fixture
    def good_reading(self) -> SensorReading:
        return SensorReading(
            timestamp=datetime(2025, 6, 1, 8, 0, 0),
            sensor_id="TI-A001-B002",
            temperature=25.0,
            pressure=990.0,
            humidity=60.0,
        )

    def test_all_valid(self, good_reading: SensorReading):
        errors = validate_reading(good_reading)
        assert errors == []

    def test_valid_edge_values(self):
        reading = SensorReading(
            timestamp=datetime.now(),
            sensor_id="TI-0000-9999",
            temperature=-40.0,
            pressure=0.0,
            humidity=0.0,
        )
        errors = validate_reading(reading)
        assert errors == []

    def test_valid_max_edge_values(self):
        reading = SensorReading(
            timestamp=datetime.now(),
            sensor_id="TI-ZZZZ-AAAA",
            temperature=150.0,
            pressure=1000.0,
            humidity=100.0,
        )
        errors = validate_reading(reading)
        assert errors == []

    def test_invalid_sensor_id_format(self, good_reading: SensorReading):
        good_reading.sensor_id = "TI-A001"  # Missing second part
        errors = validate_reading(good_reading)
        assert len(errors) == 1
        assert "TI-XXXX-YYYY format" in errors[0]

    def test_invalid_sensor_id_lowercase(self, good_reading: SensorReading):
        good_reading.sensor_id = "ti-a001-b002"
        errors = validate_reading(good_reading)
        assert len(errors) == 1
        assert "TI-XXXX-YYYY format" in errors[0]

    def test_invalid_sensor_id_wrong_prefix(self, good_reading: SensorReading):
        good_reading.sensor_id = "TX-A001-B002"
        errors = validate_reading(good_reading)
        assert len(errors) == 1

    def test_temperature_below_range(self, good_reading: SensorReading):
        good_reading.temperature = -41.0
        errors = validate_reading(good_reading)
        assert len(errors) == 1
        assert "temperature out of range" in errors[0]

    def test_temperature_above_range(self, good_reading: SensorReading):
        good_reading.temperature = 151.0
        errors = validate_reading(good_reading)
        assert len(errors) == 1
        assert "temperature out of range" in errors[0]

    def test_pressure_below_range(self, good_reading: SensorReading):
        good_reading.pressure = -1.0
        errors = validate_reading(good_reading)
        assert len(errors) == 1
        assert "pressure out of range" in errors[0]

    def test_pressure_above_range(self, good_reading: SensorReading):
        good_reading.pressure = 1001.0
        errors = validate_reading(good_reading)
        assert len(errors) == 1
        assert "pressure out of range" in errors[0]

    def test_humidity_below_range(self, good_reading: SensorReading):
        good_reading.humidity = -0.1
        errors = validate_reading(good_reading)
        assert len(errors) == 1
        assert "humidity out of range" in errors[0]

    def test_humidity_above_range(self, good_reading: SensorReading):
        good_reading.humidity = 100.1
        errors = validate_reading(good_reading)
        assert len(errors) == 1
        assert "humidity out of range" in errors[0]

    def test_multiple_errors(self, good_reading: SensorReading):
        good_reading.sensor_id = "INVALID"
        good_reading.temperature = 200.0
        good_reading.pressure = -10.0
        good_reading.humidity = 150.0
        errors = validate_reading(good_reading)
        assert len(errors) == 4

    def test_all_fields_invalid(self):
        reading = SensorReading(
            timestamp=datetime.now(),
            sensor_id="bad-id",
            temperature=500.0,
            pressure=-100.0,
            humidity=999.0,
        )
        errors = validate_reading(reading)
        assert len(errors) == 4


class TestValidateBatch:
    """Tests for validate_batch function."""

    def test_empty_batch(self):
        result = validate_batch([])
        assert result["total"] == 0
        assert result["valid"] == 0
        assert result["invalid"] == 0
        assert result["errors"] == []

    def test_all_valid_batch(self):
        readings = [
            SensorReading(datetime.now(), "TI-A001-B001", 25.0, 500.0, 50.0),
            SensorReading(datetime.now(), "TI-A002-B002", 30.0, 600.0, 60.0),
        ]
        result = validate_batch(readings)
        assert result["total"] == 2
        assert result["valid"] == 2
        assert result["invalid"] == 0
        assert result["errors"] == []

    def test_all_invalid_batch(self):
        readings = [
            SensorReading(datetime.now(), "INVALID1", 200.0, 500.0, 50.0),
            SensorReading(datetime.now(), "INVALID2", 200.0, 500.0, 50.0),
        ]
        result = validate_batch(readings)
        assert result["total"] == 2
        assert result["valid"] == 0
        assert result["invalid"] == 2
        assert len(result["errors"]) == 2

    def test_mixed_batch(self):
        readings = [
            SensorReading(datetime.now(), "TI-A001-B001", 25.0, 500.0, 50.0),
            SensorReading(datetime.now(), "INVALID", 200.0, 500.0, 50.0),
            SensorReading(datetime.now(), "TI-A003-B003", 35.0, 700.0, 70.0),
        ]
        result = validate_batch(readings)
        assert result["total"] == 3
        assert result["valid"] == 2
        assert result["invalid"] == 1
        assert len(result["errors"]) == 1
        assert result["errors"][0]["index"] == 1

    def test_error_details(self):
        readings = [
            SensorReading(datetime.now(), "INVALID", 200.0, -10.0, 150.0),
        ]
        result = validate_batch(readings)
        assert result["invalid"] == 1
        error_entry = result["errors"][0]
        assert error_entry["index"] == 0
        assert len(error_entry["messages"]) == 4
