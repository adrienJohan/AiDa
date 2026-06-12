from database.db import init_db
from core.session import create_session
from agents.orchestrator import process_message

from memory.memory import (
    get_workout_sessions
)

init_db()

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
    print("WORKOUT SESSIONS")
    print("=" * 60)

    sessions = get_workout_sessions(
        profile_id
    )

    for session_data in sessions:

        print(session_data)

else:

    print(
        "No profile found."
    )