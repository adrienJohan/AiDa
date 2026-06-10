def format_workout_sessions( sessions ):

    text = ""

    for session in sessions:

        text += f"""
Day: {session[3]}
Workout: {session[4]}
Status: {session[6]}

"""

    return text


def format_meals(meals): 

    text = ""

    for meal in meals: 

        text += f"""
            Meal Type: {meal[5]}
            Description: {meal[2]}
            Calories: {meal[3]}
            Protein: {meal[4]}
            Date: {meal[6]}

        """

    return text