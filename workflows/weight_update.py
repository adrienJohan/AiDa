from agents.weight_agent import extract_weight_update

from memory.memory import save_weight_log, update_profile

from core.session import get_profile_id, set_mode

from agents.response_agent import humanize_response


def handle_weight_update(user_message, session): 
    result = extract_weight_update(user_message)

    if not result["valid"]: 
        return humanize_response(
            "The user tried to update their weight but the message was unclear. Ask them to provide their current weight in kg.",
        )
    
    profile_id = get_profile_id(session)

    save_weight_log(profile_id, result["weight"])

    update_profile(profile_id, {"weight": result["weight"]})

    set_mode(session,"assistant")

    return humanize_response(
        "The user just updated their weight. Confirm the new weight has been logged and offer brief encouragement.",
        {"new_weight": f"{result['weight']} kg"},
    )