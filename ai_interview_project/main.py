from pathlib import Path
import json
import random
import secrets
import os
import re
import sqlite3
import hashlib
import hmac
from datetime import datetime

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware


# =========================================================
# APPLICATION
# =========================================================

app = FastAPI(title="SmartPrep AI")


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATE_DIR = BASE_DIR / "04 . templates"
DATA_DIR = TEMPLATE_DIR / "07 . sevices" / "08 . data"

QUESTION_FILE = DATA_DIR / "1 . question.json"
CODING_QUESTION_FILE = DATA_DIR / "2 . coding_questions.json"
ANSWERS_FILE = DATA_DIR / "3 . answers.json"

LOGIN_TEMPLATE = TEMPLATE_DIR / "1 . login.html"
PERSONAL_TEMPLATE = TEMPLATE_DIR / "2 . personal.html"
EDUCATION_TEMPLATE = TEMPLATE_DIR / "3 . educational.html"
SKILLS_TEMPLATE = TEMPLATE_DIR / "4 . skills.html"

DB_PATH = BASE_DIR / "smartprep_users.db"


# =========================================================
# SESSION MIDDLEWARE
# =========================================================

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv(
        "SESSION_SECRET",
        "smartprep-ai-local-development-secret"
    ),
    same_site="lax",
    https_only=False
)


# =========================================================
# PREVENT BROWSER / PROXY CACHE
# =========================================================

@app.middleware("http")
async def prevent_cache(request, call_next):

    response = await call_next(request)

    response.headers["Cache-Control"] = (
        "no-store, no-cache, must-revalidate, max-age=0, private"
    )

    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers["Vary"] = "Cookie"

    return response


# =========================================================
# SETTINGS
# =========================================================

LEVELS = [
    "Intermediate",
    "Medium",
    "Advanced"
]

LANGUAGES = [
    "C",
    "Java",
    "Python",
    "SQL",
    "Web Development"
]

ROUND_COUNTS = {
    "aptitude": 10,
    "technical": 10,
    "coding": 5,
    "hr": 10
}


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db():

    connection = sqlite3.connect(
        DB_PATH,
        timeout=30
    )

    connection.row_factory = sqlite3.Row

    return connection


# =========================================================
# CREATE DATABASE
# =========================================================

def create_database():

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with get_db() as db:

        db.execute("""
            CREATE TABLE IF NOT EXISTS users (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                email TEXT UNIQUE NOT NULL,

                password_hash TEXT NOT NULL,

                name TEXT DEFAULT '',

                age TEXT DEFAULT '',

                gender TEXT DEFAULT '',

                phone TEXT DEFAULT '',

                college TEXT DEFAULT '',

                degree TEXT DEFAULT '',

                branch TEXT DEFAULT '',

                graduation_year TEXT DEFAULT '',

                skills TEXT DEFAULT '',

                experience TEXT DEFAULT '',

                level TEXT DEFAULT 'Intermediate',

                programming_language TEXT DEFAULT 'Python',

                aptitude_score INTEGER DEFAULT 0,

                technical_score INTEGER DEFAULT 0,

                coding_score INTEGER DEFAULT 0,

                hr_score INTEGER DEFAULT 0,

                total_score INTEGER DEFAULT 0,

                aptitude_exam TEXT DEFAULT '[]',

                technical_exam TEXT DEFAULT '[]',

                coding_exam TEXT DEFAULT '[]',

                hr_exam TEXT DEFAULT '[]',

                coding_result TEXT DEFAULT '[]',

                created_at TEXT NOT NULL
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS sessions (

                session_id TEXT PRIMARY KEY,

                user_id INTEGER NOT NULL,

                created_at TEXT NOT NULL,

                FOREIGN KEY(user_id)
                REFERENCES users(id)
            )
        """)

        db.commit()


create_database()


# =========================================================
# DATABASE MIGRATION
# =========================================================

def upgrade_database():

    required_columns = [

        ("phone", "TEXT DEFAULT ''"),

        ("name", "TEXT DEFAULT ''"),

        ("age", "TEXT DEFAULT ''"),

        ("gender", "TEXT DEFAULT ''"),

        ("college", "TEXT DEFAULT ''"),

        ("degree", "TEXT DEFAULT ''"),

        ("branch", "TEXT DEFAULT ''"),

        ("graduation_year", "TEXT DEFAULT ''"),

        ("skills", "TEXT DEFAULT ''"),

        ("experience", "TEXT DEFAULT ''"),

        ("level", "TEXT DEFAULT 'Intermediate'"),

        (
            "programming_language",
            "TEXT DEFAULT 'Python'"
        ),

        (
            "aptitude_score",
            "INTEGER DEFAULT 0"
        ),

        (
            "technical_score",
            "INTEGER DEFAULT 0"
        ),

        (
            "coding_score",
            "INTEGER DEFAULT 0"
        ),

        (
            "hr_score",
            "INTEGER DEFAULT 0"
        ),

        (
            "total_score",
            "INTEGER DEFAULT 0"
        ),

        (
            "aptitude_exam",
            "TEXT DEFAULT '[]'"
        ),

        (
            "technical_exam",
            "TEXT DEFAULT '[]'"
        ),

        (
            "coding_exam",
            "TEXT DEFAULT '[]'"
        ),

        (
            "hr_exam",
            "TEXT DEFAULT '[]'"
        ),

        (
            "coding_result",
            "TEXT DEFAULT '[]'"
        )
    ]

    with get_db() as db:

        existing_columns = {

            row["name"]

            for row in db.execute(
                "PRAGMA table_info(users)"
            ).fetchall()
        }

        for column_name, column_definition in required_columns:

            if column_name not in existing_columns:

                print(
                    f"Adding missing database column: {column_name}"
                )

                db.execute(
                    f"""
                    ALTER TABLE users
                    ADD COLUMN {column_name}
                    {column_definition}
                    """
                )

        db.commit()


upgrade_database()


# =========================================================
# PASSWORD HASHING
# =========================================================

def hash_password(password):

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200000
    )

    return (
        salt.hex()
        + ":"
        + password_hash.hex()
    )


# =========================================================
# PASSWORD VERIFICATION
# =========================================================

def verify_password(
    password,
    stored_hash
):

    try:

        salt_hex, hash_hex = (
            stored_hash.split(":", 1)
        )

        salt = bytes.fromhex(
            salt_hex
        )

        expected = bytes.fromhex(
            hash_hex
        )

        actual = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            200000
        )

        return hmac.compare_digest(
            actual,
            expected
        )

    except Exception:

        return False


# =========================================================
# DEFAULT USER DATA
# =========================================================

def create_user_data():

    return {

        "email": "",

        "logged_in": True,

        "name": "",

        "age": "",

        "gender": "",

        "phone": "",

        "college": "",

        "degree": "",

        "branch": "",

        "graduation_year": "",

        "skills": "",

        "experience": "",

        "level": "Intermediate",

        "programming_language": "Python",

        "aptitude_score": 0,

        "technical_score": 0,

        "coding_score": 0,

        "hr_score": 0,

        "total_score": 0,

        "aptitude_exam": [],

        "technical_exam": [],

        "coding_exam": [],

        "hr_exam": [],

        "coding_result": []
    }


# =========================================================
# DATABASE ROW -> USER DATA
# =========================================================

def row_to_user_data(row):

    try:

        aptitude_exam = json.loads(
            row["aptitude_exam"] or "[]"
        )

    except Exception:

        aptitude_exam = []

    try:

        technical_exam = json.loads(
            row["technical_exam"] or "[]"
        )

    except Exception:

        technical_exam = []

    try:

        coding_exam = json.loads(
            row["coding_exam"] or "[]"
        )

    except Exception:

        coding_exam = []

    try:

        hr_exam = json.loads(
            row["hr_exam"] or "[]"
        )

    except Exception:

        hr_exam = []

    try:

        coding_result = json.loads(
            row["coding_result"] or "[]"
        )

    except Exception:

        coding_result = []

    return {

        "email": row["email"],

        "logged_in": True,

        "name": row["name"] or "",

        "age": row["age"] or "",

        "gender": row["gender"] or "",

        "phone": row["phone"] or "",

        "college": row["college"] or "",

        "degree": row["degree"] or "",

        "branch": row["branch"] or "",

        "graduation_year": row["graduation_year"] or "",

        "skills": row["skills"] or "",

        "experience": row["experience"] or "",

        "level": row["level"] or "Intermediate",

        "programming_language": (
            row["programming_language"]
            or "Python"
        ),

        "aptitude_score": (
            row["aptitude_score"]
            or 0
        ),

        "technical_score": (
            row["technical_score"]
            or 0
        ),

        "coding_score": (
            row["coding_score"]
            or 0
        ),

        "hr_score": (
            row["hr_score"]
            or 0
        ),

        "total_score": (
            row["total_score"]
            or 0
        ),

        "aptitude_exam": aptitude_exam,

        "technical_exam": technical_exam,

        "coding_exam": coding_exam,

        "hr_exam": hr_exam,

        "coding_result": coding_result
    }


# =========================================================
# SAVE USER DATA
# =========================================================

def save_user_data(
    user_id,
    data
):

    with get_db() as db:

        db.execute("""
            UPDATE users
            SET

                name = ?,

                age = ?,

                gender = ?,

                phone = ?,

                college = ?,

                degree = ?,

                branch = ?,

                graduation_year = ?,

                skills = ?,

                experience = ?,

                level = ?,

                programming_language = ?,

                aptitude_score = ?,

                technical_score = ?,

                coding_score = ?,

                hr_score = ?,

                total_score = ?,

                aptitude_exam = ?,

                technical_exam = ?,

                coding_exam = ?,

                hr_exam = ?,

                coding_result = ?

            WHERE id = ?
        """, (

            data.get("name", ""),

            str(
                data.get(
                    "age",
                    ""
                )
            ),

            data.get(
                "gender",
                ""
            ),

            data.get(
                "phone",
                ""
            ),

            data.get(
                "college",
                ""
            ),

            data.get(
                "degree",
                ""
            ),

            data.get(
                "branch",
                ""
            ),

            str(
                data.get(
                    "graduation_year",
                    ""
                )
            ),

            data.get(
                "skills",
                ""
            ),

            data.get(
                "experience",
                ""
            ),

            data.get(
                "level",
                "Intermediate"
            ),

            data.get(
                "programming_language",
                "Python"
            ),

            data.get(
                "aptitude_score",
                0
            ),

            data.get(
                "technical_score",
                0
            ),

            data.get(
                "coding_score",
                0
            ),

            data.get(
                "hr_score",
                0
            ),

            data.get(
                "total_score",
                0
            ),

            json.dumps(
                data.get(
                    "aptitude_exam",
                    []
                )
            ),

            json.dumps(
                data.get(
                    "technical_exam",
                    []
                )
            ),

            json.dumps(
                data.get(
                    "coding_exam",
                    []
                )
            ),

            json.dumps(
                data.get(
                    "hr_exam",
                    []
                )
            ),

            json.dumps(
                data.get(
                    "coding_result",
                    []
                )
            ),

            user_id
        ))

        db.commit()


