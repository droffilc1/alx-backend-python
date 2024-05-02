#!/usr/bin/env python3
""" 7-to_kv """
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """Type-annotated function that takes a string and an int OR float as arguments
    Returns a tuple.
    """
    return (k, v ** 2)
