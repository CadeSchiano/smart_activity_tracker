"""Small in-process rate limiter.

Use an edge/load-balancer limiter as well when deploying multiple application
instances, since process-local state is not shared between instances.
"""

from collections import defaultdict, deque
from threading import Lock
from time import monotonic

from fastapi import HTTPException, status

_attempts = defaultdict(deque)
_lock = Lock()


def enforce_rate_limit(scope: str, key: str, *, limit: int, window_seconds: int) -> None:
    """Raise 429 when ``key`` exceeds its fixed rolling-window allowance."""
    now = monotonic()
    bucket_key = (scope, key)

    with _lock:
        attempts = _attempts[bucket_key]
        cutoff = now - window_seconds
        while attempts and attempts[0] <= cutoff:
            attempts.popleft()

        if len(attempts) >= limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later.",
            )

        attempts.append(now)
