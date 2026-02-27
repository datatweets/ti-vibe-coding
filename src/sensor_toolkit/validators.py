"""Validation functions for sensor readings."""

import re
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SensorReading:
    """Represents a sensor reading with timestamp and measurements.

    Attributes:
        timestamp: ISO 8601 datetime of the reading.
        sensor_id: Sensor identifier in TI-XXXX-YYYY format.
        temperature: Temperature reading in Celsius.
        pressure: Pressure reading in hPa.
        humidity: Humidity reading as percentage.
    """

    timestamp: datetime
    sensor_id: str
    temperature: float
    pressure: float
    humidity: float


def validate_reading(reading: SensorReading) -> list[str]:
    """Validate a sensor reading against defined rules.

    Validates that all fields are within acceptable ranges:
    - temperature: [-40, 150] °C
    - pressure: [0, 1000] hPa
    - humidity: [0, 100] %
    - sensor_id: matches TI-XXXX-YYYY pattern (X, Y are alphanumeric)

    Args:
        reading: A SensorReading instance to validate.

    Returns:
        List of validation error messages. Empty list means the reading is valid.

    Examples:
        >>> from datetime import datetime
        >>> reading = SensorReading(
        ...     timestamp=datetime.now(),
        ...     sensor_id="TI-A1B2-C3D4",
        ...     temperature=25.0,
        ...     pressure=1013.25,
        ...     humidity=50.0
        ... )
        >>> errors = validate_reading(reading)
        >>> # errors will contain "pressure out of range" since 1013.25 > 1000
    """
    errors: list[str] = []

    # Validate sensor_id format: TI-XXXX-YYYY where X and Y are alphanumeric
    sensor_id_pattern = r"^TI-[A-Z0-9]{4}-[A-Z0-9]{4}$"
    if not re.match(sensor_id_pattern, reading.sensor_id):
        errors.append(
            f"sensor_id must match TI-XXXX-YYYY format, got {reading.sensor_id}"
        )

    # Validate temperature range: [-40, 150] °C
    if not -40 <= reading.temperature <= 150:
        errors.append(
            f"temperature out of range [-40, 150]: {reading.temperature}"
        )

    # Validate pressure range: [0, 1000] hPa
    if not 0 <= reading.pressure <= 1000:
        errors.append(
            f"pressure out of range [0, 1000]: {reading.pressure}"
        )

    # Validate humidity range: [0, 100] %
    if not 0 <= reading.humidity <= 100:
        errors.append(
            f"humidity out of range [0, 100]: {reading.humidity}"
        )

    return errors


def validate_batch(
    readings: list[SensorReading],
) -> dict[str, int | list[dict[str, list[str]]]]:
    """Validate a batch of sensor readings.

    Args:
        readings: List of SensorReading instances to validate.

    Returns:
        Dictionary with validation summary:
        - total: Total number of readings processed
        - valid: Count of valid readings
        - invalid: Count of invalid readings
        - errors: List of dicts with 'index' and 'messages' for each invalid reading

    Examples:
        >>> from datetime import datetime
        >>> readings = [
        ...     SensorReading(datetime.now(), "TI-A1B2-C3D4", 25.0, 500.0, 50.0),
        ...     SensorReading(datetime.now(), "INVALID", 200.0, 500.0, 50.0),
        ... ]
        >>> result = validate_batch(readings)
        >>> result["total"]
        2
        >>> result["valid"]
        1
        >>> result["invalid"]
        1
    """
    total = len(readings)
    valid = 0
    invalid = 0
    errors: list[dict[str, int | list[str]]] = []

    for index, reading in enumerate(readings):
        reading_errors = validate_reading(reading)
        if reading_errors:
            invalid += 1
            errors.append({"index": index, "messages": reading_errors})
        else:
            valid += 1

    return {
        "total": total,
        "valid": valid,
        "invalid": invalid,
        "errors": errors,
    }
