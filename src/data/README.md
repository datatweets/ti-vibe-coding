# Sample Sensor Data

Synthetic datasets for the ACT271-TI course. **Not real TI production data.**

## Files

| File | Rows | Description |
|------|------|-------------|
| `sensor_readings_1000.csv` | 1,000 | Clean data from 5 sensors — all values within valid ranges |
| `sensor_readings_dirty.csv` | ~200 | Dirty data with nulls, outliers, bad IDs, duplicates |
| `generate_sample_data.py` | — | Script to regenerate datasets (seed=42 for reproducibility) |

## Schema

| Column | Type | Valid Range |
|--------|------|-------------|
| timestamp | ISO 8601 | 2025-06-01 onwards, 5-min intervals |
| sensor_id | string | TI-A001, TI-A002, TI-B001, TI-B002, TI-C001 |
| temperature | float | -40 to 150 °C (normal range: 18–42) |
| pressure | float | 0 to 1000 hPa (normal range: 980–1020) |
| humidity | float | 0 to 100 % (normal range: 35–85) |

## Dirty Data Issues

The `sensor_readings_dirty.csv` file contains:
- ~5% null temperatures
- ~5% temperature outliers (160–300 °C)
- ~5% negative pressure values
- ~5% humidity > 100%
- ~5% invalid sensor IDs (not TI-XXXX format)
- ~3% null humidity
- ~3% duplicate rows
