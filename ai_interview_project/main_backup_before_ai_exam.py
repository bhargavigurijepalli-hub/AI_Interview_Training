from pathlib import Path
import json

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse


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


# =========================================================
# CURRENT USER DATA
# =========================================================

user_data = {
    "name": "",
    "age": "",
    "gender": "",
    "college": "",
    "degree": "",
    "branch": "",
    "graduation_year": "",
    "skills": "",
    "experience": "",
    "level": "Intermediate",
    "programming_language": "Python"
}


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

        return {}

    except json.JSONDecodeError:

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


def render_template(file_path):

    return HTMLResponse(
        content=load_template(file_path)
    )


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
# LEVEL MAPPING
# =========================================================

def general_level(level):

    """
    Aptitude and HR use:

    Intermediate -> intermediate
    Medium       -> medium
    Advanced     -> advanced
    """

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

    """
    Technical uses:

    Intermediate -> intermediate
    Medium       -> medium
    Advanced     -> advanced
    """

    mapping = {

        "Intermediate": "intermediate",

        "Medium": "medium",

        "Advanced": "advanced"

    }

    return mapping.get(
        level,
        "intermediate"
    )


def coding_level(level):

    """
    Coding uses:

    Intermediate -> Easy
    Medium       -> Medium
    Advanced     -> Hard
    """

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
# APTITUDE QUESTIONS
# =========================================================

def get_aptitude_questions(level):

    data = load_json(
        QUESTION_FILE
    )

    aptitude = data.get(
        "aptitude",
        {}
    )

    selected_level = general_level(
        level
    )

    return aptitude.get(
        selected_level,
        []
    )


# =========================================================
# TECHNICAL QUESTIONS
# =========================================================

