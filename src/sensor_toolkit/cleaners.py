"""Data cleaning and normalization for sensor readings."""

from datetime import datetime
from typing import Any, Optional

SensorReading = dict[str, Any]


def clean_temperature(temp: Any) -> Optional[float]:
    """Clean and normalize temperature value.

    Args:
        temp: Raw temperature value.

    Returns:
        Cleaned float value, or None if invalid/missing.
    """
    if temp is None or temp == "":
        return None

    try:
        value = float(temp)
        if -40 <= value <= 150:
            return round(value, 2)
        return None
    except (TypeError, ValueError):
        return None


def clean_pressure(pressure: Any) -> Optional[float]:
    """Clean and normalize pressure value.

    Args:
        pressure: Raw pressure value.

    Returns:
        Cleaned float value, or None if invalid/missing.
    """
    if pressure is None or pressure == "":
        return None

    try:
        value = float(pressure)
        if 0 <= value <= 1000:
            return round(value, 2)
        return None
    except (TypeError, ValueError):
        return None


def clean_humidity(humidity: Any) -> Optional[float]:
    """Clean and normalize humidity value.

    Args:
        humidity: Raw humidity value.

    Returns:
        Cleaned float value, or None if invalid/missing.
    """
    if humidity is None or humidity == "":
        return None

    try:
        value = float(humidity)
        if 0 <= value <= 100:
            return round(value, 2)
        return None
    except (TypeError, ValueError):
        return None


def clean_sensor_id(sensor_id: Any) -> Optional[str]:
    """Clean and normalize sensor ID.

    Args:
        sensor_id: Raw sensor ID value.

    Returns:
        Cleaned uppercase sensor ID, or None if invalid/missing.
    """
    if sensor_id is None or sensor_id == "":
        return None

    if not isinstance(sensor_id, str):
        return None

    cleaned = sensor_id.upper().strip()
    if cleaned.startswith("TI-") and len(cleaned) == 7:
        return cleaned
    return None


def clean_timestamp(timestamp: Any) -> Optional[str]:
    """Clean and normalize ISO 8601 timestamp.

    Args:
        timestamp: Raw timestamp value.

    Returns:
        Normalized ISO 8601 string, or None if invalid/missing.
    """
    if timestamp is None or timestamp == "":
        return None

    if not isinstance(timestamp, str):
        return None

    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.isoformat()
    except (ValueError, TypeError):
        return None


def clean_reading(reading: SensorReading) -> SensorReading:
    """Clean and normalize all fields in a sensor reading.

    Args:
        reading: Sensor reading dict with potentially dirty data.

    Returns:
        Cleaned reading with None values for invalid fields.
    """
    return {
        "timestamp": clean_timestamp(reading.get("timestamp")),
        "sensor_id": clean_sensor_id(reading.get("sensor_id")),
        "temperature": clean_temperature(reading.get("temperature")),
        "pressure": clean_pressure(reading.get("pressure")),
        "humidity": clean_humidity(reading.get("humidity")),
    }
