from config.settings import MAX_TURNS

def should_stop(session):
    if session["completed"]:
        return True

    if any(session["extracted"].values()):
        return True

    if session["turns"] >= MAX_TURNS:
        return True

    return False
