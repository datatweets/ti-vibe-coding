# Generate Tests for a Module

Given a source file path (e.g. `src/sensor_toolkit/validators.py`), generate pytest test cases that:

1. Cover the **happy path** for every public function
2. Cover **boundary conditions** (min/max valid values, off-by-one)
3. Cover **invalid / error inputs** (wrong types, out-of-range values, None)
4. Mirror the file structure: `src/sensor_toolkit/foo.py` → `tests/test_foo.py`
5. Use fixtures in `conftest.py` for any shared sensor-reading dicts

After generating, run `pytest tests/ -q` to confirm all tests pass.