# =========================================================
# GET CURRENT USER
# =========================================================

def get_current_user(request):

    session_id = request.session.get(
        "session_id"
    )

    if not session_id:

        return None, None

    with get_db() as db:

        session = db.execute(
            """
            SELECT user_id
            FROM sessions
            WHERE session_id = ?
            """,
            (session_id,)
        ).fetchone()

        if not session:

            request.session.clear()

            return None, None

        user = db.execute(
            """
            SELECT *
            FROM users
            WHERE id = ?
            """,
            (session["user_id"],)
        ).fetchone()

        if not user:

            db.execute(
                """
                DELETE FROM sessions
                WHERE session_id = ?
                """,
                (session_id,)
            )

            db.commit()

            request.session.clear()

            return None, None

        return (
            session["user_id"],
            row_to_user_data(user)
        )


# =========================================================
# CREATE LOGIN SESSION
# =========================================================

def create_login_session(
    request,
    user_id
):

    session_id = secrets.token_urlsafe(48)

    with get_db() as db:

        db.execute(
            """
            INSERT INTO sessions
            (
                session_id,
                user_id,
                created_at
            )
            VALUES (?, ?, ?)
            """,
            (
                session_id,
                user_id,
                datetime.utcnow().isoformat()
            )
        )

        db.commit()

    request.session.clear()

    request.session["session_id"] = session_id


# =========================================================
# HTML ESCAPE
# =========================================================

def escape_html(value):

    if value is None:

        return ""

    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )


# =========================================================
# JSON LOADING
# =========================================================

def load_json(file_path):

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except FileNotFoundError:

        print(
            f"WARNING: File not found: {file_path}"
        )

        return {}

    except json.JSONDecodeError:

        print(
            f"WARNING: Invalid JSON: {file_path}"
        )

        return {}


# =========================================================
# HTML TEMPLATE LOADING
# =========================================================

def load_template(file_path):

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    except FileNotFoundError:

        return """
        <!DOCTYPE html>
        <html>
        <body>
            <h1>Template not found</h1>
        </body>
        </html>
        """


def render_template(
    file_path,
    error="",
    success=""
):

    content = load_template(
        file_path
    )

    error_html = ""

    if error:

        error_html = f"""
        <div class="error">
            {escape_html(error)}
        </div>
        """

    success_html = ""

    if success:

        success_html = f"""
        <div class="success">
            {escape_html(success)}
        </div>
        """

    content = content.replace(
        "<!-- ERROR_MESSAGE -->",
        error_html
    )

    content = content.replace(
        "<!-- SUCCESS_MESSAGE -->",
        success_html
    )

    content = content.replace(
        "{{ error }}",
        error_html
    )

    content = content.replace(
        "{{ success }}",
        success_html
    )

    content = content.replace(
        "{% if error %}",
        ""
    )

    content = content.replace(
        "{% endif %}",
        ""
    )

    return HTMLResponse(
        content=content
    )


# =========================================================
# EMAIL VALIDATION
# =========================================================

def valid_email(email):

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return bool(
        re.match(
            pattern,
            email
        )
    )


# =========================================================
# LEVEL MAPPING
# =========================================================

def general_level(level):

    mapping = {

        "Intermediate": "intermediate",

        "Medium": "medium",

        "Advanced": "advanced"
    }

    return mapping.get(
        level,
        "intermediate"
    )


def technical_level(level):

    return general_level(
        level
    )


def coding_level(level):

    mapping = {

        "Intermediate": "Easy",

        "Medium": "Medium",

        "Advanced": "Hard"
    }

    return mapping.get(
        level,
        "Easy"
    )


# =========================================================
# NORMALIZE DICTIONARY KEYS
# =========================================================

def normalize_level_keys(data):

    if not isinstance(
        data,
        dict
    ):

        return {}

    normalized = {}

    for key, value in data.items():

        normalized[
            str(key).strip().lower()
        ] = value

    return normalized


# =========================================================
# FIND LANGUAGE DATA
# =========================================================

def get_language_data(
    data,
    language
):

    if not isinstance(
        data,
        dict
    ):

        return {}

    if language in data:

        return data[language]

    target = str(
        language
    ).strip().lower()

    for key, value in data.items():

        if (
            str(key)
            .strip()
            .lower()
            == target
        ):

            return value

    return {}


# =========================================================
# BUILD QUESTION / ANSWER PAIRS
# =========================================================

def build_pairs(
    questions,
    answers
):

    pairs = []

    if not isinstance(
        questions,
        list
    ):

        questions = []

    if not isinstance(
        answers,
        list
    ):

        answers = []

    for index, question in enumerate(
        questions
    ):

        answer = ""

        if index < len(answers):

            answer = answers[index]

        pairs.append({

            "question": str(question),

            "answer": str(answer)
        })

    return pairs


# =========================================================
# GET LEVEL PAIRS
# =========================================================

def get_level_pairs(
    question_data,
    answer_data,
    level
):

    question_data = normalize_level_keys(
        question_data
    )

    answer_data = normalize_level_keys(
        answer_data
    )

    selected_level = general_level(
        level
    )

    questions = question_data.get(
        selected_level,
        []
    )

    answers = answer_data.get(
        selected_level,
        []
    )

    return build_pairs(
        questions,
        answers
    )


# =========================================================
# FILL RANDOM PAIRS
# =========================================================

def fill_random_pairs(
    selected_pairs,
    all_pairs,
    required_count
):

    selected_valid = [

        item

        for item in selected_pairs

        if str(
            item.get(
                "answer",
                ""
            )
        ).strip()
    ]

    all_valid = [

        item

        for item in all_pairs

        if str(
            item.get(
                "answer",
                ""
            )
        ).strip()
    ]

    random.shuffle(
        selected_valid
    )

    result = selected_valid[
        :required_count
    ]

    if len(result) >= required_count:

        return result

    used_questions = {

        item.get(
            "question",
            ""
        )

        for item in result
    }

    remaining = [

        item

        for item in all_valid

        if item.get(
            "question",
            ""
        ) not in used_questions
    ]

    random.shuffle(
        remaining
    )

    needed = (
        required_count
        - len(result)
    )

    result.extend(
        remaining[:needed]
    )

    return result


# =========================================================
# CREATE MCQ OPTIONS
# =========================================================

def create_mcq_options(
    selected_pairs,
    all_pairs
):

    all_answers = []

    for item in all_pairs:

        answer = str(
            item.get(
                "answer",
                ""
            )
        ).strip()

        if answer:

            all_answers.append(
                answer
            )

    unique_answers = list(
        dict.fromkeys(
            all_answers
        )
    )

    valid_questions = []

    for item in selected_pairs:

        correct_answer = str(
            item.get(
                "answer",
                ""
            )
        ).strip()

        if not correct_answer:

            continue

        distractors = [

            answer

            for answer in unique_answers

            if answer != correct_answer
        ]

        random.shuffle(
            distractors
        )

        options = [
            correct_answer
        ]

        options.extend(
            distractors[:3]
        )

        options = [

            str(option).strip()

            for option in options

            if str(option).strip()
        ]

        if correct_answer not in options:

            continue

        random.shuffle(
            options
        )

        correct_index = options.index(
            correct_answer
        )

        new_item = item.copy()

        new_item["options"] = options

        new_item["correct_option"] = chr(
            65 + correct_index
        )

        valid_questions.append(
            new_item
        )

    return valid_questions


# =========================================================
# APTITUDE QUESTIONS
# =========================================================

def get_aptitude_exam_questions(level):

    questions_data = load_json(
        QUESTION_FILE
    )

    answers_data = load_json(
        ANSWERS_FILE
    )

    question_section = normalize_level_keys(
        questions_data.get(
            "aptitude",
            {}
        )
    )

    answer_section = normalize_level_keys(
        answers_data.get(
            "aptitude",
            {}
        )
    )

    selected = get_level_pairs(
        question_section,
        answer_section,
        level
    )

    all_pairs = []

    for level_key in [
        "intermediate",
        "medium",
        "advanced",
        "hard"
    ]:

        all_pairs.extend(
            build_pairs(
                question_section.get(
                    level_key,
                    []
                ),
                answer_section.get(
                    level_key,
                    []
                )
            )
        )

    selected = fill_random_pairs(
        selected,
        all_pairs,
        ROUND_COUNTS["aptitude"]
    )

    return create_mcq_options(
        selected,
        all_pairs
    )


# =========================================================
# TECHNICAL QUESTIONS
# =========================================================

def get_technical_exam_questions(
    level,
    language
):

    questions_data = load_json(
        QUESTION_FILE
    )

    answers_data = load_json(
        ANSWERS_FILE
    )

    technical_questions = questions_data.get(
        "technical",
        {}
    )

    technical_answers = answers_data.get(
        "technical",
        {}
    )

    language_questions = get_language_data(
        technical_questions,
        language
    )

    language_answers = get_language_data(
        technical_answers,
        language
    )

    selected_level = technical_level(
        level
    )

    language_questions = normalize_level_keys(
        language_questions
    )

    language_answers = normalize_level_keys(
        language_answers
    )

    questions = language_questions.get(
        selected_level,
        []
    )

    answers = language_answers.get(
        selected_level,
        []
    )

    pairs = build_pairs(
        questions,
        answers
    )

    valid_pairs = [

        item

        for item in pairs

        if str(
            item.get(
                "answer",
                ""
            )
        ).strip()
    ]

    random.shuffle(
        valid_pairs
    )

    selected = valid_pairs[
        :ROUND_COUNTS["technical"]
    ]

    return create_mcq_options(
        selected,
        valid_pairs
    )


