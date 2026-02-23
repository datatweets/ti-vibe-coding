"""Validation functions for sensor readings."""

import re
from datetime import datetime
from typing import Any

SensorReading = dict[str, Any]


def validate_timestamp(timestamp: Any) -> tuple[bool, str]:
    """Validate ISO 8601 datetime format.

    Args:
        timestamp: Value to validate as ISO 8601 datetime.

    Returns:
        Tuple of (is_valid, error_message).
    """
    if not isinstance(timestamp, str):
        return False, f"timestamp must be string, got {type(timestamp).__name__}"

    try:
        datetime.fromisoformat(timestamp)
        return True, ""
    except (ValueError, TypeError):
        return False, f"invalid ISO 8601 format: {timestamp}"


def validate_sensor_id(sensor_id: Any) -> tuple[bool, str]:
    """Validate TI sensor ID format (TI-XXXX where X is alphanumeric).

    Args:
        sensor_id: Value to validate as sensor ID.

    Returns:
        Tuple of (is_valid, error_message).
    """
    if not isinstance(sensor_id, str):
        return False, f"sensor_id must be string, got {type(sensor_id).__name__}"

    pattern = r"^TI-[A-Z0-9]{4}$"
    if re.match(pattern, sensor_id):
        return True, ""
    return False, f"sensor_id must match TI-XXXX format, got {sensor_id}"


def validate_temperature(temp: Any) -> tuple[bool, str]:
    """Validate temperature in range [-40, 150] °C.

    Args:
        temp: Value to validate as temperature.

    Returns:
        Tuple of (is_valid, error_message).
    """
    try:
        value = float(temp)
    except (TypeError, ValueError):
        return False, f"temperature must be numeric, got {temp}"

    if -40 <= value <= 150:
        return True, ""
    return False, f"temperature out of range [-40, 150]: {value}"


def validate_pressure(pressure: Any) -> tuple[bool, str]:
    """Validate pressure in range [0, 1000] hPa.

    Args:
        pressure: Value to validate as pressure.

    Returns:
        Tuple of (is_valid, error_message).
    """
    try:
        value = float(pressure)
    except (TypeError, ValueError):
        return False, f"pressure must be numeric, got {pressure}"

    if 0 <= value <= 1000:
        return True, ""
    return False, f"pressure out of range [0, 1000]: {value}"


def validate_humidity(humidity: Any) -> tuple[bool, str]:
    """Validate humidity in range [0, 100] %.

    Args:
        humidity: Value to validate as humidity.

    Returns:
        Tuple of (is_valid, error_message).
    """
    try:
        value = float(humidity)
    except (TypeError, ValueError):
        return False, f"humidity must be numeric, got {humidity}"

    if 0 <= value <= 100:
        return True, ""
    return False, f"humidity out of range [0, 100]: {value}"


def validate_reading(reading: SensorReading) -> tuple[bool, dict[str, str]]:
    """Validate a complete sensor reading.

    Args:
        reading: Dictionary with timestamp, sensor_id, temperature,
            pressure, humidity keys.

    Returns:
        Tuple of (is_valid, errors_dict). Errors dict contains field
        names as keys and error messages as values (empty if valid).
    """
    errors = {}
    required_fields = [
        "timestamp",
        "sensor_id",
        "temperature",
        "pressure",
        "humidity",
    ]

    for field in required_fields:
        if field not in reading:
            errors[field] = f"missing required field: {field}"

    if not errors:
        validators = {
            "timestamp": validate_timestamp,
            "sensor_id": validate_sensor_id,
            "temperature": validate_temperature,
            "pressure": validate_pressure,
            "humidity": validate_humidity,
        }

        for field, validator in validators.items():
            valid, msg = validator(reading[field])
            if not valid:
                errors[field] = msg

    return len(errors) == 0, errors
