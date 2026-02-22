QUIZ_JSON_SCHEMA_HINT = """
Zwróć WYŁĄCZNIE JSON w tym formacie:

{
  "meta": {
    "topic": "string",
    "detail": "string",
    "difficulty": 1,
    "n_questions": 5
  },
  "questions": [
    {
      "id": "q1",
      "prompt": "string (markdown ok)",
      "options": ["A", "B", "C", "D"],
      "correct_index": 0,
      "explanation": "krótkie wyjaśnienie"
    }
  ]
}

Zasady:
- dokładnie 5 pytań
- dokładnie 4 odpowiedzi na pytanie
- correct_index w zakresie 0..3
- brak komentarzy, brak markdown poza polami prompt/explanation
- język: polski
"""

def build_quiz_prompt(topic: str, detail: str, difficulty: int) -> str:
    return f"""
Jesteś generatorem quizów dla studentów.
Temat: {topic}
Doprecyzowanie: {detail}
Trudność: {difficulty}/10

Wygeneruj quiz wielokrotnego wyboru (A/B/C/D).
{QUIZ_JSON_SCHEMA_HINT}
""".strip()