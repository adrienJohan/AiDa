import sqlite3

def init_db(): 
    conn = sqlite3.connect("data/aida.db")

    cursor = conn.cursor()

    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            weight REAL,
            height REAL,
            goal TEXT,
            workout_equipment TEXT,
            workout_preferences TEXT,
            nutrition_preferences TEXT,
            health_notes TEXT,
            aida_notes TEXT
        )
    """)

    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            description TEXT,
            calories REAL,
            protein REAL,
            meal_type TEXT DEFAULT 'unknown',
            date TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            workout TEXT,
            completed INTEGER,
            date TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            user_message TEXT,
            ai_response TEXT,
            timestamp TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workout_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            week_start TEXT NOT NULL,
            day TEXT NOT NULL, 
            workout_name TEXT NOT NULL,
            workout_details TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'planned'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weight_logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            weight REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

