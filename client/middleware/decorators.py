import time
import logging
from functools import wraps

logging.basicConfig(level=logging.INFO)


def log_execution_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        duration = time.time() - start
        logging.info(f"{func.__name__} executed in {duration:.2f}s")
        return result

    return wrapper


def retry_on_failure(retries=3):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    logging.warning(f"Attempt {attempt} failed: {e}")
                    if attempt == retries:
                        logging.error(f"All {retries} attempts failed.")
                        raise

        return wrapper

    return decorator
