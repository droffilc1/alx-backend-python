#!/usr/bin/env python3

""" 2-measure_runtime """


import asyncio
import time
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """Executes async_comprehension four times in parallel using
    asyncio.gather.
    Measures the total runtime and return it
    """
    start_time = time.time()
    await asyncio.gather(async_comprehension(),
                         async_comprehension(),
                         async_comprehension(),
                         async_comprehension())
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time
