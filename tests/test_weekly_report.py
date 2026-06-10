

from core.session import create_session
from agents.orchestrator import process_message

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

    print()
    print("-" * 60)