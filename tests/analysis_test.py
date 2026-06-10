from core.session import create_session
from agents.orchestrator import process_message

from memory.memory import (
    get_meals,
    get_workout_sessions
)

session = create_session()

print("AiDa started.")
print("Type 'exit' to quit.")
print()

while True:

    user_message = input("You: ")

    if user_message.lower() in [
        "exit",
        "quit"
    ]:
        break

    response = process_message(
        user_message,
        session
    )

    print()
    print("AiDa:")
    print(response)

    print()
    print("SESSION:")
    print(session)

    print("-" * 60)

print()

profile_id = session.get(
    "profile_id"
)

if profile_id is not None:

    print()
    print("MEALS")
    print("=" * 60)

    meals = get_meals(
        profile_id
    )

    for meal in meals:

        print(meal)

    print()
    print("WORKOUT SESSIONS")
    print("=" * 60)

    workouts = get_workout_sessions(
        profile_id
    )

    for workout in workouts:

        print(workout)