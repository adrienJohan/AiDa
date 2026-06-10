def get_missing_workout_info(profile):

    required_fields = [
        "goal",
        "workout_equipment",
        "workout_preferences",
        "health_notes"
    ]

    missing = []

    for field in required_fields:

        value = profile.get(field)

        if value is None or value == "":
            missing.append(field)

    return missing

def get_workout_question(field):

    questions = {
        "goal": "What is your primary fitness goal?",
        "workout_equipment": "What workout equipment do you have access to?",
        "workout_preferences": "What types of workouts do you enjoy or prefer?",
        "health_notes": "Do you have any health conditions or injuries I should be aware of?"
    }

    return questions.get(
        field,
        "Can you tell me more about your workout preferences and goals?"
    )