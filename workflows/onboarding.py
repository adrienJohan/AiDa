from memory.memory import (
    save_profile,
    get_profile,
    update_profile,
    save_weight_log
)

from utils.profile_utils import (
    get_missing_fields,
    get_question
)

from core.session import (
    get_profile_id,
    set_profile_id,
    set_mode,
    set_waiting_for,
    clear_waiting_for,
)

from agents.profile_agent import profile_agent
from agents.response_agent import humanize_response


def handle_onboarding(user_message, session): 

    profile_data = profile_agent(user_message)

    profile_id = get_profile_id(session)

    #
    # First interaction
    #

    if profile_id is None:

        profile_id = save_profile(profile_data)

        set_profile_id(
            session,
            profile_id
        )

    #
    # Existing profile
    #

    else:

        update_profile(
            profile_id,
            profile_data
        )

    #
    # Retrieve latest profile
    #

    profile = get_profile(profile_id)

    #
    # Check onboarding completion
    #

    missing_fields = get_missing_fields(profile)

    #
    # Still missing information
    #

    if missing_fields:

        next_field = missing_fields[0]

        set_waiting_for(
            session,
            next_field
        )

        return humanize_response(
            "AiDa needs to ask the user a question to complete their profile, but should not include sentences such as: To build an accurate plan for you...",
            {
                "field": next_field.replace('_', ' '),
                "original_question": get_question(next_field),
                "user_name": profile['name'] or "unknown",
            },
        )

    #
    # Onboarding complete
    #

    clear_waiting_for(session)

    save_weight_log(
        profile_id,
        profile_data["weight"]
    )

    set_mode(
        session,
        "assistant"
    )

    return humanize_response(
        "The user just finished setting up their profile. Welcome them warmly and ask how you can help them get started.",
        {"user_name": profile['name']},
    )