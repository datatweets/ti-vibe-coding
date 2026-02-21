"""Tests for src/sensor_toolkit/decorators.py."""

import logging

import pytest

from sensor_toolkit.decorators import timed


def test_timed_returns_correct_value():
    @timed
    def add(a: int, b: int) -> int:
        return a + b

    assert add(2, 3) == 5


def test_timed_preserves_function_metadata():
    @timed
    def my_func() -> None:
        """My docstring."""

    assert my_func.__name__ == "my_func"
    assert my_func.__doc__ == "My docstring."


def test_timed_logs_at_debug_level(caplog):
    @timed
    def noop() -> None:
        pass

    with caplog.at_level(logging.DEBUG, logger="sensor_toolkit.decorators"):
        noop()

    assert any("noop" in record.message and "completed in" in record.message for record in caplog.records)


def test_timed_propagates_exceptions():
    @timed
    def boom() -> None:
        raise ValueError("oops")

    with pytest.raises(ValueError, match="oops"):
        boom()


def test_timed_logs_even_on_exception(caplog):
    @timed
    def boom() -> None:
        raise RuntimeError("fail")

    with caplog.at_level(logging.DEBUG, logger="sensor_toolkit.decorators"):
        with pytest.raises(RuntimeError):
            boom()

    assert any("boom" in record.message for record in caplog.records)
