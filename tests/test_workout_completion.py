from core.session import create_session
from agents.orchestrator import process_message

from memory.memory import (
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

    profile_id = session.get(
        "profile_id"
    )

    if profile_id is not None:

        print()
        print("WORKOUT SESSIONS:")

        sessions = get_workout_sessions(
            profile_id
        )

        for workout in sessions:

            print(workout)

    print()
    print("-" * 60)

print()
print("Test finished.")