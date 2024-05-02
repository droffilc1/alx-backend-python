#!/usr/bin/env python3
""" 6-sum_mixed_list """
from typing import Union, List


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """Type-annotated function which takes a list of integers and floats
    Returns their sum as a float.
    """
    return float(sum(mxd_lst))