# =========================================================
# HR QUESTIONS
# =========================================================

def get_hr_exam_questions(level):

    questions_data = load_json(
        QUESTION_FILE
    )

    answers_data = load_json(
        ANSWERS_FILE
    )

    communication_questions = normalize_level_keys(
        questions_data.get(
            "communication",
            {}
        )
    )

    communication_answers = normalize_level_keys(
        answers_data.get(
            "communication",
            {}
        )
    )

    selected_level = general_level(
        level
    )

    questions = communication_questions.get(
        selected_level,
        []
    )

    answers = communication_answers.get(
        selected_level,
        []
    )

    pairs = build_pairs(
        questions,
        answers
    )

    valid_pairs = [

        item

        for item in pairs

        if str(
            item.get(
                "answer",
                ""
            )
        ).strip()
    ]

    random.shuffle(
        valid_pairs
    )

    selected = valid_pairs[
        :ROUND_COUNTS["hr"]
    ]

    return create_mcq_options(
        selected,
        valid_pairs
    )


# =========================================================
# CODING QUESTIONS
# =========================================================

def get_coding_questions(
    level,
    language
):

    data = load_json(
        CODING_QUESTION_FILE
    )

    language_data = get_language_data(
        data,
        language
    )

    language_data = normalize_level_keys(
        language_data
    )

    selected_level = coding_level(
        level
    ).lower()

    questions = language_data.get(
        selected_level,
        []
    )

    if not isinstance(
        questions,
        list
    ):

        questions = []

    questions = questions.copy()

    random.shuffle(
        questions
    )

    return questions[
        :ROUND_COUNTS["coding"]
    ]


# =========================================================
# MCQ SCORE
# =========================================================

def calculate_mcq_score(
    form,
    questions
):

    score = 0

    for index, item in enumerate(
        questions
    ):

        selected = str(
            form.get(
                f"q_{index}",
                ""
            )
        ).strip().upper()

        correct = str(
            item.get(
                "correct_option",
                ""
            )
        ).strip().upper()

        if selected == correct:

            score += 100

    return score


# =========================================================
# MCQ PAGE
# =========================================================

