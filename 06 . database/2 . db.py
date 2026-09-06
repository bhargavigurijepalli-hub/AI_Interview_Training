import sqlite3
from pathlib import Path


# =========================================================
# DATABASE PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "ai_interview.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    return connection


# =========================================================
# CREATE TABLES
# =========================================================

def create_tables():

    connection = get_connection()

    cursor = connection.cursor()

    # -----------------------------------------------------
    # USERS TABLE
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            email TEXT UNIQUE NOT NULL,

            password_hash TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # -----------------------------------------------------
    # STUDENT PROFILE TABLE
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_profiles (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            full_name TEXT,

            age INTEGER,

            gender TEXT,

            phone TEXT,

            prep_days INTEGER,

            college TEXT,

            degree TEXT,

            stream TEXT,

            cgpa REAL,

            skills TEXT,

            experience TEXT,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
        )
    """)

    # -----------------------------------------------------
    # INTERVIEW ANSWERS TABLE
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_answers (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            round_number INTEGER NOT NULL,

            level INTEGER NOT NULL,

            question TEXT NOT NULL,

            answer TEXT NOT NULL,

            score INTEGER DEFAULT 0,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
        )
    """)

    connection.commit()

    connection.close()


# =========================================================
# USER FUNCTIONS
# =========================================================

def create_user(email, password_hash):

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users
            (email, password_hash)

            VALUES (?, ?)
            """,
            (
                email,
                password_hash
            )
        )

        connection.commit()

        return cursor.lastrowid

    except sqlite3.IntegrityError:

        return None

    finally:

        connection.close()


def get_user_by_email(email):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    user = cursor.fetchone()

    connection.close()

    return user


# =========================================================
# PROFILE FUNCTIONS
# =========================================================

def save_student_profile(
    user_id,
    full_name,
    age,
    gender,
    phone,
    prep_days,
    college,
    degree,
    stream,
    cgpa,
    skills,
    experience
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO student_profiles
        (
            user_id,
            full_name,
            age,
            gender,
            phone,
            prep_days,
            college,
            degree,
            stream,
            cgpa,
            skills,
            experience
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            full_name,
            age,
            gender,
            phone,
            prep_days,
            college,
            degree,
            stream,
            cgpa,
            skills,
            experience
        )
    )

    connection.commit()

    connection.close()


# =========================================================
# INTERVIEW ANSWER FUNCTIONS
# =========================================================

def save_interview_answer(
    user_id,
    round_number,
    level,
    question,
    answer,
    score
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO interview_answers
        (
            user_id,
            round_number,
            level,
            question,
            answer,
            score
        )

        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            round_number,
            level,
            question,
            answer,
            score
        )
    )

    connection.commit()

    connection.close()


# =========================================================
# INITIALIZE DATABASE
# =========================================================

if __name__ == "__main__":

    create_tables()

    print("Database initialized successfully.")

    print(f"Database location: {DB_PATH}")