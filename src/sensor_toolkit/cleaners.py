"""Data cleaning and normalization for sensor readings."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .validators import SensorReading

SensorReadingDict = dict[str, Any]


def clean_temperature(temp: Any) -> float | None:
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


def clean_pressure(pressure: Any) -> float | None:
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


def clean_humidity(humidity: Any) -> float | None:
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


def clean_sensor_id(sensor_id: Any) -> str | None:
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


def clean_timestamp(timestamp: Any) -> str | None:
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


def clean_reading(reading: SensorReadingDict) -> SensorReadingDict:
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


def remove_duplicates(readings: list[SensorReading]) -> list[SensorReading]:
    """Remove duplicate sensor readings based on timestamp and sensor_id.

    Deduplicates readings by the combination of (timestamp, sensor_id),
    keeping the first occurrence of each unique pair.

    Args:
        readings: List of SensorReading instances to deduplicate.

    Returns:
        List of unique SensorReading instances with duplicates removed.

    Examples:
        >>> from datetime import datetime
        >>> from sensor_toolkit.validators import SensorReading
        >>> readings = [
        ...     SensorReading(datetime(2025, 1, 1, 12, 0), "TI-A001-B001", 25.0, 500.0, 50.0),
        ...     SensorReading(datetime(2025, 1, 1, 12, 0), "TI-A001-B001", 26.0, 501.0, 51.0),
        ... ]
        >>> unique = remove_duplicates(readings)
        >>> len(unique)
        1
    """
    seen: set[tuple[datetime, str]] = set()
    result: list[SensorReading] = []

    for reading in readings:
        key = (reading.timestamp, reading.sensor_id)
        if key not in seen:
            seen.add(key)
            result.append(reading)

    return result


def clamp_outliers(
    readings: list[SensorReading],
    temp_range: tuple[float, float] = (-40, 150),
    pressure_range: tuple[float, float] = (0, 1000),
    humidity_range: tuple[float, float] = (0, 100),
) -> list[SensorReading]:
    """Clamp sensor reading values to valid ranges.

    Instead of removing readings with out-of-range values, this function
    clamps each value to the nearest valid boundary.

    Args:
        readings: List of SensorReading instances to process.
        temp_range: Valid temperature range as (min, max). Defaults to (-40, 150).
        pressure_range: Valid pressure range as (min, max). Defaults to (0, 1000).
        humidity_range: Valid humidity range as (min, max). Defaults to (0, 100).

    Returns:
        List of SensorReading instances with values clamped to valid ranges.

    Examples:
        >>> from datetime import datetime
        >>> from sensor_toolkit.validators import SensorReading
        >>> readings = [
        ...     SensorReading(datetime.now(), "TI-A001-B001", 200.0, -50.0, 150.0),
        ... ]
        >>> clamped = clamp_outliers(readings)
        >>> clamped[0].temperature
        150.0
        >>> clamped[0].pressure
        0.0
        >>> clamped[0].humidity
        100.0
    """
    from .validators import SensorReading as SR

    result: list[SensorReading] = []

    for reading in readings:
        clamped_temp = max(temp_range[0], min(temp_range[1], reading.temperature))
        clamped_pressure = max(pressure_range[0], min(pressure_range[1], reading.pressure))
        clamped_humidity = max(humidity_range[0], min(humidity_range[1], reading.humidity))

        result.append(
            SR(
                timestamp=reading.timestamp,
                sensor_id=reading.sensor_id,
                temperature=clamped_temp,
                pressure=clamped_pressure,
                humidity=clamped_humidity,
            )
        )

    return result


def fill_missing_timestamps(
    readings: list[SensorReading],
    interval_seconds: int = 60,
) -> list[SensorReading]:
    """Fill gaps in time series data with placeholder readings.

    Inserts placeholder readings for missing time intervals. Placeholder
    readings use NaN values for temperature, pressure, and humidity to
    indicate missing data.

    Args:
        readings: List of SensorReading instances sorted by timestamp.
        interval_seconds: Expected interval between readings in seconds.
            Defaults to 60.

    Returns:
        List of SensorReading instances with gaps filled. Original readings
        are preserved; placeholder readings have NaN values for measurements.

    Examples:
        >>> from datetime import datetime
        >>> from sensor_toolkit.validators import SensorReading
        >>> readings = [
        ...     SensorReading(datetime(2025, 1, 1, 12, 0), "TI-A001-B001", 25.0, 500.0, 50.0),
        ...     SensorReading(datetime(2025, 1, 1, 12, 2), "TI-A001-B001", 26.0, 501.0, 51.0),
        ... ]
        >>> filled = fill_missing_timestamps(readings, interval_seconds=60)
        >>> len(filled)  # Original 2 + 1 placeholder
        3
    """
    from .validators import SensorReading as SR

    if not readings:
        return []

    # Sort readings by timestamp
    sorted_readings = sorted(readings, key=lambda r: r.timestamp)
    result: list[SensorReading] = []
    interval = timedelta(seconds=interval_seconds)

    for i, reading in enumerate(sorted_readings):
        result.append(reading)

        # Check if there's a next reading and if there's a gap
        if i < len(sorted_readings) - 1:
            next_reading = sorted_readings[i + 1]
            current_time = reading.timestamp + interval

            # Fill gaps with placeholder readings
            while current_time < next_reading.timestamp:
                placeholder = SR(
                    timestamp=current_time,
                    sensor_id=reading.sensor_id,
                    temperature=float("nan"),
                    pressure=float("nan"),
                    humidity=float("nan"),
                )
                result.append(placeholder)
                current_time += interval

    return result