def mcq_page(
    title,
    subtitle,
    questions,
    submit_url,
    user_data
):

    cards = []

    for index, item in enumerate(
        questions
    ):

        question = escape_html(
            item.get(
                "question",
                ""
            )
        )

        option_html = []

        for option_index, option in enumerate(
            item.get(
                "options",
                []
            )
        ):

            letter = chr(
                65 + option_index
            )

            option_html.append(
                f"""
                <label class="option">

                    <input
                        type="radio"
                        name="q_{index}"
                        value="{letter}"
                        required
                    >

                    <span class="letter">
                        {letter}
                    </span>

                    <span class="option-text">
                        {escape_html(option)}
                    </span>

                </label>
                """
            )

        cards.append(
            f"""
            <div class="question-card">

                <div class="question-number">
                    Question {index + 1}
                </div>

                <h2>
                    {question}
                </h2>

                <div class="options">
                    {"".join(option_html)}
                </div>

            </div>
            """
        )

    if not cards:

        cards.append("""
        <div class="question-card">

            <h2>
                No questions available.
            </h2>

            <p>
                Please check your question
                and answer JSON files.
            </p>

        </div>
        """)

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <meta charset="UTF-8">

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0"
        >

        <title>
            {escape_html(title)}
        </title>

        <style>

            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f4f6f9;
                color: #222;
            }}

            .header {{
                background: #1f2937;
                color: white;
                text-align: center;
                padding: 30px 20px;
            }}

            .container {{
                width: 90%;
                max-width: 1000px;
                margin: 30px auto;
            }}

            .candidate-info,
            .question-card {{
                background: white;
                padding: 25px;
                margin-bottom: 25px;
                border-radius: 12px;
                box-shadow:
                    0 2px 8px rgba(0,0,0,0.08);
            }}

            .question-number {{
                font-weight: bold;
                color: #555;
                margin-bottom: 12px;
            }}

            .question-card h2 {{
                font-size: 20px;
                line-height: 1.5;
                margin-top: 0;
            }}

            .option {{
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 15px;
                margin: 10px 0;
                border: 1px solid #ddd;
                border-radius: 8px;
                cursor: pointer;
            }}

            .option:hover {{
                background: #eef6ff;
                border-color: #2563eb;
            }}

            .option input {{
                width: 18px;
                height: 18px;
            }}

            .letter {{
                font-weight: bold;
                width: 25px;
            }}

            .submit-container {{
                text-align: center;
                margin: 40px 0;
            }}

            .submit-button {{
                border: none;
                background: #2563eb;
                color: white;
                padding: 16px 40px;
                border-radius: 8px;
                font-size: 17px;
                font-weight: bold;
                cursor: pointer;
            }}

        </style>

    </head>

    <body>

        <div class="header">

            <h1>
                {escape_html(title)}
            </h1>

            <p>
                {escape_html(subtitle)}
            </p>

        </div>

        <div class="container">

            <div class="candidate-info">

                <strong>
                    Difficulty:
                </strong>

                {escape_html(user_data["level"])}

                <br><br>

                <strong>
                    Instructions:
                </strong>

                <br>

                Select one option for each question.

                <br>

                Correct = 100 marks.

                <br>

                Wrong = 0 marks.

            </div>

            <form
                method="post"
                action="{escape_html(submit_url)}"
            >

                {"".join(cards)}

                <div class="submit-container">

                    <button
                        type="submit"
                        class="submit-button"
                    >
                        Submit Answers
                    </button>

                </div>

            </form>

        </div>

    </body>

    </html>
    """
# =========================================================
# CODING EVALUATION HELPERS
# =========================================================

def normalize_code(code):
    """
    Normalize submitted source code for static analysis.

    IMPORTANT:
    This does NOT execute the submitted code.
    """

    code = str(code or "").lower()

    # Remove block comments.
    code = re.sub(
        r"/\*.*?\*/",
        " ",
        code,
        flags=re.DOTALL
    )

    # Remove // comments.
    code = re.sub(
        r"//.*",
        " ",
        code
    )

    # Remove Python comments, but do not destroy
    # normal code containing # inside strings.
    lines = []

    for line in code.splitlines():

        stripped = line.strip()

        if stripped.startswith("#"):

            continue

        lines.append(line)

    code = "\n".join(lines)

    # Normalize whitespace.
    code = re.sub(
        r"\s+",
        " ",
        code
    ).strip()

    return code


def contains_any(code, patterns):

    return any(
        pattern in code
        for pattern in patterns
    )


def contains_all(code, patterns):

    return all(
        pattern in code
        for pattern in patterns
    )


def code_has_loop(code):

    return contains_any(
        code,
        [
            "for ",
            "for(",
            "for(",
            "while ",
            "while("
        ]
    )


def code_has_array_or_collection(code):

    return contains_any(
        code,
        [
            "[",
            "array",
            "list",
            "vector",
            "int[]",
            "string[]",
            "arr"
        ]
    )


def code_has_function(code):

    return contains_any(
        code,
        [
            "def ",
            "function ",
            "void ",
            "int ",
            "public ",
            "static ",
            "return "
        ]
    )


def code_has_comparison(code):

    return contains_any(
        code,
        [
            ">",
            "<",
            "==",
            "!=",
            "compare",
            "compareto",
            "comparator"
        ]
    )


def code_has_output(code):

    return contains_any(
        code,
        [
            "print",
            "printf",
            "println",
            "system.out",
            "return"
        ]
    )


# =========================================================
# QUESTION TYPE DETECTION
# =========================================================

def get_question_type(question):

    q = str(
        question or ""
    ).lower()

    # Array / list problems
    if (
        "largest element in an array" in q
        or "largest element in a list" in q
    ):
        return "largest"

    if "second largest element" in q:

        return "second_largest"

    if "duplicate elements" in q:

        return "duplicates"

    # String problems
    if (
        "reverse a string" in q
        or "reverse a string entered" in q
    ):
        return "reverse_string"

    if "first non-repeating character" in q:

        return "first_non_repeating"

    if "longest substring without repeating" in q:

        return "longest_substring"

    # Prime
    if "whether a number is prime" in q:

        return "prime"

    # Linked list
    if "reverse a singly linked list" in q:

        return "reverse_linked_list"

    if "detect a cycle in a linked list" in q:

        return "cycle_linked_list"

    # Stack
    if "stack using an array" in q:

        return "stack"

    # Tree
    if "binary search tree" in q:

        return "bst"

    # Graph
    if (
        "graph traversal using bfs and dfs" in q
        or "bfs and dfs traversal" in q
    ):
        return "graph"

    # LRU
    if "lru cache" in q:

        return "lru"

    # SQL
    if "second highest salary from an employee table" in q:

        return "sql_second_highest"

    if "salary is greater than 50000" in q:

        return "sql_salary_50000"

    if "count the number of employees in each department" in q:

        return "sql_department_count"

    if "greater than the average salary of their department" in q:

        return "sql_department_average"

    if "second highest salary in each department" in q:

        return "sql_second_department"

    if "duplicate records in a table" in q:

        return "sql_duplicates"

    if "top three highest-paid employees in each department" in q:

        return "sql_top_three"

    if "highest salary difference between employees in each department" in q:

        return "sql_salary_difference"

    if "running total of employee salaries" in q:

        return "sql_running_total"

    # Web
    if "registration form" in q:

        return "web_registration"

    if "javascript to reverse a string" in q:

        return "web_reverse"

    if "responsive navigation bar" in q:

        return "web_navigation"

    if "search filter for a list of products" in q:

        return "web_search_filter"

    if "css grid or flexbox" in q:

        return "web_responsive"

    if "validate an email address and password" in q:

        return "web_validation"

    if "fetches data from a rest api" in q:

        return "web_api"

    if "debounced search box" in q:

        return "web_debounce"

    if "form validation, api integration and dynamic dom updates" in q:

        return "web_full_application"

    return "unknown"


# =========================================================
# CODING EVALUATION
# =========================================================

def evaluate_code(
    code,
    question,
    language
):

    code = str(
        code or ""
    ).strip()

    language = str(
        language or ""
    ).strip().lower()

    # -----------------------------------------------------
    # EMPTY ANSWER
    # -----------------------------------------------------

    if not code:

        return {
            "correct": False,
            "attempted": False,
            "reason": "No answer submitted.",
            "matched": 0,
            "required": 0
        }

    normalized = normalize_code(code)

    if len(normalized) < 10:

        return {
            "correct": False,
            "attempted": True,
            "reason": "The submitted answer is too short.",
            "matched": 0,
            "required": 1
        }

    question_type = get_question_type(
        question
    )

    score = 0
    required = 0
    reasons = []

    # =====================================================
    # ARRAY / LIST — LARGEST
    # =====================================================

    if question_type == "largest":

        required = 3

        if code_has_array_or_collection(normalized):

            score += 1

        if code_has_loop(normalized) or "max(" in normalized:

            score += 1

        if (
            code_has_comparison(normalized)
            or "max(" in normalized
        ):

            score += 1

        reasons.append(
            "array/list handling"
        )

        reasons.append(
            "maximum search"
        )

    # =====================================================
    # SECOND LARGEST
    # =====================================================

    elif question_type == "second_largest":

        required = 4

        if code_has_array_or_collection(normalized):

            score += 1

        if code_has_loop(normalized):

            score += 1

        if (
            "second" in normalized
            or "secondlargest" in normalized
            or "second_largest" in normalized
            or "secondlargest" in normalized
        ):

            score += 1

        if (
            code_has_comparison(normalized)
            or "sort" in normalized
        ):

            score += 1

        reasons.append(
            "array/list processing"
        )

        reasons.append(
            "second-largest logic"
        )

    # =====================================================
    # REVERSE STRING
    # =====================================================

    elif question_type == "reverse_string":

        required = 3

        if contains_any(
            normalized,
            [
                "string",
                "char",
                "str"
            ]
        ):

            score += 1

        if contains_any(
            normalized,
            [
                "reverse",
                "revers",
                "[::-1]",
                "stringbuilder",
                "stringbuffer",
                "split",
                "swap"
            ]
        ):

            score += 1

        if (
            code_has_loop(normalized)
            or "reverse(" in normalized
            or "[::-1]" in normalized
        ):

            score += 1

        reasons.append(
            "string processing"
        )

        reasons.append(
            "reversal logic"
        )

    # =====================================================
    # PRIME NUMBER
    # =====================================================

    elif question_type == "prime":

        required = 3

        if (
            "%" in normalized
            or "mod" in normalized
        ):

            score += 1

        if code_has_loop(normalized):

            score += 1

        if (
            "sqrt" in normalized
            or "i * i" in normalized
            or "i*i" in normalized
            or "2" in normalized
        ):

            score += 1

        reasons.append(
            "divisibility checking"
        )

        reasons.append(
            "iteration"
        )

        reasons.append(
            "prime-number logic"
        )

    # =====================================================
    # REVERSE LINKED LIST
    # =====================================================

    elif question_type == "reverse_linked_list":

        required = 3

        if contains_any(
            normalized,
            [
                "node",
                "struct",
                "class"
            ]
        ):

            score += 1

        if "next" in normalized:

            score += 1

        if (
            code_has_loop(normalized)
            and contains_any(
                normalized,
                [
                    "prev",
                    "previous",
                    "current",
                    "curr"
                ]
            )
        ):

            score += 1

        reasons.append(
            "linked-list nodes"
        )

        reasons.append(
            "next-pointer handling"
        )

        reasons.append(
            "pointer reversal"
        )

    # =====================================================
    # DUPLICATES
    # =====================================================

    elif question_type == "duplicates":

        required = 3

        if code_has_array_or_collection(normalized):

            score += 1

        if contains_any(
            normalized,
            [
                "set",
                "hashset",
                "hashmap",
                "dict",
                "counter",
                "count"
            ]
        ):

            score += 1

        if code_has_loop(normalized):

            score += 1

        reasons.append(
            "array/list processing"
        )

        reasons.append(
            "duplicate tracking"
        )

        reasons.append(
            "iteration"
        )

    # =====================================================
    # FIRST NON-REPEATING CHARACTER
    # =====================================================

    elif question_type == "first_non_repeating":

        required = 3

        if contains_any(
            normalized,
            [
                "dict",
                "counter",
                "count",
                "map",
                "hashmap"
            ]
        ):

            score += 1

        if code_has_loop(normalized):

            score += 1

        if contains_any(
            normalized,
            [
                "return",
                "print",
                "printf"
            ]
        ):

            score += 1

        reasons.append(
            "frequency counting"
        )

        reasons.append(
            "character iteration"
        )

        reasons.append(
            "first unique-character selection"
        )

    # =====================================================
    # LONGEST SUBSTRING
    # =====================================================

    elif question_type == "longest_substring":

        required = 3

        if contains_any(
            normalized,
            [
                "set",
                "dict",
                "hashset",
                "map"
            ]
        ):

            score += 1

        if code_has_loop(normalized):

            score += 1

        if contains_any(
            normalized,
            [
                "left",
                "right",
                "window",
                "maxlength",
                "max_len",
                "maxlen"
            ]
        ):

            score += 1

        reasons.append(
            "unique-character tracking"
        )

        reasons.append(
            "iteration"
        )

        reasons.append(
            "sliding-window/maximum-length logic"
        )

    # =====================================================
    # STACK
    # =====================================================

    elif question_type == "stack":

        required = 3

        if "stack" in normalized:

            score += 1

        if contains_any(
            normalized,
            [
                "push",
                "pop"
            ]
        ):

            score += 1

        if contains_any(
            normalized,
            [
                "top",
                "peek",
                "array",
                "["
            ]
        ):

            score += 1

        reasons.append(
            "stack structure"
        )

        reasons.append(
            "push/pop operations"
        )

        reasons.append(
            "stack storage/access"
        )

    # =====================================================
    # BST
    # =====================================================

    elif question_type == "bst":

        required = 4

        if contains_any(
            normalized,
            [
                "node",
                "struct",
                "class"
            ]
        ):

            score += 1

        if "left" in normalized:

            score += 1

        if "right" in normalized:

            score += 1

        if contains_any(
            normalized,
            [
                "insert",
                "inorder",
                "in_order",
                "in order"
            ]
        ):

            score += 1

        reasons.append(
            "tree node structure"
        )

        reasons.append(
            "left/right child handling"
        )

        reasons.append(
            "BST insertion/traversal"
        )

    # =====================================================
    # CYCLE LINKED LIST
    # =====================================================

    elif question_type == "cycle_linked_list":

        required = 3

        if contains_any(
            normalized,
            [
                "node",
                "struct",
                "class"
            ]
        ):

            score += 1

        if "next" in normalized:

            score += 1

        if (
            "slow" in normalized
            and "fast" in normalized
        ) or contains_any(
            normalized,
            [
                "visited",
                "hashset",
                "set"
            ]
        ):

            score += 1

        reasons.append(
            "linked-list traversal"
        )

        reasons.append(
            "next-pointer handling"
        )

        reasons.append(
            "cycle detection"
        )

    # =====================================================
    # GRAPH BFS / DFS
    # =====================================================

    elif question_type == "graph":

        required = 4

        if "graph" in normalized:

            score += 1

        if (
            "bfs" in normalized
            or "breadth" in normalized
        ):

            score += 1

        if (
            "dfs" in normalized
            or "depth" in normalized
        ):

            score += 1

        if contains_any(
            normalized,
            [
                "queue",
                "stack",
                "visited",
                "recursion"
            ]
        ):

            score += 1

        reasons.append(
            "graph representation"
        )

        reasons.append(
            "BFS"
        )

        reasons.append(
            "DFS"
        )

        reasons.append(
            "traversal state"
        )

    # =====================================================
    # LRU CACHE
    # =====================================================

    elif question_type == "lru":

        required = 4

        if contains_any(
            normalized,
            [
                "hashmap",
                "hash_map",
                "dict",
                "ordered",
                "linkedhashmap"
            ]
        ):

            score += 1

        if contains_any(
            normalized,
            [
                "linked",
                "doubly",
                "ordereddict"
            ]
        ):

            score += 1

        if "get" in normalized:

            score += 1

        if "put" in normalized:

            score += 1

        reasons.append(
            "key-value cache storage"
        )

        reasons.append(
            "recency ordering"
        )

        reasons.append(
            "get operation"
        )

        reasons.append(
            "put operation"
        )

    # =====================================================
    # SQL
    # =====================================================

    elif question_type.startswith("sql_"):

        required = 3

        # Every SQL answer should normally contain SELECT.
        if "select" in normalized:

            score += 1

        # FROM is expected in these questions.
        if "from" in normalized:

            score += 1

        if question_type == "sql_second_highest":

            if contains_any(
                normalized,
                [
                    "max",
                    "dense_rank",
                    "row_number",
                    "rank",
                    "order by",
                    "limit",
                    "offset"
                ]
            ):

                score += 1

        elif question_type == "sql_salary_50000":

            required = 4

            if "salary" in normalized:

                score += 1

            if "50000" in normalized:

                score += 1

            if "where" in normalized:

                score += 1

        elif question_type == "sql_department_count":

            required = 4

            if "count" in normalized:

                score += 1

            if "department" in normalized:

                score += 1

            if "group by" in normalized:

                score += 1

        elif question_type == "sql_department_average":

            required = 4

            if "avg" in normalized:

                score += 1

            if "department" in normalized:

                score += 1

            if (
                "group by" in normalized
                or "partition by" in normalized
            ):

                score += 1

        elif question_type == "sql_second_department":

            required = 4

            if "salary" in normalized:

                score += 1

            if "department" in normalized:

                score += 1

            if contains_any(
                normalized,
                [
                    "dense_rank",
                    "row_number",
                    "rank"
                ]
            ):

                score += 1

        elif question_type == "sql_duplicates":

            required = 4

            if "group by" in normalized:

                score += 1

            if "having" in normalized:

                score += 1

            if "count" in normalized:

                score += 1

        elif question_type == "sql_top_three":

            required = 4

            if "salary" in normalized:

                score += 1

            if "department" in normalized:

                score += 1

            if contains_any(
                normalized,
                [
                    "row_number",
                    "rank",
                    "dense_rank"
                ]
            ):

                score += 1

            if "partition by" in normalized:

                score += 1

        elif question_type == "sql_salary_difference":

            required = 5

            if "salary" in normalized:

                score += 1

            if "max" in normalized:

                score += 1

            if "min" in normalized:

                score += 1

            if "department" in normalized:

                score += 1

            if "group by" in normalized:

                score += 1

        elif question_type == "sql_running_total":

            required = 5

            if "sum" in normalized:

                score += 1

            if "over" in normalized:

                score += 1

            if "order by" in normalized:

                score += 1

            if "salary" in normalized:

                score += 1

            if (
                "joining_date" in normalized
                or "join_date" in normalized
                or "joining date" in normalized
            ):

                score += 1

        reasons.append(
            "SQL query structure"
        )

        reasons.append(
            "question-specific SQL logic"
        )

    # =====================================================
    # WEB DEVELOPMENT
    # =====================================================

    elif question_type.startswith("web_"):

        required = 3

        if question_type == "web_registration":

            required = 5

            if "<form" in normalized:

                score += 1

            if "name" in normalized:

                score += 1

            if "email" in normalized:

                score += 1

            if "password" in normalized:

                score += 1

            if (
                "submit" in normalized
                or 'type="submit"' in normalized
            ):

                score += 1

        elif question_type == "web_reverse":

            required = 3

            if contains_any(
                normalized,
                [
                    "function",
                    "=>"
                ]
            ):

                score += 1

            if contains_any(
                normalized,
                [
                    "split",
                    "reverse",
                    "join",
                    "charat"
                ]
            ):

                score += 1

            if contains_any(
                normalized,
                [
                    "return",
                    "console.log",
                    "textcontent",
                    "innerhtml"
                ]
            ):

                score += 1

        elif question_type == "web_navigation":

            required = 4

            if (
                "<nav" in normalized
                or "navbar" in normalized
            ):

                score += 1

            if (
                "display" in normalized
                or "flex" in normalized
                or "grid" in normalized
            ):

                score += 1

            if "css" in normalized or "{" in normalized:

                score += 1

            if (
                "media" in normalized
                or "@media" in normalized
            ):

                score += 1

        elif question_type == "web_search_filter":

            required = 4

            if "input" in normalized:

                score += 1

            if "filter" in normalized:

                score += 1

            if (
                "includes" in normalized
                or "indexof" in normalized
            ):

                score += 1

            if (
                "addEventListener" .lower() in normalized
                or "onclick" in normalized
            ):

                score += 1

        elif question_type == "web_responsive":

            required = 4

            if (
                "grid" in normalized
                or "flex" in normalized
            ):

                score += 1

            if "display" in normalized:

                score += 1

            if (
                "@media" in normalized
                or "media" in normalized
            ):

                score += 1

            if "<html" in normalized or "<div" in normalized:

                score += 1

        elif question_type == "web_validation":

            required = 4

            if "email" in normalized:

                score += 1

            if "password" in normalized:

                score += 1

            if (
                "regex" in normalized
                or ".test(" in normalized
                or ".match(" in normalized
                or "includes" in normalized
            ):

                score += 1

            if (
                "valid" in normalized
                or "validation" in normalized
            ):

                score += 1

        elif question_type == "web_api":

            required = 4

            if "fetch(" in normalized:

                score += 1

            if (
                ".json(" in normalized
                or "json()" in normalized
            ):

                score += 1

            if (
                "then(" in normalized
                or "async" in normalized
                or "await" in normalized
            ):

                score += 1

            if (
                "innerhtml" in normalized
                or "textcontent" in normalized
                or "dom" in normalized
            ):

                score += 1

        elif question_type == "web_debounce":

            required = 4

            if (
                "settimeout" in normalized
                or "setinterval" in normalized
            ):

                score += 1

            if "cleartimeout" in normalized:

                score += 1

            if "input" in normalized:

                score += 1

            if "fetch" in normalized:

                score += 1

        elif question_type == "web_full_application":

            required = 5

            if "<form" in normalized:

                score += 1

            if (
                "fetch(" in normalized
                or "api" in normalized
            ):

                score += 1

            if (
                "valid" in normalized
                or "validation" in normalized
            ):

                score += 1

            if (
                "innerhtml" in normalized
                or "textcontent" in normalized
                or "dom" in normalized
            ):

                score += 1

            if (
                "css" in normalized
                or "display" in normalized
                or "@media" in normalized
            ):

                score += 1

        reasons.append(
            "required web-development structure"
        )

    # =====================================================
    # UNKNOWN QUESTION
    # =====================================================

    else:

        return {
            "correct": False,
            "attempted": True,
            "reason": (
                "No evaluation rule exists for "
                "this coding question yet."
            ),
            "matched": 0,
            "required": 0
        }

    # =====================================================
    # FINAL DECISION
    # =====================================================

    # A solution must satisfy at least 70% of the
    # question-specific concepts.

    threshold = max(
        1,
        int(
            required * 0.70
        )
    )

    is_correct = (
        score >= threshold
    )

    if is_correct:

        reason = (
            "Accepted: the submitted solution "
            "contains the required concepts for "
            "this coding problem."
        )

    else:

        missing = max(
            0,
            required - score
        )

        reason = (
            "Rejected: the submitted solution is "
            f"missing approximately {missing} "
            "important concept(s) for this problem."
        )

    return {

        "correct": is_correct,

        "attempted": True,

        "reason": reason,

        "matched": score,

        "required": required
    }




# =========================================================
# CODING QUESTION REQUIREMENTS
# =========================================================

def get_coding_requirements(
    question,
    language
):

    q = str(
        question or ""
    ).lower()

    language = str(
        language or ""
    ).lower()

    requirements = []

    # -----------------------------------------------------
    # C
    # -----------------------------------------------------

    if language == "c":

        if "largest element in an array" in q:

            requirements = [
                ["int", "float", "double"],
                ["for", "while"],
                ["array", "["]
            ]

        elif "reverse a string" in q:

            requirements = [
                ["char"],
                ["strlen", "string"],
                ["for", "while"],
                ["swap", "temp", "reverse"]
            ]

        elif "check whether a number is prime" in q:

            requirements = [
                ["int"],
                ["for", "while"],
                ["%", "mod"],
                ["prime"]
            ]

        elif "reverse a singly linked list" in q:

            requirements = [
                ["struct"],
                ["next"],
                ["prev"],
                ["while", "for"]
            ]

        elif "second largest element in an array" in q:

            requirements = [
                ["array", "["],
                ["second"],
                ["largest", "max"],
                ["for", "while"]
            ]

        elif "stack using an array" in q:

            requirements = [
                ["stack"],
                ["push"],
                ["pop"],
                ["top", "peek"],
                ["array", "["]
            ]

        elif "binary search tree" in q:

            requirements = [
                ["struct"],
                ["left"],
                ["right"],
                ["insert"],
                ["inorder"]
            ]

        elif "detect a cycle in a linked list" in q:

            requirements = [
                ["struct"],
                ["next"],
                ["slow"],
                ["fast"],
                ["while"]
            ]

        elif "graph traversal using bfs and dfs" in q:

            requirements = [
                ["graph"],
                ["bfs"],
                ["dfs"],
                ["queue"],
                ["visited"]
            ]

    # -----------------------------------------------------
    # JAVA
    # -----------------------------------------------------

    elif language == "java":

        if "second largest element in an array" in q:

            requirements = [
                ["int", "integer"],
                ["array", "[]"],
                ["second"],
                ["largest", "max"],
                ["for", "while"]
            ]

        elif "reverse a string" in q:

            requirements = [
                ["string"],
                ["reverse", "revers"],
                ["charat", "tochararray", "stringbuilder"],
            ]

        elif "check whether a number is prime" in q:

            requirements = [
                ["int"],
                ["%", "mod"],
                ["for", "while"],
                ["prime"]
            ]

        elif "reverse a singly linked list" in q:

            requirements = [
                ["node"],
                ["next"],
                ["prev"],
                ["while", "for"]
            ]

        elif "stack using an array" in q:

            requirements = [
                ["stack"],
                ["push"],
                ["pop"],
                ["top", "peek"],
                ["array", "[]"]
            ]

        elif "duplicate elements in an array" in q:

            requirements = [
                ["array", "[]"],
                ["duplicate"],
                ["hashset", "hashmap", "set"],
                ["for", "while"]
            ]

        elif "lru cache" in q:

            requirements = [
                ["lru"],
                ["hashmap"],
                ["doubly", "linked"],
                ["get"],
                ["put"]
            ]

        elif "detect a cycle in a linked list" in q:

            requirements = [
                ["node"],
                ["next"],
                ["slow"],
                ["fast"],
                ["while"]
            ]

        elif "bfs and dfs" in q:

            requirements = [
                ["bfs"],
                ["dfs"],
                ["queue"],
                ["visited"],
                ["graph"]
            ]

    # -----------------------------------------------------
    # PYTHON
    # -----------------------------------------------------

    elif language == "python":

        if "first non-repeating character" in q:

            requirements = [
                ["def"],
                ["count", "counter", "dict"],
                ["for"],
                ["return"]
            ]

        elif "check whether a number is prime" in q:

            requirements = [
                ["def", "prime"],
                ["%"],
                ["for", "while"],
                ["return"]
            ]

        elif "largest element in a list" in q:

            requirements = [
                ["list"],
                ["max", "for", "while"],
                ["return", "print"]
            ]

        elif "longest substring without repeating characters" in q:

            requirements = [
                ["def"],
                ["set", "dict"],
                ["left"],
                ["right", "for", "while"],
                ["return"]
            ]

        elif "reverse a singly linked list" in q:

            requirements = [
                ["class", "node"],
                ["next"],
                ["prev"],
                ["while"],
                ["return"]
            ]

        elif "duplicate elements in a list" in q:

            requirements = [
                ["list"],
                ["duplicate"],
                ["set", "dict"],
                ["for"]
            ]

        elif "lru cache" in q:

            requirements = [
                ["lru"],
                ["dict", "ordered"],
                ["get"],
                ["put"],
                ["cache"]
            ]

        elif "detect a cycle in a linked list" in q:

            requirements = [
                ["node"],
                ["next"],
                ["slow"],
                ["fast"],
                ["while"]
            ]

        elif "bfs and dfs" in q:

            requirements = [
                ["bfs"],
                ["dfs"],
                ["queue", "deque"],
                ["visited", "set"],
                ["graph"]
            ]

    # -----------------------------------------------------
    # SQL
    # -----------------------------------------------------

    elif language == "sql":

        if "second highest salary from an employee table" in q:

            requirements = [
                ["select"],
                ["salary"],
                ["employee"],
                ["max", "order by", "dense_rank", "limit", "offset"]
            ]

        elif "salary is greater than 50000" in q:

            requirements = [
                ["select"],
                ["from"],
                ["salary"],
                ["50000"],
                ["where"]
            ]

        elif "count the number of employees in each department" in q:

            requirements = [
                ["select"],
                ["count"],
                ["department"],
                ["group by"]
            ]

        elif "greater than the average salary of their department" in q:

            requirements = [
                ["select"],
                ["avg"],
                ["department"],
                ["group by", "partition by"],
                ["having", "where"]
            ]

        elif "second highest salary in each department" in q:

            requirements = [
                ["select"],
                ["salary"],
                ["department"],
                ["dense_rank", "row_number", "rank"],
                ["partition by"]
            ]

        elif "duplicate records in a table" in q:

            requirements = [
                ["select"],
                ["group by"],
                ["having"],
                ["count"]
            ]

        elif "top three highest-paid employees in each department" in q:

            requirements = [
                ["select"],
                ["department"],
                ["salary"],
                ["row_number", "rank", "dense_rank"],
                ["partition by"]
            ]

        elif "highest salary difference between employees in each department" in q:

            requirements = [
                ["select"],
                ["max"],
                ["min"],
                ["department"],
                ["group by"]
            ]

        elif "running total of employee salaries" in q:

            requirements = [
                ["select"],
                ["sum"],
                ["over"],
                ["order by"],
                ["joining", "join_date", "joining_date"]
            ]

    # -----------------------------------------------------
    # WEB DEVELOPMENT
    # -----------------------------------------------------

    elif language == "web development":

        if "registration form" in q:

            requirements = [
                ["<form"],
                ["name"],
                ["email"],
                ["password"],
                ["submit"]
            ]

        elif "javascript to reverse a string" in q:

            requirements = [
                ["function", "=>"],
                ["string"],
                ["reverse", "split"],
                ["join"]
            ]

        elif "responsive navigation bar" in q:

            requirements = [
                ["<nav", "<navbar"],
                ["html"],
                ["css"],
                ["display"],
                ["media"]
            ]

        elif "search filter" in q:

            requirements = [
                ["javascript"],
                ["filter"],
                ["input"],
                ["addEventListener", "onclick"],
                ["textcontent", "innerhtml"]
            ]

        elif "css grid or flexbox" in q:

            requirements = [
                ["html"],
                ["css"],
                ["grid", "flex"],
                ["display"],
                ["responsive"]
            ]

        elif "validate an email address and password" in q:

            requirements = [
                ["javascript"],
                ["email"],
                ["password"],
                ["validation", "valid"],
                ["regex", "test", "match"]
            ]

        elif "fetches data from a rest api" in q:

            requirements = [
                ["fetch"],
                ["api"],
                ["json"],
                ["then", "async", "await"],
                ["dom", "innerhtml", "textcontent"]
            ]

        elif "debounced search box" in q:

            requirements = [
                ["debounce"],
                ["settimeout"],
                ["cleartimeout"],
                ["input"],
                ["fetch"]
            ]

        elif "form validation, api integration and dynamic dom updates" in q:

            requirements = [
                ["html"],
                ["css"],
                ["javascript"],
                ["fetch"],
                ["validation"],
                ["dom", "innerhtml", "textcontent"]
            ]

    return requirements


# =========================================================
# CODING EVALUATION
# =========================================================

def evaluate_code(
    code,
    question,
    language
):

    code = str(
        code or ""
    ).strip()

    if not code:

        return {
            "correct": False,
            "attempted": False,
            "reason": "No answer submitted.",
            "matched": 0,
            "required": 0
        }

    normalized = normalize_code(
        code
    )

    requirements = get_coding_requirements(
        question,
        language
    )

    # If no question-specific rule exists,
    # do not automatically mark it correct.
    if not requirements:

        return {
            "correct": False,
            "attempted": True,
            "reason": (
                "This coding question does not "
                "have an evaluation rule yet."
            ),
            "matched": 0,
            "required": 0
        }

    matched = 0

    for requirement_group in requirements:

        if contains_any(
            normalized,
            requirement_group
        ):

            matched += 1

    total_requirements = len(
        requirements
    )

    # Require at least 70% of the important
    # programming concepts.
    threshold = max(
        1,
        int(
            total_requirements * 0.70
        )
    )

    is_correct = (
        matched >= threshold
    )

    if is_correct:

        reason = (
            "The submitted solution contains "
            "the required programming concepts."
        )

    else:

        reason = (
            "The submitted solution is missing "
            "some important concepts required "
            "for this question."
        )

    return {

        "correct": is_correct,

        "attempted": True,

        "reason": reason,

        "matched": matched,

        "required": total_requirements
    }


# =========================================================
# CODING RESULT PAGE
# =========================================================

def coding_result_page(
    user_data,
    results
):

    attempted = sum(
        1
        for item in results
        if item.get("attempted")
    )

    correct = sum(
        1
        for item in results
        if item.get("correct")
    )

    wrong = attempted - correct

    unanswered = (
        len(results)
        - attempted
    )

    score = correct * 100

    rows = []

    for index, item in enumerate(
        results
    ):

        if item.get("correct"):

            status = "Correct"

            status_class = "correct"

        elif item.get("attempted"):

            status = "Wrong"

            status_class = "wrong"

        else:

            status = "Not Attempted"

            status_class = "unanswered"

        rows.append(
            f"""
            <div class="result-card">

                <div class="question-title">
                    Coding Question {index + 1}
                </div>

                <div class="status {status_class}">
                    {status}
                </div>

                <p>
                    {escape_html(
                        item.get(
                            "reason",
                            ""
                        )
                    )}
                </p>

            </div>
            """
        )

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <meta charset="UTF-8">

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0"
        >

        <title>
            Coding Result
        </title>

        <style>

            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f4f6f9;
                color: #222;
            }}

            .header {{
                background: #1f2937;
                color: white;
                text-align: center;
                padding: 30px;
            }}

            .container {{
                width: 90%;
                max-width: 900px;
                margin: 35px auto;
            }}

            .summary {{
                background: white;
                padding: 30px;
                border-radius: 12px;
                margin-bottom: 25px;
                text-align: center;
                box-shadow:
                    0 2px 8px rgba(0,0,0,0.08);
            }}

            .score {{
                font-size: 38px;
                font-weight: bold;
                margin: 15px 0;
            }}

            .stats {{
                display: grid;
                grid-template-columns:
                    repeat(4, 1fr);
                gap: 15px;
                margin-top: 25px;
            }}

            .stat {{
                padding: 18px;
                background: #f8fafc;
                border-radius: 10px;
            }}

            .stat-number {{
                font-size: 25px;
                font-weight: bold;
            }}

            .result-card {{
                background: white;
                padding: 25px;
                margin-bottom: 18px;
                border-radius: 12px;
                box-shadow:
                    0 2px 8px rgba(0,0,0,0.08);
            }}

            .question-title {{
                font-size: 19px;
                font-weight: bold;
                margin-bottom: 12px;
            }}

            .status {{
                display: inline-block;
                padding: 7px 14px;
                border-radius: 20px;
                font-weight: bold;
                margin-bottom: 10px;
            }}

            .correct {{
                background: #dcfce7;
                color: #166534;
            }}

            .wrong {{
                background: #fee2e2;
                color: #991b1b;
            }}

            .unanswered {{
                background: #e5e7eb;
                color: #374151;
            }}

            .button {{
                display: block;
                width: fit-content;
                margin: 30px auto;
                padding: 14px 30px;
                background: #2563eb;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
            }}

            @media (max-width: 700px) {{

                .stats {{
                    grid-template-columns:
                        repeat(2, 1fr);
                }}

            }}

        </style>

    </head>

    <body>

        <div class="header">

            <h1>
                Round 3 — Coding Result
            </h1>

            <p>
                {escape_html(
                    user_data["programming_language"]
                )}
            </p>

        </div>

        <div class="container">

            <div class="summary">

                <h2>
                    Coding Round Completed
                </h2>

                <div class="score">
                    {score} / 500
                </div>

                <div class="stats">

                    <div class="stat">

                        <div class="stat-number">
                            {attempted}
                        </div>

                        Attempted

                    </div>

                    <div class="stat">

                        <div class="stat-number">
                            {correct}
                        </div>

                        Correct

                    </div>

                    <div class="stat">

                        <div class="stat-number">
                            {wrong}
                        </div>

                        Wrong

                    </div>

                    <div class="stat">

                        <div class="stat-number">
                            {unanswered}
                        </div>

                        Not Attempted

                    </div>

                </div>

            </div>

            {"".join(rows)}

            <a
                href="/hr"
                class="button"
            >
                Continue to HR Round
            </a>

        </div>

    </body>

    </html>
    """


