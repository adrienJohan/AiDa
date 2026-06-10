from agents.image_meal_agent import analyze_meal_image

from memory.memory import ( save_meals, get_meals)


analysis = analyze_meal_image(
    "test_meal.jpeg"
)

print()

print("ANALYSIS")
print(analysis)

save_meals(
    1,
    analysis["description"],
    analysis["calories"],
    analysis["protein"],
    analysis["meal_type"],
    analysis["date"]
)

print()

print("MEALS")

for meal in get_meals(1):

    print(meal)