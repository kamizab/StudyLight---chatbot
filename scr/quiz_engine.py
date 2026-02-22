from typing import Dict, Any, Tuple

def grade_quiz(quiz: Dict[str, Any], answers: Dict[str, int]) -> Tuple[int, int]:
    score = 0
    questions = quiz.get("questions", [])
    total = len(questions)

    for q in questions:
        qid = q["id"]
        if answers.get(qid) == q["correct_index"]:
            score += 1

    return score, total