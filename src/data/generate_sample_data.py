#!/usr/bin/env python3
"""Generate synthetic sensor data for ACT271-TI course.

Run once to create CSV files:
    python src/data/generate_sample_data.py
"""
import csv
import random
from datetime import datetime, timedelta

random.seed(42)

SENSORS = ["TI-A001", "TI-A002", "TI-B001", "TI-B002", "TI-C001"]
START = datetime(2025, 6, 1, 8, 0, 0)


def generate_clean(n: int = 1000) -> list[dict]:
    """Generate n clean sensor readings within valid ranges."""
    rows = []
    for i in range(n):
        ts = START + timedelta(minutes=i * 5)
        sid = SENSORS[i % len(SENSORS)]
        rows.append({
            "timestamp": ts.isoformat(),
            "sensor_id": sid,
            "temperature": round(random.uniform(18.0, 42.0), 2),
            "pressure": round(random.uniform(980.0, 1020.0), 2),
            "humidity": round(random.uniform(35.0, 85.0), 2),
        })
    return rows


def generate_dirty(n: int = 200) -> list[dict]:
    """Generate n readings with intentional quality issues."""
    rows = []
    for i in range(n):
        ts = START + timedelta(minutes=i * 5)
        sid = SENSORS[i % len(SENSORS)]
        temp = round(random.uniform(18.0, 42.0), 2)
        pres = round(random.uniform(980.0, 1020.0), 2)
        hum = round(random.uniform(35.0, 85.0), 2)

        # Inject various data quality issues
        r = random.random()
        if r < 0.05:          # 5% null temperature
            temp = ""
        elif r < 0.10:        # 5% outlier temperature
            temp = round(random.uniform(160.0, 300.0), 2)
        elif r < 0.15:        # 5% negative pressure
            pres = round(random.uniform(-50.0, -1.0), 2)
        elif r < 0.20:        # 5% humidity > 100
            hum = round(random.uniform(101.0, 150.0), 2)
        elif r < 0.25:        # 5% bad sensor ID
            sid = f"INVALID-{i}"
        elif r < 0.28:        # 3% null humidity
            hum = ""
        elif r < 0.31:        # 3% duplicate of previous row
            if rows:
                rows.append(dict(rows[-1]))
                continue

        rows.append({
            "timestamp": ts.isoformat(),
            "sensor_id": sid,
            "temperature": temp,
            "pressure": pres,
            "humidity": hum,
        })
    return rows


def write_csv(rows: list[dict], path: str) -> None:
    """Write rows to CSV file."""
    fields = ["timestamp", "sensor_id", "temperature", "pressure", "humidity"]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Wrote {len(rows)} rows → {path}")


if __name__ == "__main__":
    print("Generating sample sensor data...")
    write_csv(generate_clean(1000), "src/data/sensor_readings_1000.csv")
    write_csv(generate_dirty(200), "src/data/sensor_readings_dirty.csv")
    print("Done!")
