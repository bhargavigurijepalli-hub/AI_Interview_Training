from pathlib import Path
import json
import random

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse


# =========================================================
# APP
# =========================================================

app = FastAPI(title="SmartPrep AI")


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATE_DIR = BASE_DIR / "04 . templates"

QUESTION_FILE = (
    TEMPLATE_DIR
    / "07 . sevices"
    / "08 . data"
    / "1 . question.json"
)

CODING_QUESTION_FILE = (
    TEMPLATE_DIR
    / "07 . sevices"
    / "08 . data"
    / "2 . coding_questions.json"
)

LOGIN_TEMPLATE = TEMPLATE_DIR / "1 . login.html"
PERSONAL_TEMPLATE = TEMPLATE_DIR / "2 . personal.html"
EDUCATION_TEMPLATE = TEMPLATE_DIR / "3 . educational.html"
SKILLS_TEMPLATE = TEMPLATE_DIR / "4 . skills.html"
TEST_TEMPLATE = TEMPLATE_DIR / "5 . test_phase.html"
RESULTS_TEMPLATE = TEMPLATE_DIR / "6 . results.html"


# =========================================================
# USER DATA
# =========================================================

user_data = {
    "name": "",
    "email": "",
    "password": "",
    "age": "",
    "gender": "",
    "education": "",
    "college": "",
    "branch": "",
    "skills": [],
    "programming_language": "",
    "experience": "",
    "level": "",

    # Technical interview
    "questions": [],
    "answers": [],
    "current_question": 0,
    "question_count": 0,
    "score": 0,
    "total": 0,

    # Coding interview
    "coding_questions": [],
    "coding_answers": [],
    "current_coding_question": 0,
    "coding_score": 0,
    "coding_total": 0,
}


# =========================================================
# LEVEL MAPPING
# =========================================================

LEVEL_MAPPING = {
    "Intermediate": "intermediate",
    "Medium": "medium",
    "Advanced": "advanced",
}


# =========================================================
# SUPPORTED LANGUAGES
# =========================================================

SUPPORTED_LANGUAGES = [
    "C",
    "Java",
    "Python",
    "SQL",
    "Web Development",
]


# =========================================================
# QUESTION COUNTS
# =========================================================

ALLOWED_QUESTION_COUNTS = [
    5,
    10,
    15,
    20,
    25,
    30,
    40,
    50,
]


# =========================================================
# TEMPLATE READER
# =========================================================

def read_template(template_path: Path):

    if not template_path.exists():

        return f"""
        <!DOCTYPE html>

        <html>

        <head>
            <title>SmartPrep AI</title>
        </head>

        <body>

        <h2>
            Template Not Found
        </h2>

        <p>
            File:
            {template_path}
        </p>

        </body>

        </html>
        """

    return template_path.read_text(
        encoding="utf-8"
    )


# =========================================================
# QUESTION LOADER
# =========================================================

