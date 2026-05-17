"""
Utility decorators used across the project.
"""

import asyncio
import time
from functools import wraps


def timed(func):
    """
    Measure execution time of async functions.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):

        start_time = time.time()

        try:
            result = await func(*args, **kwargs)

            elapsed = time.time() - start_time

            print(f"[TIME] {func.__name__} executed in {elapsed:.2f}s")

            return result

        except Exception as e:

            elapsed = time.time() - start_time

            print(
                f"[ERROR] {func.__name__} failed after {elapsed:.2f}s: {e}"
            )

            raise

    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0):
    """
    Retry failed async functions automatically.
    """

    def decorator(func):

        @wraps(func)
        async def wrapper(*args, **kwargs):

            last_exception = None

            for attempt in range(1, max_attempts + 1):

                try:
                    return await func(*args, **kwargs)

                except Exception as e:

                    last_exception = e

                    if attempt < max_attempts:

                        print(
                            f"[RETRY] Attempt "
                            f"{attempt}/{max_attempts} failed."
                        )

                        await asyncio.sleep(delay)

                    else:
                        print(
                            f"[FAILED] {func.__name__} "
                            f"failed after retries."
                        )

            raise last_exception

        return wrapper

    return decorator