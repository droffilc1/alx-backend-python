#!/usr/bin/env python3
""" 8-make_multiplier """
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Type-annotated function that takes a float as argument
    Returns a function that multiplies a float by multiplier.
    """
    def multiplier_func(x: float) -> float:
        """Function that multiplies a float by multiplier"""
        return x * multiplier
    return multiplier_func
