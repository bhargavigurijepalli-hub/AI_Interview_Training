from pathlib import Path
import json
import random
import re
import html

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse

app = FastAPI(title="SmartPrep AI")

# =========================================================
# PATHS
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
INTERVIEW_TEMPLATE = TEMPLATE_DIR / "7 . interview.html"

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
    "aptitude": 20,
    "technical": 20,
    "coding": 5,
    "hr": 20
}

# =========================================================
# USER DATA
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
# EXAM STATE
# =========================================================

exam_state = {
    "started": False,
    "aptitude": [],
    "technical": [],
    "coding": [],
    "hr": [],
    "responses": {},
    "scores": {}
}


# =========================================================
# FILE HELPERS
# =========================================================

def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def load_template(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
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
    return HTMLResponse(content=load_template(file_path))


def escape_html(value):
    return html.escape(str(value or ""))


# =========================================================
# LEVEL HELPERS
# =========================================================

def general_level(level):
    mapping = {
        "Intermediate": "intermediate",
        "Medium": "medium",
        "Advanced": "advanced"
    }
    return mapping.get(level, "intermediate")


def technical_level(level):
    mapping = {
        "Intermediate": "intermediate",
        "Medium": "medium",
        "Advanced": "advanced"
    }
    return mapping.get(level, "intermediate")


def coding_level(level):
    mapping = {
        "Intermediate": "Easy",
        "Medium": "Medium",
        "Advanced": "Hard"
    }
    return mapping.get(level, "Easy")


# =========================================================
# DATA NORMALIZATION
# =========================================================

def normalize_level_keys(data):
    """
    Handles the current question.json inconsistency where some
    sections use 'hard' while answers.json uses 'medium'.

    We keep the user's selected level as the preferred level.
    """

    if not isinstance(data, dict):
        return data

    normalized = {}

    for key, value in data.items():

        if key == "hard" and "medium" not in data:
            normalized["medium"] = value
        else:
            normalized[key] = value

    return normalized


# =========================================================
# QUESTION/ANSWER PAIRING
# =========================================================

def build_pairs(questions, answers):
    """
    IMPORTANT:
    Questions and answers are paired BEFORE randomization.
    This prevents a shuffled question from receiving the wrong answer.
    """

    pairs = []

    for index, question in enumerate(questions):

        answer = ""

        if index < len(answers):
            answer = answers[index]

        pairs.append({
            "question": question,
            "answer": answer
        })

    return pairs


def get_level_pairs(question_data, answer_data, level):
    """
    Return question-answer pairs for selected level.
    """

    selected = general_level(level)

    question_data = normalize_level_keys(question_data)
    answer_data = normalize_level_keys(answer_data)

    questions = question_data.get(selected, [])
    answers = answer_data.get(selected, [])

    return build_pairs(questions, answers)


def fill_random_pairs(
    selected_pairs,
    all_pairs,
    required_count
):
    """
    Select randomly from the selected difficulty first.

    If the selected difficulty does not contain enough questions,
    remaining questions are taken from other levels.

    No new questions are generated.
    """

    selected_copy = selected_pairs.copy()
    random.shuffle(selected_copy)

    result = selected_copy[:required_count]

    if len(result) >= required_count:
        return result

    used_questions = {
        item["question"]
        for item in result
    }

    remaining = [
        item
        for item in all_pairs
        if item["question"] not in used_questions
    ]

    random.shuffle(remaining)

    needed = required_count - len(result)

    result.extend(remaining[:needed])

    return result


# =========================================================
# APTITUDE
# =========================================================

def get_aptitude_exam_questions(level):
    questions_data = load_json(QUESTION_FILE)
    answers_data = load_json(ANSWERS_FILE)

    question_section = questions_data.get("aptitude", {})
    answer_section = answers_data.get("aptitude", {})

    selected = get_level_pairs(
        question_section,
        answer_section,
        level
    )

    all_pairs = []

    for level_key in ["intermediate", "medium", "advanced", "hard"]:
        questions = question_section.get(level_key, [])
        answers = answer_section.get(level_key, [])

        all_pairs.extend(
            build_pairs(questions, answers)
        )

    return fill_random_pairs(
        selected,
        all_pairs,
        ROUND_COUNTS["aptitude"]
    )


# =========================================================
# TECHNICAL
# =========================================================

def get_technical_exam_questions(level, language):
    questions_data = load_json(QUESTION_FILE)
    answers_data = load_json(ANSWERS_FILE)

    question_section = (
        questions_data
        .get("technical", {})
        .get(language, {})
    )

    answer_section = (
        answers_data
        .get("technical", {})
        .get(language, {})
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
        questions = question_section.get(level_key, [])
        answers = answer_section.get(level_key, [])

        all_pairs.extend(
            build_pairs(questions, answers)
        )

    return fill_random_pairs(
        selected,
        all_pairs,
        ROUND_COUNTS["technical"]
    )


# =========================================================
# CODING
# =========================================================

def get_coding_exam_questions(level, language):
    question_data = load_json(CODING_QUESTION_FILE)
    answer_data = load_json(ANSWERS_FILE)

    coding_questions = question_data.get(language, {})
    coding_answers = (
        answer_data
        .get("coding", {})
        .get(language, {})
    )

    selected_level = coding_level(level)

    selected_questions = coding_questions.get(
        selected_level,
        []
    )

    selected_answers = coding_answers.get(
        selected_level,
        []
    )

    selected_pairs = build_pairs(
        selected_questions,
        selected_answers
    )

    # Coding has 3 questions at each difficulty in
    # the current question bank.
    #
    # We need 5 questions, so fill from other difficulties
    # when necessary.

    all_pairs = []

    for difficulty in ["Easy", "Medium", "Hard"]:

        questions = coding_questions.get(
            difficulty,
            []
        )

        answers = coding_answers.get(
            difficulty,
            []
        )

        all_pairs.extend(
            build_pairs(questions, answers)
        )

    return fill_random_pairs(
        selected_pairs,
        all_pairs,
        ROUND_COUNTS["coding"]
    )


# =========================================================
# HR / COMMUNICATION
# =========================================================

def get_hr_exam_questions(level):
    questions_data = load_json(QUESTION_FILE)
    answers_data = load_json(ANSWERS_FILE)

    question_section = questions_data.get(
        "communication",
        {}
    )

    answer_section = answers_data.get(
        "communication",
        {}
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

        questions = question_section.get(
            level_key,
            []
        )

        answers = answer_section.get(
            level_key,
            []
        )

        all_pairs.extend(
            build_pairs(questions, answers)
        )

    return fill_random_pairs(
        selected,
        all_pairs,
        ROUND_COUNTS["hr"]
    )


# =========================================================
# BASIC ANSWER EVALUATION
# =========================================================

def normalize_text(text):
    text = str(text or "").lower().strip()

    text = re.sub(
        r"[^a-z0-9\s.%\-]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


def extract_numbers(text):
    numbers = re.findall(
        r"-?\d+(?:\.\d+)?",
        str(text or "")
    )

    result = []

    for value in numbers:
        try:
            result.append(float(value))
        except ValueError:
            pass

    return result


def evaluate_answer(candidate_answer, correct_answer, round_name):
    """
    Basic local evaluator.

    This is NOT an LLM evaluator.
    It provides a useful local score without exposing answers
    to the browser.

    A real semantic AI evaluator can be integrated later.
    """

    candidate = normalize_text(candidate_answer)
    correct = normalize_text(correct_answer)

    if not candidate:
        return {
            "score": 0,
            "feedback": "No answer was provided."
        }

    if not correct:
        return {
            "score": 50,
            "feedback": "Answer recorded for review."
        }

    # Exact match
    if candidate == correct:
        return {
            "score": 100,
            "feedback": "Excellent. Your answer matches the expected answer."
        }

    # Numerical comparison for aptitude
    if round_name == "aptitude":

        candidate_numbers = extract_numbers(
            candidate_answer
        )

        correct_numbers = extract_numbers(
            correct_answer
        )

        if candidate_numbers and correct_numbers:

            for candidate_number in candidate_numbers:

                for correct_number in correct_numbers:

                    if abs(
                        candidate_number -
                        correct_number
                    ) < 0.01:

                        return {
                            "score": 100,
                            "feedback": (
                                "Correct result. "
                                "Your numerical answer matches."
                            )
                        }

    # Keyword evaluation
    correct_words = set(
        word
        for word in correct.split()
        if len(word) >= 4
    )

    candidate_words = set(
        word
        for word in candidate.split()
        if len(word) >= 4
    )

    if correct_words:

        matched = len(
            correct_words.intersection(
                candidate_words
            )
        )

        ratio = matched / len(correct_words)

        if ratio >= 0.70:
            return {
                "score": 90,
                "feedback": (
                    "Strong answer. Most important concepts "
                    "were identified."
                )
            }

        if ratio >= 0.45:
            return {
                "score": 70,
                "feedback": (
                    "Good attempt. Some important concepts "
                    "were identified."
                )
            }

        if ratio >= 0.20:
            return {
                "score": 50,
                "feedback": (
                    "Partial answer. Try to explain more "
                    "of the key concepts."
                )
            }

    return {
        "score": 30,
        "feedback": (
            "Your answer was recorded, but it does not "
            "closely match the expected key concepts."
        )
    }


# =========================================================
# EXAM START
# =========================================================

def start_exam():
    global exam_state

    level = user_data["level"]
    language = user_data["programming_language"]

    aptitude = get_aptitude_exam_questions(
        level
    )

    technical = get_technical_exam_questions(
        level,
        language
    )

    coding = get_coding_exam_questions(
        level,
        language
    )

    hr = get_hr_exam_questions(
        level
    )

    exam_state = {
        "started": True,
        "aptitude": aptitude,
        "technical": technical,
        "coding": coding,
        "hr": hr,
        "responses": {},
        "scores": {}
    }

    return exam_state


# =========================================================
# FRONTEND QUESTION DATA
# =========================================================

def public_question_list(items, round_name):
    """
    IMPORTANT:
    Correct answers are intentionally NOT returned.
    """

    result = []

    for index, item in enumerate(items):

        result.append({
            "id": f"{round_name}_{index}",
            "round": round_name,
            "number": index + 1,
            "question": item["question"],
            "type": (
                "coding"
                if round_name == "coding"
                else "text"
            )
        })

    return result


def get_all_public_questions():
    return {
        "aptitude": public_question_list(
            exam_state["aptitude"],
            "aptitude"
        ),
        "technical": public_question_list(
            exam_state["technical"],
            "technical"
        ),
        "coding": public_question_list(
            exam_state["coding"],
            "coding"
        ),
        "hr": public_question_list(
            exam_state["hr"],
            "hr"
        )
    }


# =========================================================
# PAGES
# =========================================================

@app.get("/", response_class=HTMLResponse)
def home():
    return render_template(LOGIN_TEMPLATE)


@app.post("/login")
def login(
    email: str = Form(""),
    password: str = Form("")
):
    return RedirectResponse(
        url="/personal",
        status_code=303
    )


@app.get("/personal", response_class=HTMLResponse)
def personal():
    return render_template(PERSONAL_TEMPLATE)


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


@app.get("/education", response_class=HTMLResponse)
def education():
    return render_template(EDUCATION_TEMPLATE)


@app.get("/educational")
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
    user_data["graduation_year"] = graduation_year

    return RedirectResponse(
        url="/skills",
        status_code=303
    )


@app.get("/skills", response_class=HTMLResponse)
def skills():
    return render_template(SKILLS_TEMPLATE)


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
        url="/interview",
        status_code=303
    )


# =========================================================
# INTERVIEW
# =========================================================

@app.get(
    "/interview",
    response_class=HTMLResponse
)
def interview():

    start_exam()

    template = load_template(
        INTERVIEW_TEMPLATE
    )

    return HTMLResponse(
        content=template
    )


@app.get("/api/exam")
def api_exam():

    if not exam_state["started"]:
        start_exam()

    return JSONResponse({
        "candidate": {
            "name": user_data["name"],
            "level": user_data["level"],
            "language": user_data[
                "programming_language"
            ]
        },
        "counts": ROUND_COUNTS,
        "questions": get_all_public_questions()
    })


# =========================================================
# SUBMIT ANSWER
# =========================================================

@app.post("/api/answer")
async def submit_answer(data: dict):

    round_name = data.get(
        "round",
        ""
    )

    question_index = data.get(
        "question_index",
        0
    )

    candidate_answer = data.get(
        "answer",
        ""
    )

    if round_name not in exam_state:
        return JSONResponse(
            {
                "success": False,
                "message": "Invalid round."
            },
            status_code=400
        )

    try:
        question_index = int(
            question_index
        )
    except (ValueError, TypeError):
        question_index = 0

    questions = exam_state.get(
        round_name,
        []
    )

    if (
        question_index < 0
        or question_index >= len(questions)
    ):
        return JSONResponse(
            {
                "success": False,
                "message": "Invalid question."
            },
            status_code=400
        )

    item = questions[question_index]

    evaluation = evaluate_answer(
        candidate_answer,
        item.get("answer", ""),
        round_name
    )

    key = f"{round_name}_{question_index}"

    exam_state["responses"][key] = (
        candidate_answer
    )

    exam_state["scores"][key] = (
        evaluation["score"]
    )

    return JSONResponse({
        "success": True,
        "score": evaluation["score"],
        "feedback": evaluation["feedback"]
    })


# =========================================================
# FINISH ROUND
# =========================================================

@app.post("/api/finish-round")
async def finish_round(data: dict):

    round_name = data.get(
        "round",
        ""
    )

    if round_name not in ROUND_COUNTS:
        return JSONResponse(
            {
                "success": False,
                "message": "Invalid round."
            },
            status_code=400
        )

    scores = []

    for key, score in exam_state[
        "scores"
    ].items():

        if key.startswith(
            round_name + "_"
        ):
            scores.append(score)

    average = (
        sum(scores) / len(scores)
        if scores
        else 0
    )

    return JSONResponse({
        "success": True,
        "round": round_name,
        "answered": len(scores),
        "total": ROUND_COUNTS[
            round_name
        ],
        "score": round(average, 2)
    })


# =========================================================
# RESULTS
# =========================================================

@app.get(
    "/results",
    response_class=HTMLResponse
)
def results():

    round_scores = {}

    for round_name in ROUND_COUNTS:

        scores = []

        for key, score in exam_state[
            "scores"
        ].items():

            if key.startswith(
                round_name + "_"
            ):
                scores.append(score)

        if scores:
            round_scores[round_name] = round(
                sum(scores) / len(scores),
                2
            )
        else:
            round_scores[round_name] = 0

    available_scores = [
        value
        for value in round_scores.values()
        if value > 0
    ]

    overall = (
        round(
            sum(available_scores)
            / len(available_scores),
            2
        )
        if available_scores
        else 0
    )

    name = escape_html(
        user_data["name"]
    )

    rows = ""

    labels = {
        "aptitude": "Aptitude",
        "technical": "Technical",
        "coding": "Coding",
        "hr": "HR / Communication"
    }

    for key in ROUND_COUNTS:

        rows += f"""
        <tr>
            <td>{labels[key]}</td>
            <td>
                {round_scores[key]}%
            </td>
        </tr>
        """

    page = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>SmartPrep AI - Results</title>

        <style>
            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f4f6f9;
            }}

            .container {{
                max-width: 900px;
                margin: 50px auto;
                background: white;
                padding: 35px;
                border-radius: 16px;
                box-shadow:
                    0 5px 25px
                    rgba(0,0,0,0.10);
            }}

            h1 {{
                margin-top: 0;
            }}

            .overall {{
                text-align: center;
                padding: 25px;
                background: #eef2ff;
                border-radius: 12px;
                margin: 25px 0;
            }}

            .overall strong {{
                font-size: 48px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}

            th, td {{
                padding: 15px;
                border-bottom: 1px solid #ddd;
                text-align: left;
            }}

            th {{
                background: #f3f4f6;
            }}

            .button {{
                display: inline-block;
                margin-top: 25px;
                padding: 13px 22px;
                background: #2563eb;
                color: white;
                text-decoration: none;
                border-radius: 8px;
            }}
        </style>
    </head>

    <body>

        <div class="container">

            <h1>SmartPrep AI — Final Results</h1>

            <p>
                Candidate:
                <strong>{name}</strong>
            </p>

            <div class="overall">
                <div>Overall Score</div>
                <strong>{overall}%</strong>
            </div>

            <h2>Round Performance</h2>

            <table>
                <thead>
                    <tr>
                        <th>Round</th>
                        <th>Score</th>
                    </tr>
                </thead>

                <tbody>
                    {rows}
                </tbody>
            </table>

            <a
                class="button"
                href="/interview"
            >
                Start New Interview
            </a>

        </div>

    </body>
    </html>
    """

    return HTMLResponse(
        content=page
    )


# =========================================================
# OLD ROUTES
# =========================================================

@app.get("/aptitude")
def old_aptitude():
    return RedirectResponse(
        url="/interview",
        status_code=303
    )


@app.get("/technical")
def old_technical():
    return RedirectResponse(
        url="/interview",
        status_code=303
    )


@app.get("/test-phase")
def old_test_phase():
    return RedirectResponse(
        url="/interview",
        status_code=303
    )


@app.get("/coding")
def old_coding():
    return RedirectResponse(
        url="/interview",
        status_code=303
    )


@app.get("/coding-phase")
def old_coding_phase():
    return RedirectResponse(
        url="/interview",
        status_code=303
    )


@app.get("/hr")
def old_hr():
    return RedirectResponse(
        url="/interview",
        status_code=303
    )


@app.get("/completed")
def completed():
    return RedirectResponse(
        url="/results",
        status_code=303
    )


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health():
    return {
        "status": "ok",
        "application": "SmartPrep AI"
    }