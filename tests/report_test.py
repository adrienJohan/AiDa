from memory.memory import (
    get_profile,
    get_workout_sessions,
    get_meals,
    get_weight_logs
)

from agents.weekly_report_agent import (
    generate_weekly_report
)

profile_id = 1

profile = get_profile(
    profile_id
)

workouts = get_workout_sessions(
    profile_id
)

meals = get_meals(
    profile_id
)

weights = get_weight_logs(
    profile_id
)

report = generate_weekly_report(
    profile,
    workouts,
    meals,
    weights
)

print(report)