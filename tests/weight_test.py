from agents.weight_agent import (
    extract_weight_update
)

tests = [

    "I weigh 87kg",

    "My weight is 86.5 kg",

    "I'm down to 85kg",

    "Hello",

    "Create a workout plan"
]

for test in tests:

    print()
    print("INPUT:")
    print(test)

    print()

    result = extract_weight_update(
        test
    )

    print(result)