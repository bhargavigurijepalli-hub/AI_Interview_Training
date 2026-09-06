
def evaluate_answer(candidate_answer, correct_answer, round_name):
    """
    Evaluate a candidate's answer.

    Scoring:
        100 = Correct
        80  = Mostly correct
        60  = Partially correct
        40  = Weak/partially relevant
        0   = Wrong or no answer

    This is a local rule-based evaluator.
    It is NOT an LLM/semantic AI evaluator.
    """

    candidate = normalize_text(candidate_answer)
    correct = normalize_text(correct_answer)

    # =========================================================
    # EMPTY ANSWER
    # =========================================================

    if not candidate:
        return {
            "score": 0,
            "feedback": "No answer was provided. Score: 0."
        }

    # =========================================================
    # NO CORRECT ANSWER AVAILABLE
    # =========================================================

    if not correct:
        return {
            "score": 0,
            "feedback": "The expected answer is unavailable, so no marks were awarded."
        }

    # =========================================================
    # EXACT MATCH
    # =========================================================

    if candidate == correct:
        return {
            "score": 100,
            "feedback": "Correct answer. Excellent."
        }

    # =========================================================
    # APTITUDE ROUND
    # =========================================================

    if round_name.lower() == "aptitude":

        candidate_numbers = extract_numbers(candidate_answer)
        correct_numbers = extract_numbers(correct_answer)

        if candidate_numbers and correct_numbers:

            for candidate_number in candidate_numbers:

                for correct_number in correct_numbers:

                    if abs(candidate_number - correct_number) < 0.01:
                        return {
                            "score": 100,
                            "feedback": "Correct numerical answer."
                        }

        return {
            "score": 0,
            "feedback": "Incorrect answer. The numerical result does not match the expected answer."
        }

    # =========================================================
    # KEYWORD-BASED EVALUATION
    # =========================================================

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

    # If there are no meaningful words to compare
    if not correct_words:
        return {
            "score": 0,
            "feedback": "Unable to evaluate the answer. No marks awarded."
        }

    matched_words = correct_words.intersection(candidate_words)

    matched = len(matched_words)

    total = len(correct_words)

    ratio = matched / total

    # =========================================================
    # SCORING
    # =========================================================

    # Very strong match
    if ratio >= 0.75:
        return {
            "score": 90,
            "feedback": (
                "Mostly correct. Your answer contains most of "
                "the important concepts."
            )
        }

    # Good partial answer
    if ratio >= 0.50:
        return {
            "score": 70,
            "feedback": (
                "Partially correct. You identified several "
                "important concepts, but the explanation needs improvement."
            )
        }

    # Weak partial answer
    if ratio >= 0.35:
        return {
            "score": 40,
            "feedback": (
                "Your answer is only partially relevant. "
                "Include more of the important concepts."
            )
        }

    # =========================================================
    # WRONG ANSWER
    # =========================================================

    return {
        "score": 0,
        "feedback": (
            "Incorrect answer. Your response does not contain "
            "enough of the expected concepts. Score: 0."
        )
    }

