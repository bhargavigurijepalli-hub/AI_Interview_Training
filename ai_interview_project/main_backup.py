from pathlib import Path
import json
import re
import random

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates


# =========================================================
# APP
# =========================================================

app = FastAPI(title="SmartPrep AI")


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_DIR = BASE_DIR / "templates"
DATA_DIR = BASE_DIR / "data"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


# =========================================================
# DATA FILES
# =========================================================

QUESTION_FILES = [
    DATA_DIR / "questions.json",
    DATA_DIR / "question.json",
    BASE_DIR / "questions.json",
    BASE_DIR / "question.json",
]


# =========================================================
# EXAM STATE
# =========================================================

exam_state = {
    "round": "",
    "level": "",
    "language": "",
    "questions": [],
    "current_question": 0,
    "responses": {},
    "scores": {},
    "round_scores": {},
}


# =========================================================
# BASIC HELPERS
# =========================================================

def normalize_text(text):
    """
    Convert text into a normalized form for comparison.
    """

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
    """
    Extract integer/decimal numbers from text.
    """

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


# =========================================================
# ANSWER EVALUATOR
# =========================================================

def evaluate_answer(
    candidate_answer,
    correct_answer,
    round_name
):
    """
    Evaluate candidate answer.

    Scoring:
        100 = Correct
        90  = Strong technical/HR answer
        70  = Good partial answer
        40  = Weak partial answer
        0   = Wrong answer

    IMPORTANT:
    Attempting an answer does NOT automatically give marks.
    """

    candidate = normalize_text(candidate_answer)
    correct = normalize_text(correct_answer)

    round_name = str(
        round_name or ""
    ).lower().strip()


    # -----------------------------------------------------
    # EMPTY ANSWER
    # -----------------------------------------------------

    if not candidate:

        return {
            "score": 0,
            "feedback": (
                "No answer was provided. "
                "Score: 0."
            )
        }


    # -----------------------------------------------------
    # EXPECTED ANSWER MISSING
    # -----------------------------------------------------

    if not correct:

        return {
            "score": 0,
            "feedback": (
                "Expected answer is unavailable. "
                "Score: 0."
            )
        }


    # -----------------------------------------------------
    # EXACT MATCH
    # -----------------------------------------------------

    if candidate == correct:

        return {
            "score": 100,
            "feedback": (
                "Correct answer. Excellent."
            )
        }


    # =====================================================
    # APTITUDE
    # =====================================================

    if round_name == "aptitude":

        candidate_numbers = extract_numbers(
            candidate_answer
        )

        correct_numbers = extract_numbers(
            correct_answer
        )

        if candidate_numbers and correct_numbers:

            candidate_number = candidate_numbers[-1]

            correct_number = correct_numbers[-1]

            if abs(
                candidate_number -
                correct_number
            ) < 0.01:

                return {
                    "score": 100,
                    "feedback": (
                        "Correct numerical answer."
                    )
                }

        return {
            "score": 0,
            "feedback": (
                "Incorrect answer. "
                "The numerical result is wrong. "
                "Score: 0."
            )
        }


    # =====================================================
    # CODING
    # =====================================================

    if round_name == "coding":

        # Exact normalized match already checked above.
        #
        # For coding questions, require meaningful
        # overlap instead of giving marks merely
        # because code was submitted.

        correct_words = {
            word
            for word in correct.split()
            if len(word) >= 4
        }

        candidate_words = {
            word
            for word in candidate.split()
            if len(word) >= 4
        }

        if not correct_words:

            return {
                "score": 0,
                "feedback": (
                    "Unable to evaluate coding answer. "
                    "Score: 0."
                )
            }

        matched_words = (
            correct_words.intersection(
                candidate_words
            )
        )

        ratio = (
            len(matched_words) /
            len(correct_words)
        )

        if ratio >= 0.75:

            return {
                "score": 90,
                "feedback": (
                    "Strong coding answer. "
                    "Most important concepts were present."
                )
            }

        if ratio >= 0.50:

            return {
                "score": 70,
                "feedback": (
                    "Good coding attempt, "
                    "but some important parts are missing."
                )
            }

        if ratio >= 0.35:

            return {
                "score": 40,
                "feedback": (
                    "Partially correct coding answer. "
                    "More important concepts are required."
                )
            }

        return {
            "score": 0,
            "feedback": (
                "Incorrect coding answer. "
                "The submitted solution does not match "
                "enough of the expected solution. "
                "Score: 0."
            )
        }


    # =====================================================
    # TECHNICAL / HR
    # =====================================================

    correct_words = {
        word
        for word in correct.split()
        if len(word) >= 4
    }

    candidate_words = {
        word
        for word in candidate.split()
        if len(word) >= 4
    }


    if not correct_words:

        return {
            "score": 0,
            "feedback": (
                "Unable to evaluate the answer. "
                "Score: 0."
            )
        }


    matched_words = (
        correct_words.intersection(
            candidate_words
        )
    )

    matched = len(matched_words)

    total = len(correct_words)

    ratio = matched / total


    # -----------------------------------------------------
    # STRONG ANSWER
    # -----------------------------------------------------

    if ratio >= 0.75:

        return {
            "score": 90,
            "feedback": (
                "Strong answer. "
                "Most important concepts were identified."
            )
        }


    # -----------------------------------------------------
    # GOOD ANSWER
    # -----------------------------------------------------

    if ratio >= 0.50:

        return {
            "score": 70,
            "feedback": (
                "Good answer. "
                "Some important concepts were identified, "
                "but the explanation can be improved."
            )
        }


    # -----------------------------------------------------
    # PARTIAL ANSWER
    # -----------------------------------------------------

    if ratio >= 0.35:

        return {
            "score": 40,
            "feedback": (
                "Partially relevant answer. "
                "More important concepts are required."
            )
        }


    # -----------------------------------------------------
    # WRONG ANSWER
    # -----------------------------------------------------

    return {
        "score": 0,
        "feedback": (
            "Incorrect answer. "
            "Your response does not contain enough "
            "of the expected concepts. "
            "Score: 0."
        )
    }


