def decide(live, duplicate):

    if not live:
        return {"status": "rejected", "reason": "liveness failed"}

    if duplicate:
        return {"status": "rejected", "reason": "duplicate identity"}

    return {"status": "approved"}