# =========================================================
# HOME
# =========================================================

@app.get(
    "/",
    response_class=HTMLResponse
)
def home(request: Request):

    return render_template(
        LOGIN_TEMPLATE
    )


# =========================================================
# LOGIN
# =========================================================

@app.post("/login")
def login(
    request: Request,
    email: str = Form(""),
    password: str = Form("")
):

    email = email.strip().lower()
    password = password.strip()

    if not email:

        return render_template(
            LOGIN_TEMPLATE,
            error="Please enter your email address."
        )

    if not valid_email(email):

        return render_template(
            LOGIN_TEMPLATE,
            error="Please enter a valid email address."
        )

    if not password:

        return render_template(
            LOGIN_TEMPLATE,
            error="Please enter your password."
        )

    if len(password) < 6:

        return render_template(
            LOGIN_TEMPLATE,
            error=(
                "Password must contain "
                "at least 6 characters."
            )
        )

    with get_db() as db:

        user = db.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

        if not user:

            password_hash = hash_password(
                password
            )

            cursor = db.execute(
                """
                INSERT INTO users
                (
                    email,
                    password_hash,
                    created_at
                )
                VALUES (?, ?, ?)
                """,
                (
                    email,
                    password_hash,
                    datetime.utcnow().isoformat()
                )
            )

            db.commit()

            user_id = cursor.lastrowid

        else:

            if not verify_password(
                password,
                user["password_hash"]
            ):

                return render_template(
                    LOGIN_TEMPLATE,
                    error="Incorrect password."
                )

            user_id = user["id"]

    create_login_session(
        request,
        user_id
    )

    return RedirectResponse(
        url="/personal",
        status_code=303
    )