def load_questions():

    if not QUESTION_FILE.exists():

        return []

    try:

        with open(
            QUESTION_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        return data

    except Exception:

        return []


# =========================================================
# CODING QUESTION LOADER
# =========================================================

def load_coding_questions():

    if not CODING_QUESTION_FILE.exists():

        return []

    try:

        with open(
            CODING_QUESTION_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        return data

    except Exception:

        return []


# =========================================================
# TECHNICAL QUESTION EXTRACTION
# =========================================================

def get_questions(
    category="technical",
    level="Intermediate",
    programming_language="Python",
):

    data = load_questions()

    if not data:

        return []


    json_level = LEVEL_MAPPING.get(
        level,
        level,
    )


    # -----------------------------------------------------
    # FORMAT 1
    #
    # {
    #   "technical": {
    #       "Python": {
    #           "intermediate": [...]
    #       }
    #   }
    # }
    # -----------------------------------------------------

    if isinstance(data, dict):

        technical_data = data.get(
            category,
            data,
        )

        if isinstance(
            technical_data,
            dict,
        ):

            language_data = technical_data.get(
                programming_language,
                technical_data.get(
                    programming_language.lower(),
                    {},
                ),
            )

            if isinstance(
                language_data,
                dict,
            ):

                questions = language_data.get(
                    json_level,
                    language_data.get(
                        level,
                        [],
                    ),
                )

                if isinstance(
                    questions,
                    list,
                ):

                    return questions


            # -------------------------------------------------
            # Try language-insensitive matching
            # -------------------------------------------------

            for key, value in technical_data.items():

                if str(key).lower() == str(
                    programming_language
                ).lower():

                    if isinstance(
                        value,
                        dict,
                    ):

                        questions = value.get(
                            json_level,
                            value.get(
                                level,
                                [],
                            ),
                        )

                        if isinstance(
                            questions,
                            list,
                        ):

                            return questions


    # -----------------------------------------------------
    # FORMAT 2
    #
    # List of question objects
    # -----------------------------------------------------

    if isinstance(data, list):

        result = []

        for item in data:

            if not isinstance(
                item,
                dict,
            ):

                continue

            item_level = str(
                item.get(
                    "level",
                    "",
                )
            ).lower()

            item_language = str(
                item.get(
                    "programming_language",
                    item.get(
                        "language",
                        "",
                    ),
                )
            ).lower()

            item_category = str(
                item.get(
                    "category",
                    "technical",
                )
            ).lower()

            if (
                item_level == json_level.lower()
                and item_language == programming_language.lower()
                and item_category == category.lower()
            ):

                question_text = item.get(
                    "question",
                    item.get(
                        "text",
                        "",
                    ),
                )

                if question_text:

                    result.append(
                        question_text
                    )

        return result


    return []


# =========================================================
# CODING QUESTION EXTRACTION
# =========================================================

def get_coding_questions(
    programming_language,
):

    data = load_coding_questions()

    if not data:

        return []


    result = []


    # -----------------------------------------------------
    # FORMAT:
    #
    # {
    #   "Python": {
    #       "Easy": [...],
    #       "Medium": [...],
    #       "Hard": [...]
    #   }
    # }
    # -----------------------------------------------------

    if isinstance(data, dict):

        language_data = data.get(
            programming_language,
            data.get(
                programming_language.lower(),
                {},
            ),
        )

        if isinstance(
            language_data,
            dict,
        ):

            for difficulty in [
                "Easy",
                "Medium",
                "Hard",
            ]:

                questions = language_data.get(
                    difficulty,
                    [],
                )

                if isinstance(
                    questions,
                    list,
                ):

                    if questions:

                        selected = random.choice(
                            questions
                        )

                        if isinstance(
                            selected,
                            dict,
                        ):

                            selected = selected.get(
                                "question",
                                selected.get(
                                    "text",
                                    "",
                                ),
                            )

                        if selected:

                            result.append(
                                {
                                    "difficulty": difficulty,
                                    "question": selected,
                                }
                            )

            return result


    # -----------------------------------------------------
    # List format
    # -----------------------------------------------------

    if isinstance(data, list):

        for difficulty in [
            "Easy",
            "Medium",
            "Hard",
        ]:

            matching = []

            for item in data:

                if not isinstance(
                    item,
                    dict,
                ):

                    continue

                item_language = str(
                    item.get(
                        "programming_language",
                        item.get(
                            "language",
                            "",
                        ),
                    )
                ).lower()

                item_difficulty = str(
                    item.get(
                        "difficulty",
                        "",
                    )
                ).lower()

                if (
                    item_language
                    == programming_language.lower()
                    and item_difficulty
                    == difficulty.lower()
                ):

                    matching.append(item)


            if matching:

                selected = random.choice(
                    matching
                )

                question_text = selected.get(
                    "question",
                    selected.get(
                        "text",
                        "",
                    ),
                )

                if question_text:

                    result.append(
                        {
                            "difficulty": difficulty,
                            "question": question_text,
                        }
                    )

        return result


    return []


# =========================================================
# LOGIN
# =========================================================

@app.get(
    "/",
    response_class=HTMLResponse,
)
async def login_page():

    return read_template(
        LOGIN_TEMPLATE
    )


@app.post("/login")
async def login(

    name: str = Form(""),
    email: str = Form(""),
    password: str = Form(""),

):

    user_data["name"] = name.strip()

    user_data["email"] = email.strip()

    user_data["password"] = password.strip()

    return RedirectResponse(
        "/personal",
        status_code=303,
    )


# =========================================================
# PERSONAL
# =========================================================

@app.get(
    "/personal",
    response_class=HTMLResponse,
)
async def personal_page():

    return read_template(
        PERSONAL_TEMPLATE
    )


@app.post("/personal")
async def personal(

    age: str = Form(""),
    gender: str = Form(""),

):

    user_data["age"] = age.strip()

    user_data["gender"] = gender.strip()

    return RedirectResponse(
        "/education",
        status_code=303,
    )


# =========================================================
# EDUCATION
# =========================================================

@app.get(
    "/education",
    response_class=HTMLResponse,
)
async def education_page():

    return read_template(
        EDUCATION_TEMPLATE
    )


@app.post("/education")
async def education(

    education: str = Form(""),
    college: str = Form(""),
    branch: str = Form(""),

):

    user_data["education"] = education.strip()

    user_data["college"] = college.strip()

    user_data["branch"] = branch.strip()

    return RedirectResponse(
        "/skills",
        status_code=303,
    )


# =========================================================
# SKILLS
# =========================================================

@app.get(
    "/skills",
    response_class=HTMLResponse,
)
async def skills_page():

    return read_template(
        SKILLS_TEMPLATE
    )


@app.post("/skills")
async def skills(

    programming_language: str = Form(""),

    skills: str = Form(""),

    experience: str = Form(""),

    level: str = Form(""),

    question_count: int = Form(10),

):

    programming_language = (
        programming_language.strip()
    )

    skills = skills.strip()

    experience = experience.strip()

    level = level.strip()


    # -----------------------------------------------------
    # VALIDATE LANGUAGE
    # -----------------------------------------------------

    if programming_language not in SUPPORTED_LANGUAGES:

        return HTMLResponse(

            """
            <!DOCTYPE html>

            <html>

            <head>

            <title>
                Invalid Language
            </title>

            </head>

            <body>

            <h2>
                Invalid Programming Language
            </h2>

            <p>
                Please select C, Java, Python or SQL.
            </p>

            <a href="/skills">
                Go Back
            </a>

            </body>

            </html>
            """,

            status_code=400,
        )


    # -----------------------------------------------------
    # VALIDATE LEVEL
    # -----------------------------------------------------

    if level not in LEVEL_MAPPING:

        return HTMLResponse(

            """
            <!DOCTYPE html>

            <html>

            <head>

            <title>
                Invalid Level
            </title>

            </head>

            <body>

            <h2>
                Invalid Interview Level
            </h2>

            <p>
                Please select Intermediate,
                Medium or Advanced.
            </p>

            <a href="/skills">
                Go Back
            </a>

            </body>

            </html>
            """,

            status_code=400,
        )


    # -----------------------------------------------------
    # VALIDATE QUESTION COUNT
    # -----------------------------------------------------

    if question_count not in ALLOWED_QUESTION_COUNTS:

        question_count = 10


    # -----------------------------------------------------
    # SAVE DATA
    # -----------------------------------------------------

    user_data["skills"] = [
        item.strip()
        for item in skills.split(",")
        if item.strip()
    ]

    user_data[
        "programming_language"
    ] = programming_language

    user_data[
        "experience"
    ] = experience

    user_data[
        "level"
    ] = level

    user_data[
        "question_count"
    ] = question_count


    # -----------------------------------------------------
    # GET TECHNICAL QUESTIONS
    # -----------------------------------------------------

    questions = get_questions(

        category="technical",

        level=level,

        programming_language=(
            programming_language
        ),

    )


    # -----------------------------------------------------
    # RANDOMIZE QUESTIONS
    # -----------------------------------------------------

    random.shuffle(
        questions
    )


    # -----------------------------------------------------
    # LIMIT QUESTIONS
    # -----------------------------------------------------

    questions = questions[
        :question_count
    ]


    # -----------------------------------------------------
    # SAVE QUESTIONS
    # -----------------------------------------------------

    user_data[
        "questions"
    ] = questions

    user_data[
        "answers"
    ] = []

    user_data[
        "current_question"
    ] = 0

    user_data[
        "score"
    ] = 0

    user_data[
        "total"
    ] = len(
        questions
    )


    # -----------------------------------------------------
    # NO QUESTIONS
    # -----------------------------------------------------

    if not questions:

        return HTMLResponse(

            f"""
            <!DOCTYPE html>

            <html>

            <head>

            <title>
                No Questions Found
            </title>

            </head>

            <body>

            <h2>
                No Questions Found
            </h2>

            <p>
                Language:
                <strong>
                    {programming_language}
                </strong>
            </p>

            <p>
                Level:
                <strong>
                    {level}
                </strong>
            </p>

            <p>
                Please check your question.json file.
            </p>

            <a href="/skills">
                Go Back
            </a>

            </body>

            </html>
            """,

            status_code=404,
        )


    # -----------------------------------------------------
    # START INTERVIEW
    # -----------------------------------------------------

    return RedirectResponse(
        "/test-phase",
        status_code=303,
    )


# =========================================================
# TEST PHASE
# =========================================================

@app.get(
    "/test-phase",
    response_class=HTMLResponse,
)
async def test_phase():

    questions = user_data.get(
        "questions",
        [],
    )

    current = user_data.get(
        "current_question",
        0,
    )

    language = user_data.get(
        "programming_language",
        "",
    )

    level = user_data.get(
        "level",
        "",
    )

    total = len(
        questions
    )


    # -----------------------------------------------------
    # NO QUESTIONS
    # -----------------------------------------------------

    if not questions:

        return HTMLResponse(

            """
            <h2>
                No questions available.
            </h2>

            <a href="/skills">
                Go Back
            </a>
            """,

            status_code=404,
        )


    # -----------------------------------------------------
    # INTERVIEW FINISHED
    # -----------------------------------------------------

    if current >= total:

        return RedirectResponse(
            "/coding-phase",
            status_code=303,
        )


    question = questions[
        current
    ]


    percentage = round(
        (
            current
            / total
        ) * 100
    )


    html = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>
    SmartPrep AI Interview
</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{

    margin: 0;

    padding: 30px;

    font-family:
        "Segoe UI",
        Arial,
        sans-serif;

    background:
        #0f172a;

    color:
        #f8fafc;
}}

.container {{

    width: 100%;

    max-width:
        850px;

    margin:
        auto;

    background:
        #1e293b;

    padding:
        35px;

    border-radius:
        15px;

    box-shadow:
        0 15px 40px
        rgba(0,0,0,0.4);
}}

.header {{

    border-bottom:
        1px solid #475569;

    padding-bottom:
        20px;

    margin-bottom:
        25px;
}}

.header h1 {{

    margin-top: 0;
}}

.info {{

    color:
        #cbd5e1;

    line-height:
        1.8;
}}

.progress-container {{

    width:
        100%;

    height:
        8px;

    background:
        #334155;

    border-radius:
        10px;

    margin:
        20px 0;
}}

.progress {{

    height:
        100%;

    width:
        {percentage}%;

    background:
        #38bdf8;

    border-radius:
        10px;
}}

.question-card {{

    background:
        #0f172a;

    padding:
        30px;

    border-radius:
        12px;

    border:
        1px solid #334155;
}}

.question-number {{

    color:
        #38bdf8;

    font-weight:
        bold;

    margin-bottom:
        15px;
}}

.question-text {{

    font-size:
        20px;

    line-height:
        1.6;

    margin-bottom:
        25px;
}}

textarea {{

    width:
        100%;

    min-height:
        220px;

    padding:
        15px;

    resize:
        vertical;

    background:
        #1e293b;

    color:
        white;

    border:
        1px solid #475569;

    border-radius:
        8px;

    font-size:
        16px;

    outline:
        none;
}}

textarea:focus {{

    border-color:
        #38bdf8;
}}

button {{

    width:
        100%;

    margin-top:
        20px;

    padding:
        15px;

    border:
        none;

    border-radius:
        8px;

    background:
        #38bdf8;

    color:
        #0f172a;

    font-size:
        17px;

    font-weight:
        bold;

    cursor:
        pointer;
}}

button:hover {{

    background:
        #0ea5e9;
}}

</style>

</head>

<body>

<div class="container">

<div class="header">

<h1>
    💻 SmartPrep AI Interview
</h1>

<div class="info">

Programming Language:
<strong>
    {language}
</strong>

<br>

Interview Level:
<strong>
    {level}
</strong>

<br>

Question:
<strong>
    {current + 1} / {total}
</strong>

</div>

<div class="progress-container">

<div class="progress"></div>

</div>

</div>

<div class="question-card">

<div class="question-number">

Question {current + 1}

</div>

<div class="question-text">

{question}

</div>

<form
    method="post"
    action="/test-phase"
>

<textarea
    name="answer"
    placeholder="Type your answer here..."
    required
></textarea>

<button type="submit">

    Submit Answer

</button>

</form>

</div>

</div>

</body>

</html>
"""


    return HTMLResponse(
        html
    )


# =========================================================
# SUBMIT TECHNICAL QUESTION
# =========================================================

@app.post("/test-phase")
async def submit_test(

    answer: str = Form(""),

):

    questions = user_data.get(
        "questions",
        [],
    )

    current = user_data.get(
        "current_question",
        0,
    )


    if current >= len(
        questions
    ):

        return RedirectResponse(
            "/coding-phase",
            status_code=303,
        )


    answer = answer.strip()


    user_data[
        "answers"
    ].append(
        answer
    )


    # -----------------------------------------------------
    # BASIC SCORE
    #
    # Counts answered questions only.
    # No AI evaluation.
    # -----------------------------------------------------

    if answer:

        user_data[
            "score"
        ] += 1


    user_data[
        "current_question"
    ] += 1


    # -----------------------------------------------------
    # MORE TECHNICAL QUESTIONS
    # -----------------------------------------------------

    if user_data[
        "current_question"
    ] < len(questions):

        return RedirectResponse(
            "/test-phase",
            status_code=303,
        )


    # -----------------------------------------------------
    # TECHNICAL INTERVIEW FINISHED
    # -----------------------------------------------------

    return RedirectResponse(
        "/coding-phase",
        status_code=303,
    )


# =========================================================
# CODING PHASE
# =========================================================

@app.get(
    "/coding-phase",
    response_class=HTMLResponse,
)
async def coding_phase():

    language = user_data.get(
        "programming_language",
        "",
    )


    # -----------------------------------------------------
    # LOAD CODING QUESTIONS
    # -----------------------------------------------------

    coding_questions = get_coding_questions(
        language
    )


    # -----------------------------------------------------
    # IF NO CODING QUESTIONS
    # -----------------------------------------------------

    if not coding_questions:

        return RedirectResponse(
            "/results",
            status_code=303,
        )


    user_data[
        "coding_questions"
    ] = coding_questions

    user_data[
        "coding_answers"
    ] = []

    user_data[
        "current_coding_question"
    ] = 0

    user_data[
        "coding_score"
    ] = 0

    user_data[
        "coding_total"
    ] = len(
        coding_questions
    )


    return RedirectResponse(
        "/coding-question",
        status_code=303,
    )


# =========================================================
# CODING QUESTION
# =========================================================

@app.get(
    "/coding-question",
    response_class=HTMLResponse,
)
async def coding_question():

    questions = user_data.get(
        "coding_questions",
        [],
    )

    current = user_data.get(
        "current_coding_question",
        0,
    )

    language = user_data.get(
        "programming_language",
        "",
    )

    total = len(
        questions
    )


    if not questions:

        return RedirectResponse(
            "/results",
            status_code=303,
        )


    if current >= total:

        return RedirectResponse(
            "/results",
            status_code=303,
        )


    item = questions[
        current
    ]


    difficulty = item.get(
        "difficulty",
        "",
    )

    question = item.get(
        "question",
        "",
    )


    percentage = round(
        (
            current
            / total
        ) * 100
    )


    html = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>
    SmartPrep AI Coding
</title>

<style>

* {{
    box-sizing:
        border-box;
}}

body {{

    margin:
        0;

    padding:
        30px;

    font-family:
        "Segoe UI",
        Arial,
        sans-serif;

    background:
        #0f172a;

    color:
        #f8fafc;
}}

.container {{

    max-width:
        850px;

    margin:
        auto;

    background:
        #1e293b;

    padding:
        35px;

    border-radius:
        15px;

    box-shadow:
        0 15px 40px
        rgba(0,0,0,0.4);
}}

.header {{

    border-bottom:
        1px solid #475569;

    padding-bottom:
        20px;

    margin-bottom:
        25px;
}}

.info {{

    color:
        #cbd5e1;

    line-height:
        1.8;
}}

.badge {{

    display:
        inline-block;

    padding:
        6px 12px;

    border-radius:
        20px;

    background:
        #334155;

    color:
        #38bdf8;

    font-weight:
        bold;

    margin:
        10px 0 20px 0;
}}

.progress-container {{

    width:
        100%;

    height:
        8px;

    background:
        #334155;

    border-radius:
        10px;

    margin:
        20px 0;
}}

.progress {{

    height:
        100%;

    width:
        {percentage}%;

    background:
        #38bdf8;

    border-radius:
        10px;
}}

.question-card {{

    background:
        #0f172a;

    padding:
        30px;

    border-radius:
        12px;

    border:
        1px solid #334155;
}}

.question-text {{

    font-size:
        20px;

    line-height:
        1.6;

    margin-bottom:
        25px;
}}

textarea {{

    width:
        100%;

    min-height:
        300px;

    padding:
        15px;

    resize:
        vertical;

    background:
        #1e293b;

    color:
        white;

    border:
        1px solid #475569;

    border-radius:
        8px;

    font-family:
        Consolas,
        monospace;

    font-size:
        15px;

    outline:
        none;
}}

textarea:focus {{

    border-color:
        #38bdf8;
}}

button {{

    width:
        100%;

    margin-top:
        20px;

    padding:
        15px;

    border:
        none;

    border-radius:
        8px;

    background:
        #38bdf8;

    color:
        #0f172a;

    font-size:
        17px;

    font-weight:
        bold;

    cursor:
        pointer;
}}

button:hover {{

    background:
        #0ea5e9;
}}

</style>

</head>

<body>

<div class="container">

<div class="header">

<h1>
    💻 Coding Interview
</h1>

<div class="info">

Programming Language:
<strong>
    {language}
</strong>

<br>

Coding Question:
<strong>
    {current + 1} / {total}
</strong>

</div>

<div class="badge">
    {difficulty}
</div>

<div class="progress-container">

<div class="progress"></div>

</div>

</div>

<div class="question-card">

<div class="question-text">

{question}

</div>

<form
    method="post"
    action="/coding-question"
>

<textarea
    name="answer"
    placeholder="Write your solution/code here..."
    required
></textarea>

<button type="submit">

    Submit Coding Answer

</button>

</form>

</div>

</div>

</body>

</html>
"""


    return HTMLResponse(
        html
    )


# =========================================================
# SUBMIT CODING QUESTION
# =========================================================

@app.post("/coding-question")
async def submit_coding_question(

    answer: str = Form(""),

):

    questions = user_data.get(
        "coding_questions",
        [],
    )

    current = user_data.get(
        "current_coding_question",
        0,
    )


    if current >= len(
        questions
    ):

        return RedirectResponse(
            "/results",
            status_code=303,
        )


    answer = answer.strip()


    user_data[
        "coding_answers"
    ].append(
        answer
    )


    # -----------------------------------------------------
    # BASIC CODING SCORE
    #
    # Counts submitted answers.
    # No AI evaluation.
    # -----------------------------------------------------

    if answer:

        user_data[
            "coding_score"
        ] += 1


    user_data[
        "current_coding_question"
    ] += 1


    if user_data[
        "current_coding_question"
    ] < len(questions):

        return RedirectResponse(
            "/coding-question",
            status_code=303,
        )


    return RedirectResponse(
        "/results",
        status_code=303,
    )


# =========================================================
# RESULTS
# =========================================================

@app.get(
    "/results",
    response_class=HTMLResponse,
)
async def results():

    name = user_data.get(
        "name",
        "",
    )

    language = user_data.get(
        "programming_language",
        "",
    )

    level = user_data.get(
        "level",
        "",
    )

    technical_score = user_data.get(
        "score",
        0,
    )

    technical_total = user_data.get(
        "total",
        0,
    )

    coding_score = user_data.get(
        "coding_score",
        0,
    )

    coding_total = user_data.get(
        "coding_total",
        0,
    )


    # -----------------------------------------------------
    # TECHNICAL PERCENTAGE
    # -----------------------------------------------------

    if technical_total > 0:

        technical_percentage = round(
            technical_score
            / technical_total
            * 100,
            2,
        )

    else:

        technical_percentage = 0


    # -----------------------------------------------------
    # CODING PERCENTAGE
    # -----------------------------------------------------

    if coding_total > 0:

        coding_percentage = round(
            coding_score
            / coding_total
            * 100,
            2,
        )

    else:

        coding_percentage = 0


    # -----------------------------------------------------
    # OVERALL
    # -----------------------------------------------------

    total_score = (
        technical_score
        + coding_score
    )

    total_questions = (
        technical_total
        + coding_total
    )


    if total_questions > 0:

        overall_percentage = round(
            total_score
            / total_questions
            * 100,
            2,
        )

    else:

        overall_percentage = 0


    # -----------------------------------------------------
    # FEEDBACK
    # -----------------------------------------------------

    if overall_percentage >= 80:

        feedback = (
            "Excellent performance."
        )

    elif overall_percentage >= 60:

        feedback = (
            "Good performance."
        )

    elif overall_percentage >= 40:

        feedback = (
            "Average performance. "
            "Keep practicing."
        )

    else:

        feedback = (
            "Needs improvement. "
            "Practice more."
        )


    return HTMLResponse(

        f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>
    SmartPrep AI Results
</title>

<style>

body {{

    margin:
        0;

    padding:
        40px;

    font-family:
        "Segoe UI",
        Arial,
        sans-serif;

    background:
        #0f172a;

    color:
        #f8fafc;
}}

.container {{

    max-width:
        750px;

    margin:
        auto;

    padding:
        40px;

    background:
        #1e293b;

    border-radius:
        15px;

    text-align:
        center;

    box-shadow:
        0 15px 40px
        rgba(0,0,0,0.4);
}}

.score {{

    font-size:
        60px;

    font-weight:
        bold;

    color:
        #38bdf8;

    margin:
        30px 0;
}}

.info {{

    margin:
        12px 0;

    color:
        #cbd5e1;
}}

.section {{

    margin-top:
        25px;

    padding:
        20px;

    background:
        #0f172a;

    border-radius:
        10px;
}}

.section h3 {{

    margin-top:
        0;
}}

button {{

    margin-top:
        25px;

    padding:
        13px 22px;

    border:
        none;

    border-radius:
        7px;

    background:
        #38bdf8;

    color:
        #0f172a;

    font-size:
        15px;

    font-weight:
        bold;

    cursor:
        pointer;
}}

button:hover {{

    background:
        #0ea5e9;
}}

</style>

</head>

<body>

<div class="container">

<h1>
    🎯 Interview Results
</h1>

<div class="info">

Candidate:
<strong>
    {name}
</strong>

</div>

<div class="info">

Programming Language:
<strong>
    {language}
</strong>

</div>

<div class="info">

Interview Level:
<strong>
    {level}
</strong>

</div>

<div class="score">

{overall_percentage}%

</div>

<div class="section">

<h3>
    Technical Interview
</h3>

<p>

Score:
<strong>
    {technical_score} / {technical_total}
</strong>

</p>

<p>

Percentage:
<strong>
    {technical_percentage}%
</strong>

</p>

</div>

<div class="section">

<h3>
    Coding Interview
</h3>

<p>

Score:
<strong>
    {coding_score} / {coding_total}
</strong>

</p>

<p>

Percentage:
<strong>
    {coding_percentage}%
</strong>

</p>

</div>

<div class="section">

<h3>
    Overall Performance
</h3>

<p>

Score:
<strong>
    {total_score} / {total_questions}
</strong>

</p>

<p>

{feedback}

</p>

</div>

<form
    action="/skills"
    method="get"
>

<button type="submit">

    Start Another Interview

</button>

</form>

</div>

</body>

</html>
"""

    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
async def health():

    return {

        "status": "ok",

        "application": "SmartPrep AI",

        "question_file":
            str(QUESTION_FILE),

        "question_file_exists":
            QUESTION_FILE.exists(),

        "coding_question_file":
            str(CODING_QUESTION_FILE),

        "coding_question_file_exists":
            CODING_QUESTION_FILE.exists(),

    }