from fastapi_limiter.depends import RateLimiter
from fastapi_limiter import FastAPILimiter
from app.config import settings

# Parse the rate limit setting from the configuration
try:
    rate_limit_parts = settings.RATE_LIMIT.split("/")
    request_limit = int(rate_limit_parts[0])  # Number of requests allowed
    time_window = int(rate_limit_parts[1])  # Time window in seconds
except (AttributeError, IndexError, ValueError) as e:
    raise ValueError("Invalid RATE_LIMIT configuration. Expected format '<requests>/<seconds>'") from e

# Initialize RateLimiter with parsed values
rate_limiter = RateLimiter(times=request_limit, seconds=time_window)

# Initialize FastAPILimiter
async def init_rate_limiter(redis_url: str):
    """
    Initialize the FastAPILimiter with a Redis backend.

    Args:
        redis_url (str): Redis connection URL.
    """
    try:
        await FastAPILimiter.init(redis_url)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize rate limiter: {e}")