# =========================================================
# PERSONAL GET
# =========================================================

@app.get(
    "/personal",
    response_class=HTMLResponse
)
def personal(request: Request):

    user_id, user_data = get_current_user(
        request
    )

    if not user_id:

        return RedirectResponse(
            url="/",
            status_code=303
        )

    return render_template(
        PERSONAL_TEMPLATE
    )


# =========================================================
# PERSONAL POST
# =========================================================

@app.post("/personal")
def save_personal(
    request: Request,
    name: str = Form(""),
    age: str = Form(""),
    gender: str = Form(""),
    phone: str = Form("")
):

    user_id, user_data = get_current_user(
        request
    )

    if not user_id:

        return RedirectResponse(
            url="/",
            status_code=303
        )

    name = name.strip()
    age = age.strip()
    gender = gender.strip()
    phone = phone.strip()

    if not name:

        return render_template(
            PERSONAL_TEMPLATE,
            error="Please enter your name."
        )

    if not age:

        return render_template(
            PERSONAL_TEMPLATE,
            error="Please enter your age."
        )

    try:

        age_number = int(age)

    except ValueError:

        return render_template(
            PERSONAL_TEMPLATE,
            error="Age must be a valid number."
        )

    if age_number < 13 or age_number > 80:

        return render_template(
            PERSONAL_TEMPLATE,
            error="Age must be between 13 and 80."
        )

    if not gender:

        return render_template(
            PERSONAL_TEMPLATE,
            error="Please select your gender."
        )

    if not re.fullmatch(
        r"[0-9]{10}",
        phone
    ):

        return render_template(
            PERSONAL_TEMPLATE,
            error=(
                "Please enter a valid "
                "10-digit contact number."
            )
        )

    user_data["name"] = name
    user_data["age"] = age_number
    user_data["gender"] = gender
    user_data["phone"] = phone

    save_user_data(
        user_id,
        user_data
    )

    return RedirectResponse(
        url="/education",
        status_code=303
    )


