import sqlite3
from datetime import datetime, date as date_class


def save_profile(profile) :
    conn = sqlite3.connect("data/aida.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO profiles (name, age, weight, height, goal, workout_equipment, workout_preferences, nutrition_preferences,health_notes, aida_notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        profile['name'],
        profile['age'],
        profile['weight'],
        profile['height'],
        profile['goal'],
        profile['workout_equipment'],
        profile['workout_preferences'], 
        profile['nutrition_preferences'],
        profile['health_notes'],
        profile['aida_notes']
    ))

    id = cursor.lastrowid

    conn.commit()
    conn.close()

    return id

def get_profile(profile_id) : 
    conn = sqlite3.connect("data/aida.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM profiles WHERE id = ?
    """, (profile_id,))

    profile = cursor.fetchone()
    conn.close()

    if profile:
        return {
            'id': profile[0],
            'name': profile[1],
            'age': profile[2],
            'weight': profile[3],
            'height': profile[4],
            'goal': profile[5],
            'workout_equipment': profile[6],
            'workout_preferences': profile[7], 
            'nutrition_preferences': profile[8],
            'health_notes': profile[9],
            'aida_notes': profile[10]
        }
    else:
        return None



def update_profile(profile_id, new_data):

    current_profile = get_profile(profile_id)

    if current_profile is None:
        return False

    merged_profile = current_profile.copy()

    for key, value in new_data.items():

        if key == "id":
            continue

        if value is not None and key != "aida_notes":
            merged_profile[key] = value
        
        elif value is not None and key == "aida_notes":
            if merged_profile["aida_notes"]:
                merged_profile["aida_notes"] += " " + value
            else:
                merged_profile["aida_notes"] = value

    conn = sqlite3.connect("data/aida.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE profiles
        SET
            name = ?,
            age = ?,
            weight = ?,
            height = ?,
            goal = ?,
            workout_equipment = ?,
            workout_preferences = ?,
            nutrition_preferences = ?,
            health_notes = ?,
            aida_notes = ?
        WHERE id = ?
    """, (
        merged_profile["name"],
        merged_profile["age"],
        merged_profile["weight"],
        merged_profile["height"],
        merged_profile["goal"],
        merged_profile["workout_equipment"],
        merged_profile["workout_preferences"],
        merged_profile["nutrition_preferences"],
        merged_profile["health_notes"],
        merged_profile["aida_notes"],
        profile_id
    ))

    conn.commit()
    conn.close()

    return True


def save_conversation(user_id, user_message, ai_response):

    conn = sqlite3.connect(
        "data/aida.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO conversations
        (
            user_id,
            user_message,
            ai_response,
            timestamp
        )
        VALUES (?, ?, ?, ?)
    """, (
        user_id,
        user_message,
        ai_response,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()

def get_recent_conversations( user_id, limit=10):

    conn = sqlite3.connect(
        "data/aida.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            user_message,
            ai_response
        FROM conversations
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (
        user_id,
        limit
    ))

    rows = cursor.fetchall()

    conn.close()

    return rows[::-1]


def save_workouts (user_id, workout, completed=0, date=None): 
    if date is None: 
        date = datetime.now().date().isoformat()

    conn = sqlite3.connect("data/aida.db")

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO workouts
        (
            user_id,
            workout,
            completed,
            date
        )
        VALUES (?, ?, ?, ?)
    """, (
        user_id,
        workout,
        completed,
        date
    ))

    conn.commit()
    conn.close()

def get_workouts(user_id): 
    conn = sqlite3.connect("data/aida.db")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM workouts WHERE user_id = ?
    """, (user_id,))


    workouts = cursor.fetchall()

    conn.close()


    return workouts


def save_meals( user_id, description, calories, protein, meal_type="unknown", date=None): 
    if date is None: 
        date = date_class.today().isoformat()

    conn = sqlite3.connect("data/aida.db")

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO meals
        (
            user_id, 
            description, 
            calories, 
            protein, 
            meal_type,
            date
        )
        VALUES (?, ?, ?, ?, ?,?)

    """, (
        user_id, 
        description, 
        calories, 
        protein, 
        meal_type,
        date
    ))

    conn.commit()
    conn.close()

def get_meals(user_id): 
    conn = sqlite3.connect("data/aida.db")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * 
        FROM meals
        WHERE user_id = ?
    """, (user_id,))

    meals = cursor.fetchall()

    conn.close()

    return meals


def save_workout_session (user_id, week_start, day, workout_name, workout_details, status="planned"):
    conn = sqlite3.connect("data/aida.db")

    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO workout_sessions
        (
            user_id,
            week_start,
            day,
            workout_name,
            workout_details,
            status           
        )
        VALUES (?,?,?,?,?,?)
    """, (user_id,week_start,day,workout_name,workout_details,status))


    conn.commit()
    conn.close()

def get_workout_sessions(user_id): 
    conn = sqlite3.connect("data/aida.db")

    cursor = conn.cursor()


    cursor.execute("""
    
        SELECT * 
        FROM workout_sessions
        WHERE user_id = ?
        ORDER BY week_start

    """, (user_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows


def save_workout_plan (user_id, week_plan): 
    week_start = date_class.today().isoformat()

    for session in week_plan: 
        save_workout_session(
            user_id=user_id,
            week_start=week_start,
            day=session["day"],
            workout_name=session["workout_name"],
            workout_details=session["workout_details"]            
        )


def mark_workout_session_completed( user_id,day ):

    conn = sqlite3.connect(
        "data/aida.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE workout_sessions
        SET status = 'completed'
        WHERE user_id = ?
        AND day = ?
        AND status = 'planned'
    """, (
        user_id,
        day
    ))

    conn.commit()

    updated = cursor.rowcount

    conn.close()

    return updated


def get_today_name(): 
    return datetime.now().strftime("%A")



def save_weight_log( user_id, weight, log_date=None): 
    if log_date is None: 

        log_date = date_class.today().isoformat()

    conn = sqlite3.connect("data/aida.db")

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO weight_logs(
            user_id,
            weight,
            date           
        )
        VALUES (?, ?, ?)

    """, (
        user_id, 
        weight, 
        log_date
    ))

    conn.commit()
    conn.close()


def get_weight_logs(user_id): 
    conn = sqlite3.connect("data/aida.db")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * 
        FROM weight_logs
        WHERE user_id = ?
        ORDER BY date

    """, (user_id,))

    rows = cursor.fetchall()
    
    conn.close()

    return rows
