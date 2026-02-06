def decide(liveness, duplicate):

    if not liveness:
        return {"status": "rejected", "reason": "spoof suspected"}

    if duplicate:
        return {"status": "rejected", "reason": "duplicate identity"}

    return {"status": "approved"}