"""Analytics functions for sensor data processing."""

from collections import deque
from typing import Literal

from sensor_toolkit.decorators import timed

SensorField = Literal["temperature", "pressure", "humidity"]
SensorReading = dict[str, str | float]


@timed
def moving_average(
    readings: list[SensorReading],
    field: SensorField,
    window: int = 5,
) -> list[float | None]:
    """Calculate a simple moving average over a list of sensor readings.

    Args:
        readings: List of sensor reading dicts, each containing the target field
            as a numeric value. Non-numeric or missing values are skipped (treated
            as gaps) and produce ``None`` in the output.
        field: The sensor field to average. One of ``"temperature"``,
            ``"pressure"``, or ``"humidity"``.
        window: Number of readings to include in each average. Must be >= 1.

    Returns:
        A list of the same length as ``readings``. Each position contains the
        mean of up to ``window`` preceding valid values, or ``None`` when fewer
        than ``window`` valid values are available.

    Raises:
        ValueError: If ``window`` is less than 1.

    Example:
        >>> readings = [{"temperature": t} for t in [20.0, 22.0, 21.0, 23.0, 24.0]]
        >>> moving_average(readings, "temperature", window=3)
        [None, None, 21.0, 22.0, 22.666...]
    """
    if window < 1:
        raise ValueError(f"window must be >= 1, got {window}")

    results: list[float | None] = []
    buf: deque[float] = deque(maxlen=window)

    for reading in readings:
        raw = reading.get(field)
        try:
            value = float(raw)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            results.append(None)
            continue

        buf.append(value)
        if len(buf) == window:
            results.append(round(sum(buf) / window, 6))
        else:
            results.append(None)

    return results