# =========================================================
# LOAD QUESTION DATA
# =========================================================

def load_questions():

    for file_path in QUESTION_FILES:

        if not file_path.exists():
            continue

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            if isinstance(data, list):
                return data

            if isinstance(data, dict):

                for key in [
                    "questions",
                    "data",
                    "question_bank"
                ]:

                    if key in data:

                        if isinstance(
                            data[key],
                            list
                        ):

                            return data[key]

        except Exception as error:

            print(
                f"Error loading {file_path}: {error}"
            )

    return []


# =========================================================
# GET QUESTION LISTS
# =========================================================

def get_aptitude_exam_questions(level):

    questions = load_questions()

    result = []

    for item in questions:

        if not isinstance(item, dict):
            continue

        round_name = str(
            item.get(
                "round",
                item.get(
                    "category",
                    ""
                )
            )
        ).lower()

        if "aptitude" not in round_name:
            continue

        item_level = str(
            item.get(
                "level",
                ""
            )
        ).lower()

        if (
            level
            and item_level
            and item_level != str(level).lower()
        ):
            continue

        result.append(item)

    return result


def get_technical_exam_questions(
    level,
    language
):

    questions = load_questions()

    result = []

    for item in questions:

        if not isinstance(item, dict):
            continue

        round_name = str(
            item.get(
                "round",
                item.get(
                    "category",
                    ""
                )
            )
        ).lower()

        if "technical" not in round_name:
            continue

        item_level = str(
            item.get(
                "level",
                ""
            )
        ).lower()

        item_language = str(
            item.get(
                "language",
                ""
            )
        ).lower()

        if (
            level
            and item_level
            and item_level != str(level).lower()
        ):
            continue

        if (
            language
            and item_language
            and item_language != str(language).lower()
        ):
            continue

        result.append(item)

    return result


