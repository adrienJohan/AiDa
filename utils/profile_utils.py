def get_missing_fields(profile):

    required_fields = [
        "name",
        "age",
        "weight",
        "height",
        "goal"
    ]

    missing = []

    for field in required_fields:

        value = profile.get(field)

        if value is None or value == "":
            missing.append(field)

    return missing

def get_question(field):

    questions = {
        "name": "What is your name?",
        "age": "How old are you?",
        "weight": "What is your current weight?",
        "height": "What is your height?",
        "goal": "What is your primary fitness goal?"
    }

    return questions.get(
        field,
        "Can you tell me more?"
    )