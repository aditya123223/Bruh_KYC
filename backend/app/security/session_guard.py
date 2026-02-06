import time
import secrets

_sessions = {}

SESSION_TTL = 300
MAX_SESSIONS = 200


def cleanup_sessions():
    now = time.time()

    expired = [
        token for token, t in _sessions.items()
        if now - t > SESSION_TTL
    ]

    for token in expired:
        del _sessions[token]


def create_session():

    cleanup_sessions()

    # anti-spam guard
    if len(_sessions) >= MAX_SESSIONS:
        raise Exception("Too many active sessions")

    token = secrets.token_hex(16)
    _sessions[token] = time.time()

    return token


def validate_session(token):

    cleanup_sessions()

    if token not in _sessions:
        return False

    return True