def get_coding_exam_questions(
    level,
    language
):

    questions = load_questions()

    result = []

    for item in questions:

        if not isinstance(item, dict):
            continue

        round_name = str(
            item.get(
                "round",
                item.get(
                    "category",
                    ""
                )
            )
        ).lower()

        if "coding" not in round_name:
            continue

        item_level = str(
            item.get(
                "level",
                ""
            )
        ).lower()

        item_language = str(
            item.get(
                "language",
                ""
            )
        ).lower()

        if (
            level
            and item_level
            and item_level != str(level).lower()
        ):
            continue

        if (
            language
            and item_language
            and item_language != str(language).lower()
        ):
            continue

        result.append(item)

    return result


def get_hr_exam_questions(level):

    questions = load_questions()

    result = []

    for item in questions:

        if not isinstance(item, dict):
            continue

        round_name = str(
            item.get(
                "round",
                item.get(
                    "category",
                    ""
                )
            )
        ).lower()

        if (
            "hr" not in round_name
            and "communication" not in round_name
        ):
            continue

        item_level = str(
            item.get(
                "level",
                ""
            )
        ).lower()

        if (
            level
            and item_level
            and item_level != str(level).lower()
        ):
            continue

        result.append(item)

    return result


# =========================================================
# FALLBACK QUESTIONS
# =========================================================

FALLBACK_QUESTIONS = {

    "aptitude": [

        {
            "question": "What is 25 + 35?",
            "answer": "60",
            "round": "aptitude",
            "level": "easy"
        },

        {
            "question": "What is 10% of 200?",
            "answer": "20",
            "round": "aptitude",
            "level": "easy"
        },

        {
            "question": "If a number is multiplied by 5 and the result is 50, what is the number?",
            "answer": "10",
            "round": "aptitude",
            "level": "easy"
        }

    ],


    "technical": [

        {
            "question": "What is Java?",
            "answer": (
                "Java is an object oriented programming "
                "language used to build applications."
            ),
            "round": "technical",
            "level": "easy",
            "language": "java"
        },

        {
            "question": "What is Python?",
            "answer": (
                "Python is a high level interpreted "
                "programming language."
            ),
            "round": "technical",
            "level": "easy",
            "language": "python"
        },

        {
            "question": "What is inheritance in Java?",
            "answer": (
                "Inheritance is an object oriented "
                "mechanism where a class acquires "
                "properties and methods of another class."
            ),
            "round": "technical",
            "level": "medium",
            "language": "java"
        }

    ],


    "coding": [

        {
            "question": "Write a program to find the largest number in an array.",
            "answer": (
                "Use a loop to compare each element "
                "with the current maximum and update "
                "the maximum when a larger element is found."
            ),
            "round": "coding",
            "level": "easy",
            "language": "python"
        },

        {
            "question": "Write a program to check whether a number is prime.",
            "answer": (
                "Check divisibility from 2 to the square "
                "root of the number. If divisible it is "
                "not prime otherwise it is prime."
            ),
            "round": "coding",
            "level": "easy",
            "language": "python"
        }

    ],


    "hr": [

        {
            "question": "Tell me about yourself.",
            "answer": (
                "I am a computer science student with "
                "knowledge of Python Java HTML CSS and "
                "software development. I am interested "
                "in learning new technologies and building projects."
            ),
            "round": "hr",
            "level": "easy"
        },

        {
            "question": "Why should we hire you?",
            "answer": (
                "You should hire me because I am a quick "
                "learner, hardworking, adaptable and "
                "interested in contributing to the organization."
            ),
            "round": "hr",
            "level": "easy"
        }

    ]

}


# =========================================================
# SELECT QUESTIONS
# =========================================================

def select_questions(
    round_name,
    level="",
    language=""
):

    if round_name == "aptitude":

        questions = get_aptitude_exam_questions(
            level
        )

    elif round_name == "technical":

        questions = get_technical_exam_questions(
            level,
            language
        )

    elif round_name == "coding":

        questions = get_coding_exam_questions(
            level,
            language
        )

    elif round_name == "hr":

        questions = get_hr_exam_questions(
            level
        )

    else:

        questions = []


    # Use fallback if no matching questions
    if not questions:

        questions = FALLBACK_QUESTIONS.get(
            round_name,
            []
        )


    # Make a copy
    questions = list(questions)


    # Shuffle questions
    random.shuffle(questions)


    # Limit exam to 10 questions
    return questions[:10]


