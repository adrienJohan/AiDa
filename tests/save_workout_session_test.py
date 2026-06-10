from memory.memory import save_workout_session, get_workout_sessions, save_workout_plan

week_plan = [
    {
        "day": "Monday",
        "workout_name": "Upper Body",
        "workout_details": "Pushups"
    },
    {
        "day": "Wednesday",
        "workout_name": "Cardio",
        "workout_details": "Running"
    }
]

save_workout_plan(
    7,
    week_plan
)

print(
    get_workout_sessions(7)
)