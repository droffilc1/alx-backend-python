#!/usr/bin/env python3
""" 0-basic_async_syntax.py """

import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """An asynchronous coroutine that takes in an integer argument (max_delay,
    with a default value of 10) named wait_random that waits for a random delay
    between 0 and max_delay (included and float value) seconds and eventually returns it.
    """
    # Generate a random delay between 0 and max_delay
    delay = random.uniform(0, max_delay)

    # Use asyncio.sleep to introduce asynchronous delay
    await asyncio.sleep(delay)

    # Return the random delay value after waiting
    return delay
