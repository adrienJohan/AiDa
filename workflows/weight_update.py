from agents.weight_agent import extract_weight_update

from memory.memory import save_weight_log, update_profile

from core.session import get_profile_id, set_mode


def handle_weight_update(user_message, session): 
    result = extract_weight_update(user_message)

    if not result["valid"]: 
        return (
            "I couldn't determine "
            "your weight."
        )
    
    profile_id = get_profile_id(session)

    save_weight_log(profile_id, result["weight"])

    update_profile(profile_id, {"weight": result["weight"]})

    set_mode(session,"assistant")

    return (
        f"Weight logged successfully.\n\n"
        f"Current weight: "
        f"{result['weight']} kg"
    )