def get_technical_questions(
    level,
    language
):

    data = load_json(
        QUESTION_FILE
    )

    technical = data.get(
        "technical",
        {}
    )

    language_data = technical.get(
        language,
        {}
    )

    selected_level = technical_level(
        level
    )

    return language_data.get(
        selected_level,
        []
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

    language_data = data.get(
        language,
        {}
    )

    selected_level = coding_level(
        level
    )

    return language_data.get(
        selected_level,
        []
    )


# =========================================================
# HR / COMMUNICATION QUESTIONS
# =========================================================

def get_hr_questions(level):

    data = load_json(
        QUESTION_FILE
    )

    communication = data.get(
        "communication",
        {}
    )

    selected_level = general_level(
        level
    )

    return communication.get(
        selected_level,
        []
    )


# =========================================================
# GET APTITUDE ANSWER
# =========================================================

def get_aptitude_answer(
    level,
    index
):

    data = load_json(
        ANSWERS_FILE
    )

    aptitude = data.get(
        "aptitude",
        {}
    )

    selected_level = general_level(
        level
    )

    answers = aptitude.get(
        selected_level,
        []
    )

    if index < len(answers):

        return answers[index]

    return "Answer not available."


# =========================================================
# GET TECHNICAL ANSWER
# =========================================================

def get_technical_answer(
    level,
    language,
    index
):

    data = load_json(
        ANSWERS_FILE
    )

    technical = data.get(
        "technical",
        {}
    )

    language_data = technical.get(
        language,
        {}
    )

    selected_level = technical_level(
        level
    )

    answers = language_data.get(
        selected_level,
        []
    )

    if index < len(answers):

        return answers[index]

    return "Answer not available."


# =========================================================
# GET CODING SOLUTION
# =========================================================

def get_coding_answer(
    level,
    language,
    index
):

    data = load_json(
        ANSWERS_FILE
    )

    coding = data.get(
        "coding",
        {}
    )

    language_data = coding.get(
        language,
        {}
    )

    selected_level = coding_level(
        level
    )

    answers = language_data.get(
        selected_level,
        []
    )

    if index < len(answers):

        return answers[index]

    return "Solution not available."


# =========================================================
# GET HR ANSWER
# =========================================================

def get_hr_answer(
    level,
    index
):

    data = load_json(
        ANSWERS_FILE
    )

    communication = data.get(
        "communication",
        {}
    )

    selected_level = general_level(
        level
    )

    answers = communication.get(
        selected_level,
        []
    )

    if index < len(answers):

        return answers[index]

    return "Answer not available."


# =========================================================
# QUESTION PAGE DESIGN
# =========================================================

def question_page(
    title,
    subtitle,
    questions,
    answers,
    next_url,
    button_text,
    code_mode=False
):

    cards = []

    for index, question in enumerate(
        questions
    ):

        question_text = escape_html(
            question
        )

        if index < len(answers):

            answer_text = escape_html(
                answers[index]
            )

        else:

            answer_text = (
                "Answer not available."
            )

        if code_mode:

            answer_html = f"""
            <div class="answer-box">

                <h3>Solution</h3>

                <pre><code>{answer_text}</code></pre>

            </div>
            """

        else:

            answer_html = f"""
            <div class="answer-box">

                <h3>Answer</h3>

                <p>{answer_text}</p>

            </div>
            """

        card = f"""
        <div class="question-card">

            <div class="question-number">
                Question {index + 1}
            </div>

            <h2>
                {question_text}
            </h2>

            {answer_html}

        </div>
        """

        cards.append(card)

    all_cards = "\n".join(cards)

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <meta charset="UTF-8">

        <meta
            name="viewport"
            content="width=device-width,
            initial-scale=1.0"
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

            .header h1 {{
                margin: 0 0 10px;
            }}

            .header p {{
                margin: 0;
                font-size: 17px;
            }}

            .container {{
                width: 90%;
                max-width: 1000px;
                margin: 30px auto;
            }}

            .candidate-info {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 25px;
                box-shadow:
                    0 2px 8px
                    rgba(0,0,0,0.08);
            }}

            .question-card {{
                background: white;
                padding: 25px;
                margin-bottom: 25px;
                border-radius: 12px;
                box-shadow:
                    0 2px 8px
                    rgba(0,0,0,0.08);
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

            .answer-box {{
                margin-top: 20px;
                padding: 20px;
                background: #eef6ff;
                border-left: 5px solid #2563eb;
                border-radius: 7px;
            }}

            .answer-box h3 {{
                margin-top: 0;
                color: #1d4ed8;
            }}

            .answer-box p {{
                line-height: 1.7;
                white-space: pre-wrap;
            }}

            pre {{
                background: #1e1e1e;
                color: #f5f5f5;
                padding: 20px;
                border-radius: 7px;
                overflow-x: auto;
                line-height: 1.5;
            }}

            code {{
                font-family: Consolas, monospace;
            }}

            .button-container {{
                text-align: center;
                margin: 40px 0;
            }}

            .next-button {{
                display: inline-block;
                background: #2563eb;
                color: white;
                padding: 15px 32px;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
            }}

            .next-button:hover {{
                background: #1d4ed8;
            }}

            .no-question {{
                background: white;
                padding: 30px;
                text-align: center;
                border-radius: 10px;
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

                <strong>Candidate:</strong>
                {escape_html(user_data["name"])}

                <br><br>

                <strong>Difficulty:</strong>
                {escape_html(user_data["level"])}

                <br><br>

                <strong>Language:</strong>
                {escape_html(
                    user_data["programming_language"]
                )}

            </div>

            {
                all_cards
                if all_cards
                else
                '<div class="no-question">No questions available for this selection.</div>'
            }

            <div class="button-container">

                <a
                    href="{next_url}"
                    class="next-button"
                >
                    {escape_html(button_text)}
                </a>

            </div>

        </div>

    </body>

    </html>
    """


# =========================================================
# HOME / LOGIN
# =========================================================

@app.get(
    "/",
    response_class=HTMLResponse
)
def home():

    return render_template(
        LOGIN_TEMPLATE
    )


@app.post("/login")
def login(
    email: str = Form(""),
    password: str = Form("")
):

    return RedirectResponse(
        url="/personal",
        status_code=303
    )


# =========================================================
# PERSONAL DETAILS
# =========================================================

@app.get(
    "/personal",
    response_class=HTMLResponse
)
def personal():

    return render_template(
        PERSONAL_TEMPLATE
    )


@app.post("/personal")
def save_personal(
    name: str = Form(""),
    age: str = Form(""),
    gender: str = Form("")
):

    user_data["name"] = name
    user_data["age"] = age
    user_data["gender"] = gender

    return RedirectResponse(
        url="/education",
        status_code=303
    )


# =========================================================
# EDUCATION
# =========================================================

@app.get(
    "/education",
    response_class=HTMLResponse
)
def education():

    return render_template(
        EDUCATION_TEMPLATE
    )


# Old URL also supported
@app.get(
    "/educational"
)
def old_education():

    return RedirectResponse(
        url="/education",
        status_code=303
    )


@app.post("/education")
def save_education(
    college: str = Form(""),
    degree: str = Form(""),
    branch: str = Form(""),
    graduation_year: str = Form("")
):

    user_data["college"] = college
    user_data["degree"] = degree
    user_data["branch"] = branch
    user_data["graduation_year"] = (
        graduation_year
    )

    return RedirectResponse(
        url="/skills",
        status_code=303
    )


# =========================================================
# SKILLS
# =========================================================

@app.get(
    "/skills",
    response_class=HTMLResponse
)
def skills():

    return render_template(
        SKILLS_TEMPLATE
    )


@app.post("/skills")
def save_skills(
    programming_language: str = Form("Python"),
    skills: str = Form(""),
    experience: str = Form(""),
    level: str = Form("Intermediate")
):

    if programming_language not in LANGUAGES:

        programming_language = "Python"

    if level not in LEVELS:

        level = "Intermediate"

    user_data["programming_language"] = (
        programming_language
    )

    user_data["skills"] = skills

    user_data["experience"] = experience

    user_data["level"] = level

    return RedirectResponse(
        url="/aptitude",
        status_code=303
    )


# =========================================================
# ROUND 1 — APTITUDE
# =========================================================

@app.get(
    "/aptitude",
    response_class=HTMLResponse
)
def aptitude():

    level = user_data["level"]

    questions = get_aptitude_questions(
        level
    )

    answers = []

    for index in range(
        len(questions)
    ):

        answers.append(
            get_aptitude_answer(
                level,
                index
            )
        )

    return HTMLResponse(
        content=question_page(

            title="Round 1 — Aptitude",

            subtitle=(
                "Aptitude Questions "
                "with Answers"
            ),

            questions=questions,

            answers=answers,

            next_url="/technical",

            button_text=(
                "Continue to Technical Round"
            )
        )
    )


# =========================================================
# ROUND 2 — TECHNICAL
# =========================================================

@app.get(
    "/technical",
    response_class=HTMLResponse
)
def technical():

    level = user_data["level"]

    language = user_data[
        "programming_language"
    ]

    questions = get_technical_questions(
        level,
        language
    )

    answers = []

    for index in range(
        len(questions)
    ):

        answers.append(
            get_technical_answer(
                level,
                language,
                index
            )
        )

    return HTMLResponse(
        content=question_page(

            title="Round 2 — Technical",

            subtitle=(
                language +
                " Technical Questions "
                "with Answers"
            ),

            questions=questions,

            answers=answers,

            next_url="/coding",

            button_text=(
                "Continue to Coding Round"
            )
        )
    )


# =========================================================
# OLD TECHNICAL URL
# =========================================================

@app.get(
    "/test-phase"
)
def old_test_phase():

    return RedirectResponse(
        url="/technical",
        status_code=303
    )


# =========================================================
# ROUND 3 — CODING
# =========================================================

@app.get(
    "/coding",
    response_class=HTMLResponse
)
def coding():

    level = user_data["level"]

    language = user_data[
        "programming_language"
    ]

    questions = get_coding_questions(
        level,
        language
    )

    answers = []

    for index in range(
        len(questions)
    ):

        answers.append(
            get_coding_answer(
                level,
                language,
                index
            )
        )

    return HTMLResponse(
        content=question_page(

            title="Round 3 — Coding",

            subtitle=(
                language +
                " Coding Questions "
                "with Solutions"
            ),

            questions=questions,

            answers=answers,

            next_url="/hr",

            button_text=(
                "Continue to HR / Communication"
            ),

            code_mode=True
        )
    )


# =========================================================
# OLD CODING URL
# =========================================================

@app.get(
    "/coding-phase"
)
def old_coding_phase():

    return RedirectResponse(
        url="/coding",
        status_code=303
    )


# =========================================================
# ROUND 4 — HR / COMMUNICATION
# =========================================================

@app.get(
    "/hr",
    response_class=HTMLResponse
)
def hr():

    level = user_data["level"]

    questions = get_hr_questions(
        level
    )

    answers = []

    for index in range(
        len(questions)
    ):

        answers.append(
            get_hr_answer(
                level,
                index
            )
        )

    return HTMLResponse(
        content=question_page(

            title="Round 4 — HR / Communication",

            subtitle=(
                "HR and Communication "
                "Questions with Answers"
            ),

            questions=questions,

            answers=answers,

            next_url="/completed",

            button_text="Finish Interview"
        )
    )


# =========================================================
# COMPLETED
# =========================================================

@app.get(
    "/completed",
    response_class=HTMLResponse
)
def completed():

    return HTMLResponse(
        content="""

        <!DOCTYPE html>

        <html>

        <head>

            <meta charset="UTF-8">

            <meta
                name="viewport"
                content="width=device-width,
                initial-scale=1.0"
            >

            <title>
                Interview Completed
            </title>

            <style>

                body {

                    margin: 0;

                    font-family: Arial, sans-serif;

                    background: #f4f6f9;

                }

                .container {

                    width: 90%;

                    max-width: 700px;

                    margin: 100px auto;

                    background: white;

                    padding: 50px;

                    text-align: center;

                    border-radius: 15px;

                    box-shadow:
                        0 4px 15px
                        rgba(0,0,0,0.1);

                }

                h1 {

                    margin-bottom: 20px;

                }

                p {

                    font-size: 18px;

                    line-height: 1.6;

                    color: #555;

                }

                .button {

                    display: inline-block;

                    margin-top: 25px;

                    padding: 14px 30px;

                    background: #2563eb;

                    color: white;

                    text-decoration: none;

                    border-radius: 8px;

                    font-weight: bold;

                }

            </style>

        </head>

        <body>

            <div class="container">

                <h1>
                    🎉 Interview Completed!
                </h1>

                <p>
                    Congratulations!
                    You have completed all
                    four interview rounds.
                </p>

                <p>
                    Aptitude →
                    Technical →
                    Coding →
                    HR / Communication
                </p>

                <a
                    href="/skills"
                    class="button"
                >
                    Start Another Interview
                </a>

            </div>

        </body>

        </html>

        """
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