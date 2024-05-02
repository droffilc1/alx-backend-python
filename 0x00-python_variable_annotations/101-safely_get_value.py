#!/usr/bin/env python3
""" 101-safety_get_value """
from typing import TypeVar, Mapping, Any, Union

T = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any,
                     default: Union[T, None]) -> Union[Any, T]:
    """More involved type annotations."""
    if key in dct:
        return dct[key]
    return default