# =========================================================
# EDUCATION GET
# =========================================================

@app.get(
    "/education",
    response_class=HTMLResponse
)
def education(request: Request):

    user_id, user_data = get_current_user(
        request
    )

    if not user_id:

        return RedirectResponse(
            url="/",
            status_code=303
        )

    return render_template(
        EDUCATION_TEMPLATE
    )


# =========================================================
# OLD EDUCATIONAL URL
# =========================================================

@app.get("/educational")
def old_education():

    return RedirectResponse(
        url="/education",
        status_code=303
    )


# =========================================================
# EDUCATION POST
# =========================================================

@app.post("/education")
def save_education(
    request: Request,
    college: str = Form(""),
    degree: str = Form(""),
    branch: str = Form(""),
    graduation_year: str = Form("")
):

    user_id, user_data = get_current_user(
        request
    )

    if not user_id:

        return RedirectResponse(
            url="/",
            status_code=303
        )

    college = college.strip()
    degree = degree.strip()
    branch = branch.strip()
    graduation_year = graduation_year.strip()

    if not college:

        return render_template(
            EDUCATION_TEMPLATE,
            error="Please enter your college name."
        )

    if not degree:

        return render_template(
            EDUCATION_TEMPLATE,
            error="Please enter your degree."
        )

    if not branch:

        return render_template(
            EDUCATION_TEMPLATE,
            error="Please enter your branch."
        )

    if not graduation_year:

        return render_template(
            EDUCATION_TEMPLATE,
            error="Please enter your graduation year."
        )

    try:

        year = int(graduation_year)

    except ValueError:

        return render_template(
            EDUCATION_TEMPLATE,
            error="Graduation year must be a number."
        )

    current_year = datetime.now().year

    if year < 2000 or year > current_year + 10:

        return render_template(
            EDUCATION_TEMPLATE,
            error="Please enter a valid graduation year."
        )

    user_data["college"] = college
    user_data["degree"] = degree
    user_data["branch"] = branch
    user_data["graduation_year"] = year

    save_user_data(
        user_id,
        user_data
    )

    return RedirectResponse(
        url="/skills",
        status_code=303
    )


# =========================================================
# SKILLS GET
# =========================================================

@app.get(
    "/skills",
    response_class=HTMLResponse
)
def skills(request: Request):

    user_id, user_data = get_current_user(
        request
    )

    if not user_id:

        return RedirectResponse(
            url="/",
            status_code=303
        )

    return render_template(
        SKILLS_TEMPLATE
    )


# =========================================================
# SKILLS POST
# =========================================================

@app.post("/skills")
def save_skills(
    request: Request,
    programming_language: str = Form("Python"),
    skills: str = Form(""),
    experience: str = Form(""),
    level: str = Form("Intermediate")
):

    user_id, user_data = get_current_user(
        request
    )

    if not user_id:

        return RedirectResponse(
            url="/",
            status_code=303
        )

    programming_language = programming_language.strip()
    skills = skills.strip()
    experience = experience.strip()
    level = level.strip()

    if programming_language not in LANGUAGES:

        return render_template(
            SKILLS_TEMPLATE,
            error=(
                "Please select a valid "
                "programming language."
            )
        )

    if level not in LEVELS:

        return render_template(
            SKILLS_TEMPLATE,
            error=(
                "Please select a valid "
                "difficulty level."
            )
        )

    if not skills:

        return render_template(
            SKILLS_TEMPLATE,
            error="Please enter your skills."
        )

    user_data["programming_language"] = programming_language
    user_data["skills"] = skills
    user_data["experience"] = experience
    user_data["level"] = level

    user_data["aptitude_score"] = 0
    user_data["technical_score"] = 0
    user_data["coding_score"] = 0
    user_data["hr_score"] = 0
    user_data["total_score"] = 0

    user_data["aptitude_exam"] = []
    user_data["technical_exam"] = []
    user_data["coding_exam"] = []
    user_data["hr_exam"] = []
    user_data["coding_result"] = []

    save_user_data(
        user_id,
        user_data
    )

    return RedirectResponse(
        url="/interview",
        status_code=303
    )


# =========================================================
# START INTERVIEW
# =========================================================

@app.get("/interview")
def interview(request: Request):

    user_id, user_data = get_current_user(
        request
    )

    if not user_id:

        return RedirectResponse(
            url="/",
            status_code=303
        )

    return RedirectResponse(
        url="/aptitude",
        status_code=303
    )


# =========================================================
# APTITUDE
# =========================================================

@app.get(
    "/aptitude",
    response_class=HTMLResponse
)
def aptitude(request: Request):

    user_id, user_data = get_current_user(
        request
    )

    if not user_id:

        return RedirectResponse(
            url="/",
            status_code=303
        )

    questions = get_aptitude_exam_questions(
        user_data["level"]
    )

    user_data["aptitude_exam"] = questions

    save_user_data(
        user_id,
        user_data
    )

    return HTMLResponse(
        content=mcq_page(
            title="Round 1 — Aptitude",
            subtitle="Select the correct answer",
            questions=questions,
            submit_url="/submit-aptitude",
            user_data=user_data
        )
    )


# =========================================================
# SUBMIT APTITUDE
# =========================================================

@app.post("/submit-aptitude")
async def submit_aptitude(
    request: Request
):

    user_id, user_data = get_current_user(
        request
    )

    if not user_id:

        return RedirectResponse(
            url="/",
            status_code=303
        )

    form = await request.form()

    user_data["aptitude_score"] = (
        calculate_mcq_score(
            form,
            user_data["aptitude_exam"]
        )
    )

    save_user_data(
        user_id,
        user_data
    )

    return RedirectResponse(
        url="/technical",
        status_code=303
    )


# =========================================================
# TECHNICAL
# =========================================================

@app.get(
    "/technical",
    response_class=HTMLResponse
)
def technical(request: Request):

    user_id, user_data = get_current_user(
        request
    )

    if not user_id:

        return RedirectResponse(
            url="/",
            status_code=303
        )

    language = user_data[
        "programming_language"
    ]

    questions = get_technical_exam_questions(
        user_data["level"],
        language
    )

    user_data["technical_exam"] = questions

    save_user_data(
        user_id,
        user_data
    )

    return HTMLResponse(
        content=mcq_page(
            title="Round 2 — Technical",
            subtitle=language + " Technical MCQ",
            questions=questions,
            submit_url="/submit-technical",
            user_data=user_data
        )
    )


# =========================================================
# SUBMIT TECHNICAL
# =========================================================

@app.post("/submit-technical")
async def submit_technical(
    request: Request
):

    user_id, user_data = get_current_user(
        request
    )

    if not user_id:

        return RedirectResponse(
            url="/",
            status_code=303
        )

    form = await request.form()

    user_data["technical_score"] = (
        calculate_mcq_score(
            form,
            user_data["technical_exam"]
        )
    )

    save_user_data(
        user_id,
        user_data
    )

    return RedirectResponse(
        url="/coding",
        status_code=303
    )


# =========================================================
# OLD TECHNICAL URL
# =========================================================

@app.get("/test-phase")
def old_test_phase():

    return RedirectResponse(
        url="/technical",
        status_code=303
    )


# =========================================================
# CODING
# =========================================================

