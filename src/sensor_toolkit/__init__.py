"""Sensor Toolkit - Python module for sensor data validation and cleaning.

ACT271-TI Vibe Coding training project.
"""

__version__ = "0.1.0"
__author__ = "Texas Instruments"

from .cleaners import (
    clamp_outliers,
    clean_humidity,
    clean_pressure,
    clean_reading,
    clean_sensor_id,
    clean_temperature,
    clean_timestamp,
    fill_missing_timestamps,
    remove_duplicates,
)
from .validators import (
    SensorReading,
    validate_batch,
    validate_reading,
)

__all__ = [
    "SensorReading",
    "validate_reading",
    "validate_batch",
    "clean_timestamp",
    "clean_sensor_id",
    "clean_temperature",
    "clean_pressure",
    "clean_humidity",
    "clean_reading",
    "remove_duplicates",
    "clamp_outliers",
    "fill_missing_timestamps",
]
