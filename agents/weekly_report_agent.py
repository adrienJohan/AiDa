from google import genai

from utils.analysis_utils import (
    format_workout_sessions, 
    format_meals
)

from dotenv import load_dotenv

load_dotenv()


def generate_weekly_report( profile, workout_sessions, meals, weight_logs): 

    client = genai.Client()


    formatted_workouts = format_workout_sessions(workout_sessions)

    formatted_meals = format_meals(meals)
    

    prompt = f"""
        You are AiDa's weekly fitness analyst. 

        Generate a professional weekly progress report.

        USER PROFILE

        Name: {profile['name']}
        Age: {profile['age']}
        Goal: {profile['goal']}

        CURRENT DATAS: 

        workout_sessions: {formatted_workouts}
        meals: {formatted_meals}
        weight logs: {weight_logs}

        create a report with the following sections: 

        1- weekly progress overview
        2- weight evolution
        3- workout performance
        4- nutrition summary
        5- key strengths
        6- areas for improvement
        7- recommendations

        Be specific and actionable
        Do not simply repeat teh raw data
    """


    response = client.models.generate_content(
        model="gemma-4-26b-a4b-it",
        contents=prompt
    )

    return response.text