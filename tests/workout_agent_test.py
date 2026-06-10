from agents.workout_agent import generate_workout



profile = {
    "age": 22,
    "weight": 78,
    "height": 180,
    "goal": "lose fat",
    "workout_equipment": "adjustable dumbbells and bench",
    "health_notes": "No known limitations",
    "workout_preferences": "4 training days per week"
}

result = generate_workout(profile)

print("\nRESULT:")
print(result)

print("\nTYPE:")
print(type(result))

print("\nDISPLAY TEXT:")
print(result["display_text"])

print("\nSESSIONS:")
print("=" * 50)

for session in result["week_plan"]:

    print()

    print("DAY:", session["day"])

    print(
        "WORKOUT:",
        session["workout_name"]
    )

    print(
        "DETAILS:",
        session["workout_details"]
    )