# =========================================================
# START EXAM
# =========================================================

@app.post("/api/start-exam")
async def start_exam(
    round_name: str = Form(...),
    level: str = Form(""),
    language: str = Form("")
):

    questions = select_questions(
        round_name,
        level,
        language
    )


    if not questions:

        return JSONResponse(
            {
                "success": False,
                "message": (
                    "No questions available "
                    "for this round."
                )
            },
            status_code=404
        )


    exam_state["round"] = round_name

    exam_state["level"] = level

    exam_state["language"] = language

    exam_state["questions"] = questions

    exam_state["current_question"] = 0

    exam_state["responses"] = {}

    exam_state["scores"] = {}

    exam_state["round_scores"] = {}


    return JSONResponse(
        {
            "success": True,
            "round": round_name,
            "total_questions": len(questions)
        }
    )


# =========================================================
# PUBLIC QUESTION LIST
# =========================================================

def public_question_list(
    questions
):

    result = []

    for index, item in enumerate(
        questions
    ):

        result.append(
            {
                "index": index,

                "question": item.get(
                    "question",
                    item.get(
                        "text",
                        ""
                    )
                ),

                "options": item.get(
                    "options",
                    []
                )
            }
        )

    return result


def get_all_public_questions():

    return public_question_list(
        exam_state["questions"]
    )


# =========================================================
# HOME
# =========================================================

@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(
    request: Request
):

    template_path = (
        TEMPLATES_DIR /
        "index.html"
    )

    if template_path.exists():

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request
            }
        )

    return HTMLResponse(
        """
        <html>
        <head>
            <title>SmartPrep AI</title>
        </head>

        <body>

        <h1>SmartPrep AI</h1>

        <p>
        AI-Powered Personalized Interview Training Platform
        </p>

        <a href="/login">
            Start Interview
        </a>

        </body>
        </html>
        """
    )


# =========================================================
# LOGIN
# =========================================================

@app.get(
    "/login",
    response_class=HTMLResponse
)
async def login_page(
    request: Request
):

    if (
        TEMPLATES_DIR /
        "login.html"
    ).exists():

        return templates.TemplateResponse(
            "login.html",
            {
                "request": request
            }
        )

    return HTMLResponse(
        """
        <h1>Login</h1>

        <p>
        SmartPrep AI Login
        </p>

        <a href="/personal">
        Continue
        </a>
        """
    )


# =========================================================
# PERSONAL
# =========================================================

@app.get(
    "/personal",
    response_class=HTMLResponse
)
async def personal_page(
    request: Request
):

    if (
        TEMPLATES_DIR /
        "personal.html"
    ).exists():

        return templates.TemplateResponse(
            "personal.html",
            {
                "request": request
            }
        )

    return HTMLResponse(
        """
        <h1>Personal Information</h1>

        <a href="/education">
        Continue
        </a>
        """
    )


# =========================================================
# EDUCATION
# =========================================================

@app.get(
    "/education",
    response_class=HTMLResponse
)
async def education_page(
    request: Request
):

    if (
        TEMPLATES_DIR /
        "education.html"
    ).exists():

        return templates.TemplateResponse(
            "education.html",
            {
                "request": request
            }
        )

    return HTMLResponse(
        """
        <h1>Education</h1>

        <a href="/skills">
        Continue
        </a>
        """
    )


# =========================================================
# EDUCATIONAL
# =========================================================

@app.get(
    "/educational",
    response_class=HTMLResponse
)
async def educational_page(
    request: Request
):

    if (
        TEMPLATES_DIR /
        "educational.html"
    ).exists():

        return templates.TemplateResponse(
            "educational.html",
            {
                "request": request
            }
        )

    return HTMLResponse(
        """
        <h1>Educational Information</h1>

        <a href="/skills">
        Continue
        </a>
        """
    )


