import time

_requests = {}

WINDOW = 10       # seconds
MAX_REQUESTS = 5  # per window


def rate_limit(client_id: str):

    now = time.time()

    history = _requests.get(client_id, [])

    # keep recent requests
    history = [t for t in history if now - t < WINDOW]

    if len(history) >= MAX_REQUESTS:
        return False

    history.append(now)
    _requests[client_id] = history

    return True
