"""Utility decorators for the sensor toolkit."""

import functools
import logging
import time
from collections.abc import Callable
from typing import Any, TypeVar

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def timed(func: F) -> F:
    """Measure and log the wall-clock execution time of a function.

    Logs at DEBUG level using the module logger so timing output is
    opt-in and does not pollute production logs by default.

    Args:
        func: The function to wrap.

    Returns:
        A wrapped version of ``func`` that records elapsed time after
        each call.

    Example:
        >>> @timed
        ... def slow() -> None:
        ...     time.sleep(0.1)
        >>> slow()  # logs: "slow completed in 0.1001 s"
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            logger.debug("%s completed in %.6f s", func.__qualname__, elapsed)

    return wrapper  # type: ignore[return-value]
