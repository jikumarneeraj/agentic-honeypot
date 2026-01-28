sessions = {}

def get_session(session_id):
    if session_id not in sessions:
        sessions[session_id] = {
            "turns": 0,
            "start_time": None,
            "history": [],
            "completed": False,
            "extracted": {
                "bankAccounts": [],
                "upiIds": [],
                "phishingLinks": [],
                "phoneNumbers": [],
                "suspiciousKeywords": []
            }
        }
    return sessions[session_id]