# =========================================================
# SKILLS
# =========================================================

@app.get(
    "/skills",
    response_class=HTMLResponse
)
async def skills_page(
    request: Request
):

    if (
        TEMPLATES_DIR /
        "skills.html"
    ).exists():

        return templates.TemplateResponse(
            "skills.html",
            {
                "request": request
            }
        )

    return HTMLResponse(
        """
        <h1>Skills</h1>

        <a href="/interview">
        Start Interview
        </a>
        """
    )


# =========================================================
# INTERVIEW PAGE
# =========================================================

@app.get(
    "/interview",
    response_class=HTMLResponse
)
async def interview_page(
    request: Request
):

    if (
        TEMPLATES_DIR /
        "interview.html"
    ).exists():

        return templates.TemplateResponse(
            "interview.html",
            {
                "request": request,
                "questions": get_all_public_questions()
            }
        )

    return HTMLResponse(
        """
        <html>

        <head>
            <title>SmartPrep AI Interview</title>
        </head>

        <body>

        <h1>SmartPrep AI Interview</h1>

        <p>
        Start an interview round using the API.
        </p>

        </body>

        </html>
        """
    )


# =========================================================
# GET EXAM
# =========================================================

@app.get("/api/exam")
async def get_exam():

    return JSONResponse(
        {
            "success": True,

            "round": exam_state["round"],

            "level": exam_state["level"],

            "language": exam_state["language"],

            "current_question": (
                exam_state["current_question"]
            ),

            "total_questions": len(
                exam_state["questions"]
            ),

            "questions": (
                get_all_public_questions()
            )
        }
    )


# =========================================================
# SUBMIT ANSWER
# =========================================================

@app.post("/api/answer")
async def submit_answer(
    question_index: int = Form(...),
    candidate_answer: str = Form("")
):

    round_name = exam_state["round"]

    questions = exam_state["questions"]


    # -----------------------------------------------------
    # CHECK QUESTION INDEX
    # -----------------------------------------------------

    if (
        question_index < 0
        or question_index >= len(questions)
    ):

        return JSONResponse(
            {
                "success": False,
                "message": "Invalid question index."
            },
            status_code=400
        )


    # -----------------------------------------------------
    # GET QUESTION
    # -----------------------------------------------------

    item = questions[
        question_index
    ]


    correct_answer = item.get(
        "answer",
        item.get(
            "correct_answer",
            ""
        )
    )


    # -----------------------------------------------------
    # EVALUATE
    # -----------------------------------------------------

    evaluation = evaluate_answer(
        candidate_answer,
        correct_answer,
        round_name
    )


    # -----------------------------------------------------
    # SAVE RESPONSE
    # -----------------------------------------------------

    key = (
        f"{round_name}_"
        f"{question_index}"
    )


    exam_state["responses"][key] = (
        candidate_answer
    )


    # -----------------------------------------------------
    # SAVE SCORE
    # -----------------------------------------------------

    exam_state["scores"][key] = (
        evaluation["score"]
    )


    # -----------------------------------------------------
    # RETURN RESULT
    # -----------------------------------------------------

    return JSONResponse(
        {
            "success": True,

            "score": evaluation["score"],

            "feedback": evaluation["feedback"],

            "question_index": question_index
        }
    )


# =========================================================
# FINISH ROUND
# =========================================================

@app.post("/api/finish-round")
async def finish_round():

    round_name = exam_state["round"]


    round_scores = []

    for key, score in (
        exam_state["scores"].items()
    ):

        if key.startswith(
            round_name + "_"
        ):

            round_scores.append(
                score
            )


    total_questions = len(
        exam_state["questions"]
    )


    total_score = sum(
        round_scores
    )


    max_score = (
        total_questions * 100
    )


    percentage = 0

    if max_score > 0:

        percentage = (
            total_score /
            max_score
        ) * 100


    exam_state["round_scores"][
        round_name
    ] = {
        "total_score": total_score,
        "max_score": max_score,
        "percentage": percentage
    }


    return JSONResponse(
        {
            "success": True,

            "round": round_name,

            "total_score": total_score,

            "max_score": max_score,

            "percentage": round(
                percentage,
                2
            ),

            "question_count": total_questions
        }
    )


