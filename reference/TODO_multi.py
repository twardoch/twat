#!/usr/bin/env -S uv run
# /// script
# dependencies = ["pathos"]
# ///
"""
Parallel processing utilities using Pathos multiprocessing library.

This module provides convenient wrappers and decorators around Pathos pools
for easy parallel processing. It includes a context manager for pool management
and decorators for common parallel mapping operations.

Example usage:
    from pathos_ops import pathos_with, amap, imap, pmap

    # Using context manager directly
    with pathos_with() as pool:
        results = pool.map(lambda x: x*2, range(1000))

    # Using decorators
    @amap
    def parallel_square(x):
        return x * x

    results = parallel_square(range(1000))
"""

from __future__ import annotations

import time
from functools import wraps
from typing import TYPE_CHECKING, Any, Literal, TypeVar

from pathos.helpers import mp
from pathos.pools import ProcessPool

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

T = TypeVar("T")
U = TypeVar("U")


class pathos_with:
    """
    Context manager for Pathos parallel processing pools.

    Handles creation and cleanup of Pathos pools with proper resource management.
    Automatically determines optimal number of processes based on CPU count.

    Args:
        pool_class: The Pathos pool class to use (default: ProcessPool)
        nodes: Number of processes to use. If None, uses CPU count (default: None)

    Example:
        >>> with pathos_with() as pool:
        ...     results = pool.map(lambda x: x*2, range(100))
        >>> print(results[:5])
        [0, 2, 4, 6, 8]
    """

    def __init__(self, pool_class: type = ProcessPool, nodes: int | None = None):
        self.pool_class = pool_class
        self.nodes = nodes if nodes is not None else mp.cpu_count()
        self.pool: ProcessPool | None = None

    def __enter__(self) -> ProcessPool:
        self.pool = self.pool_class(nodes=self.nodes)
        return self.pool

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> Literal[False]:
        if self.pool:
            self.pool.close()
            self.pool.join()
            self.pool.clear()
        return False  # Propagate exceptions


def pathos_map_decorator(method_name: str, get_result: bool = False) -> Callable:
    """
    Creates a decorator for parallel mapping operations using Pathos pools.

    Args:
        method_name: Name of the pool method to use ('map', 'imap', or 'amap')
        get_result: Whether to call .get() on the result (for amap) (default: False)

    Returns:
        A decorator function that wraps the target function for parallel execution

    Example:
        >>> @pathos_map_decorator('map')
        ... def parallel_func(x):
        ...     return x * 2
        >>> results = parallel_func(range(5))
        >>> list(results)
        [0, 2, 4, 6, 8]
    """

    def decorator(func: Callable[[T], U]) -> Callable[[Iterator[T]], Iterator[U]]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with pathos_with() as pool:
                if not args:
                    msg = "No iterable provided to parallel function"
                    raise ValueError(msg)
                method = getattr(pool, method_name)
                result = method(func, args[0])
                if get_result:
                    result = result.get()
                return result

        return wrapper

    return decorator


# Convenience decorators for different mapping strategies
imap = pathos_map_decorator("imap")  # Lazy evaluation, returns iterator
amap = pathos_map_decorator("amap", get_result=True)  # Async evaluation with .get()
pmap = pathos_map_decorator("map")  # Standard parallel map


# Example functions demonstrating decorator usage
@amap
def isquare(x: int) -> int:
    """Square a number using async parallel processing."""
    return x * x


@amap
def isubs(x: int) -> int:
    """Subtract 1 from a number using async parallel processing."""
    return x - 1


def square(x: int) -> int:
    """Square a number (sequential version for comparison)."""
    return x * x


def subs(x: int) -> int:
    """Subtract 1 from a number (sequential version for comparison)."""
    return x - 1


def main() -> None:
    """
    Demonstration of parallel vs sequential processing performance.

    Compares execution time of parallel and sequential operations
    on a range of numbers using various mapping strategies.
    """
    # Example 1: Sequential map vs parallel map for squaring
    time.perf_counter()
    list(map(square, range(200)))

    time.perf_counter()
    list(isquare(range(200)))

    # Example 2: Sequential vs parallel composition of functions
    time.perf_counter()
    list(map(subs, map(square, range(200))))

    time.perf_counter()
    list(isubs(isquare(range(200))))


if __name__ == "__main__":
    main()
