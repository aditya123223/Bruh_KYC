import json
import os
import time

LOG_FILE = "attempt_log.json"


def log_attempt(data):

    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        **data
    }

    logs = []

    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except:
            logs = []

    logs.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)