@app.get(
    "/coding",
    response_class=HTMLResponse
)
def coding(request: Request):

    user_id, user_data = get_current_user(
        request
    )

    if not user_id:

        return RedirectResponse(
            url="/",
            status_code=303
        )

    language = user_data[
        "programming_language"
    ]

    questions = get_coding_questions(
        user_data["level"],
        language
    )

    user_data["coding_exam"] = questions

    user_data["coding_result"] = []

    save_user_data(
        user_id,
        user_data
    )

    cards = []

    for index, question in enumerate(
        questions
    ):

        cards.append(
            f"""
            <div class="question-card">

                <div class="question-number">
                    Coding Question {index + 1}
                </div>

                <h2>
                    {escape_html(question)}
                </h2>

                <textarea
                    name="code_{index}"
                    placeholder="Write your {escape_html(language)} code here..."
                    required
                ></textarea>

            </div>
            """
        )

    if not cards:

        cards.append("""
        <div class="question-card">

            <h2>
                No coding questions available.
            </h2>

            <p>
                Please check coding_questions.json.
            </p>

        </div>
        """)

    return HTMLResponse(
        content=f"""
        <!DOCTYPE html>

        <html>

        <head>

            <meta charset="UTF-8">

            <meta
                name="viewport"
                content="width=device-width, initial-scale=1.0"
            >

            <title>
                Round 3 — Coding
            </title>

            <style>

                * {{
                    box-sizing: border-box;
                }}

                body {{
                    margin: 0;
                    font-family: Arial, sans-serif;
                    background: #f4f6f9;
                }}

                .header {{
                    background: #1f2937;
                    color: white;
                    text-align: center;
                    padding: 30px;
                }}

                .container {{
                    width: 90%;
                    max-width: 1000px;
                    margin: 30px auto;
                }}

                .info,
                .question-card {{
                    background: white;
                    padding: 25px;
                    margin-bottom: 25px;
                    border-radius: 12px;
                    box-shadow:
                        0 2px 8px rgba(0,0,0,0.08);
                }}

                .question-number {{
                    font-weight: bold;
                    color: #555;
                    margin-bottom: 12px;
                }}

                textarea {{
                    width: 100%;
                    min-height: 250px;
                    background: #1e1e1e;
                    color: white;
                    padding: 20px;
                    border-radius: 8px;
                    font-family: Consolas, monospace;
                    font-size: 15px;
                    resize: vertical;
                }}

                .button {{
                    display: block;
                    margin: 30px auto;
                    padding: 15px 35px;
                    background: #2563eb;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 17px;
                    font-weight: bold;
                    cursor: pointer;
                }}

            </style>

        </head>

        <body>

            <div class="header">

                <h1>
                    Round 3 — Coding
                </h1>

                <p>
                    {escape_html(language)}
                    Coding Round
                </p>

            </div>

            <div class="container">

                <div class="info">

                    <strong>
                        Language:
                    </strong>

                    {escape_html(language)}

                    <br><br>

                    <strong>
                        Difficulty:
                    </strong>

                    {escape_html(user_data["level"])}

                    <br><br>

                    Write your solution in the editor.

                    <br><br>

                    <strong>
                        Scoring:
                    </strong>

                    Each correctly evaluated question =
                    100 marks.

                    <br>

                    Blank answers =
                    Not Attempted.

                </div>

                <form
                    method="post"
                    action="/submit-coding"
                >

                    {"".join(cards)}

                    <button
                        type="submit"
                        class="button"
                    >
                        Submit Coding Round
                    </button>

                </form>

            </div>

        </body>

        </html>
        """
    )


# =========================================================
# SUBMIT CODING
# =========================================================

@app.post("/submit-coding")
async def submit_coding(
    request: Request
):

    user_id, user_data = get_current_user(
        request
    )

    if not user_id:

        return RedirectResponse(
            url="/",
            status_code=303
        )

    form = await request.form()

    language = user_data[
        "programming_language"
    ]

    results = []

    score = 0

    for index, question in enumerate(
        user_data["coding_exam"]
    ):

        code = str(
            form.get(
                f"code_{index}",
                ""
            )
        ).strip()

        evaluation = evaluate_code(
            code,
            question,
            language
        )

        result = {

            "question": question,

            "attempted": evaluation[
                "attempted"
            ],

            "correct": evaluation[
                "correct"
            ],

            "reason": evaluation[
                "reason"
            ],

            "matched": evaluation[
                "matched"
            ],

            "required": evaluation[
                "required"
            ]
        }

        results.append(
            result
        )

        if evaluation["correct"]:

            score += 100

    user_data["coding_score"] = score

    user_data["coding_result"] = results

    save_user_data(
        user_id,
        user_data
    )

    return HTMLResponse(
        content=coding_result_page(
            user_data,
            results
        )
    )


# =========================================================
# OLD CODING URL
# =========================================================

@app.get("/coding-phase")
def old_coding_phase():

    return RedirectResponse(
        url="/coding",
        status_code=303
    )


# =========================================================
# HR
# =========================================================

@app.get(
    "/hr",
    response_class=HTMLResponse
)
def hr(request: Request):

    user_id, user_data = get_current_user(
        request
    )

    if not user_id:

        return RedirectResponse(
            url="/",
            status_code=303
        )

    questions = get_hr_exam_questions(
        user_data["level"]
    )

    user_data["hr_exam"] = questions

    save_user_data(
        user_id,
        user_data
    )

    return HTMLResponse(
        content=mcq_page(
            title="Round 4 — HR / Communication",
            subtitle="Select the best answer",
            questions=questions,
            submit_url="/submit-hr",
            user_data=user_data
        )
    )


# =========================================================
# SUBMIT HR
# =========================================================

@app.post("/submit-hr")
async def submit_hr(
    request: Request
):

    user_id, user_data = get_current_user(
        request
    )

    if not user_id:

        return RedirectResponse(
            url="/",
            status_code=303
        )

    form = await request.form()

    user_data["hr_score"] = (
        calculate_mcq_score(
            form,
            user_data["hr_exam"]
        )
    )

    user_data["total_score"] = (

        user_data["aptitude_score"]

        + user_data["technical_score"]

        + user_data["coding_score"]

        + user_data["hr_score"]
    )

    save_user_data(
        user_id,
        user_data
    )

    return RedirectResponse(
        url="/completed",
        status_code=303
    )


# =========================================================
# COMPLETED
# =========================================================

@app.get(
    "/completed",
    response_class=HTMLResponse
)
def completed(request: Request):

    user_id, user_data = get_current_user(
        request
    )

    if not user_id:

        return RedirectResponse(
            url="/",
            status_code=303
        )

    coding_results = user_data.get(
        "coding_result",
        []
    )

    coding_attempted = sum(
        1
        for item in coding_results
        if item.get("attempted")
    )

    coding_correct = sum(
        1
        for item in coding_results
        if item.get("correct")
    )

    coding_wrong = (
        coding_attempted
        - coding_correct
    )

    coding_unanswered = (
        len(coding_results)
        - coding_attempted
    )

    return HTMLResponse(
        content=f"""
        <!DOCTYPE html>

        <html>

        <head>

            <meta charset="UTF-8">

            <meta
                name="viewport"
                content="width=device-width, initial-scale=1.0"
            >

            <title>
                Interview Completed
            </title>

            <style>

                body {{
                    margin: 0;
                    font-family: Arial, sans-serif;
                    background: #f4f6f9;
                }}

                .container {{
                    width: 90%;
                    max-width: 750px;
                    margin: 80px auto;
                    background: white;
                    padding: 50px;
                    text-align: center;
                    border-radius: 15px;
                    box-shadow:
                        0 4px 15px
                        rgba(0,0,0,0.1);
                }}

                .score {{
                    font-size: 30px;
                    font-weight: bold;
                    margin: 25px 0;
                }}

                .coding-box {{
                    margin: 25px 0;
                    padding: 20px;
                    background: #f8fafc;
                    border-radius: 12px;
                    text-align: left;
                }}

                .coding-box h3 {{
                    text-align: center;
                }}

                .button,
                .logout {{
                    display: inline-block;
                    margin-top: 20px;
                    padding: 14px 30px;
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: bold;
                }}

                .button {{
                    background: #2563eb;
                }}

                .logout {{
                    background: #dc2626;
                }}

            </style>

        </head>

        <body>

            <div class="container">

                <h1>
                    🎉 Interview Completed!
                </h1>

                <p>
                    Congratulations!
                    You have successfully completed
                    all four interview rounds.
                </p>

                <div class="score">

                    Total Score:
                    {user_data["total_score"]}

                </div>

                <p>
                    Aptitude:
                    {user_data["aptitude_score"]}
                </p>

                <p>
                    Technical:
                    {user_data["technical_score"]}
                </p>

                <p>
                    Coding:
                    {user_data["coding_score"]}
                </p>

                <div class="coding-box">

                    <h3>
                        Coding Evaluation
                    </h3>

                    <p>
                        Attempted:
                        <strong>
                            {coding_attempted}
                        </strong>
                    </p>

                    <p>
                        Correct:
                        <strong>
                            {coding_correct}
                        </strong>
                    </p>

                    <p>
                        Wrong:
                        <strong>
                            {coding_wrong}
                        </strong>
                    </p>

                    <p>
                        Not Attempted:
                        <strong>
                            {coding_unanswered}
                        </strong>
                    </p>

                </div>

                <p>
                    HR:
                    {user_data["hr_score"]}
                </p>

                <a
                    href="/skills"
                    class="button"
                >
                    Start Another Interview
                </a>

                <br>

                <a
                    href="/logout"
                    class="logout"
                >
                    Logout
                </a>

            </div>

        </body>

        </html>
        """
    )


# =========================================================
# LOGOUT
# =========================================================

@app.get("/logout")
def logout(request: Request):

    session_id = request.session.get(
        "session_id"
    )

    if session_id:

        with get_db() as db:

            db.execute(
                """
                DELETE FROM sessions
                WHERE session_id = ?
                """,
                (session_id,)
            )

            db.commit()

    request.session.clear()

    return RedirectResponse(
        url="/",
        status_code=303
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "ok",
        "application": "SmartPrep AI"
    }