def get_missing_nutrition_info(profile):

    required_fields = [
        "goal",
        "nutrition_preferences"
    ]

    missing = []

    for field in required_fields:

        value = profile.get(field)

        if value is None or value == "":
            missing.append(field)

    return missing


def get_nutrition_question(field):

    questions = {
        "goal":
            "What is your primary fitness goal?",

        "nutrition_preferences":
            "Do you have any dietary preferences or restrictions?"
    }

    return questions.get(
        field,
        "Can you tell me more?"
    )