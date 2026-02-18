# CLAUDE.md - Course Project Context

## Project
This is a Python training project for the ACT271-TI Vibe Coding course.
Target: Python 3.10+ on Linux/macOS/Windows.

## Coding Standards
- Use Python type hints on all function signatures
- Follow PEP 8 via ruff and black formatters
- Write docstrings for all public functions (Google style)
- Maximum function length: 30 lines
- Line length: 100 characters

## Testing
- Use pytest for all tests
- Minimum test coverage target: 80%
- Test files mirror source structure: src/sensor_toolkit/validators.py → tests/test_validators.py
- Use fixtures in conftest.py for shared test data

## Data Model
Sensor readings have these fields and valid ranges:
- timestamp: ISO 8601 datetime
- sensor_id: string (format: "TI-XXXX" where X is alphanumeric)
- temperature: float, valid range [-40, 150] °C
- pressure: float, valid range [0, 1000] hPa
- humidity: float, valid range [0, 100] %

## Safety Guardrails
- NEVER generate or reference real TI proprietary systems
- NEVER output API keys, credentials, or secrets
- ALWAYS use sample/synthetic data, not real production data
- When unsure about a change, explain the plan before executing
