def create_session():
    return {
        "mode": "onboarding",
        "waiting_for": None,
        "profile_id": None,

        "pending_intent": None
    }


def get_mode(session):
    return session["mode"]


def set_mode(session, mode):
    session["mode"] = mode


def get_waiting_for(session):
    return session["waiting_for"]


def set_waiting_for(session, field):
    session["waiting_for"] = field


def clear_waiting_for(session):
    session["waiting_for"] = None


def get_profile_id(session):
    return session["profile_id"]


def set_profile_id(session, profile_id):
    session["profile_id"] = profile_id


def get_pending_intent( session ): 
    return session.get("pending_intent")

def set_pending_intent( session, intent):
    session["pending_intent"] = intent

def clear_pending_intent( session ): 
    session["pending_intent"] = None