# =========================================================
# RESULTS
# =========================================================

@app.get(
    "/results",
    response_class=HTMLResponse
)
async def results_page(
    request: Request
):

    if (
        TEMPLATES_DIR /
        "results.html"
    ).exists():

        return templates.TemplateResponse(
            "results.html",
            {
                "request": request,

                "scores": exam_state[
                    "scores"
                ],

                "round_scores": (
                    exam_state[
                        "round_scores"
                    ]
                )
            }
        )


    # Calculate current result

    scores = list(
        exam_state["scores"].values()
    )

    total_score = sum(
        scores
    )

    max_score = (
        len(
            exam_state["questions"]
        ) * 100
    )

    percentage = 0

    if max_score > 0:

        percentage = (
            total_score /
            max_score
        ) * 100


    return HTMLResponse(
        f"""
        <html>

        <head>
            <title>SmartPrep AI Results</title>
        </head>

        <body>

        <h1>Interview Results</h1>

        <h2>
        Round:
        {exam_state["round"]}
        </h2>

        <h2>
        Score:
        {total_score} / {max_score}
        </h2>

        <h2>
        Percentage:
        {percentage:.2f}%
        </h2>

        <br>

        <a href="/interview">
        Take Another Interview
        </a>

        </body>

        </html>
        """
    )


# =========================================================
# OLD ROUTES
# =========================================================

@app.get(
    "/aptitude",
    response_class=HTMLResponse
)
async def aptitude_page(
    request: Request
):

    if (
        TEMPLATES_DIR /
        "aptitude.html"
    ).exists():

        return templates.TemplateResponse(
            "aptitude.html",
            {
                "request": request
            }
        )

    return RedirectResponse(
        "/interview"
    )


@app.get(
    "/technical",
    response_class=HTMLResponse
)
async def technical_page(
    request: Request
):

    if (
        TEMPLATES_DIR /
        "technical.html"
    ).exists():

        return templates.TemplateResponse(
            "technical.html",
            {
                "request": request
            }
        )

    return RedirectResponse(
        "/interview"
    )


@app.get(
    "/test-phase",
    response_class=HTMLResponse
)
async def test_phase_page(
    request: Request
):

    if (
        TEMPLATES_DIR /
        "test-phase.html"
    ).exists():

        return templates.TemplateResponse(
            "test-phase.html",
            {
                "request": request
            }
        )

    return RedirectResponse(
        "/interview"
    )


@app.get(
    "/coding",
    response_class=HTMLResponse
)
async def coding_page(
    request: Request
):

    if (
        TEMPLATES_DIR /
        "coding.html"
    ).exists():

        return templates.TemplateResponse(
            "coding.html",
            {
                "request": request
            }
        )

    return RedirectResponse(
        "/interview"
    )


@app.get(
    "/coding-phase",
    response_class=HTMLResponse
)
async def coding_phase_page(
    request: Request
):

    if (
        TEMPLATES_DIR /
        "coding-phase.html"
    ).exists():

        return templates.TemplateResponse(
            "coding-phase.html",
            {
                "request": request
            }
        )

    return RedirectResponse(
        "/interview"
    )


@app.get(
    "/hr",
    response_class=HTMLResponse
)
async def hr_page(
    request: Request
):

    if (
        TEMPLATES_DIR /
        "hr.html"
    ).exists():

        return templates.TemplateResponse(
            "hr.html",
            {
                "request": request
            }
        )

    return RedirectResponse(
        "/interview"
    )


@app.get(
    "/completed",
    response_class=HTMLResponse
)
async def completed_page(
    request: Request
):

    if (
        TEMPLATES_DIR /
        "completed.html"
    ).exists():

        return templates.TemplateResponse(
            "completed.html",
            {
                "request": request
            }
        )

    return RedirectResponse(
        "/results"
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "application": "SmartPrep AI"
    }


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "ai_interview_project.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )