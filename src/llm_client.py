from __future__ import annotations

import json
from typing import Any, Dict, Optional

import streamlit as st
from pydantic import BaseModel, Field, ValidationError, conint, constr

from src.prompt_templates import build_quiz_prompt


# ----------------------------
# Walidacja odpowiedzi LLM
# ----------------------------
class Question(BaseModel):
    id: constr(min_length=1)
    prompt: constr(min_length=1)
    options: list[constr(min_length=1)] = Field(min_length=4, max_length=4)
    correct_index: conint(ge=0, le=3)
    explanation: constr(min_length=1)

class Quiz(BaseModel):
    meta: Dict[str, Any]
    questions: list[Question] = Field(min_length=5, max_length=5)


def _require_secret(name: str) -> str:
    val = st.secrets.get(name)
    if not val:
        st.error(
            f"Brak sekretu: **{name}**.\n\n"
            f"Dodaj go do `/.streamlit/secrets.toml` (lokalnie) albo do sekretów na hostingu."
        )
        st.stop()
    return str(val)


def generate_quiz_with_llm(topic: str, detail: str, difficulty: int) -> Dict[str, Any]:
    """
    Provider wybierasz w secrets.toml:
      PROVIDER="openai" lub PROVIDER="gemini"
    """
    provider = (st.secrets.get("PROVIDER") or "").strip().lower()
    if provider not in {"openai", "gemini"}:
        st.error("Ustaw `PROVIDER` w `/.streamlit/secrets.toml` na `openai` albo `gemini`.")
        st.stop()

    prompt = build_quiz_prompt(topic, detail, difficulty)

    if provider == "openai":
        model = st.secrets.get("OPENAI_MODEL") or "gpt-4.1-mini"
        api_key = _require_secret("OPENAI_API_KEY")
        raw_text = _call_openai(prompt=prompt, model=model, api_key=api_key)
    else:
        model = st.secrets.get("GEMINI_MODEL") or "gemini-3-flash-preview"
        api_key = _require_secret("GEMINI_API_KEY")
        raw_text = _call_gemini(prompt=prompt, model=model, api_key=api_key)

    # Parsowanie JSON
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"LLM nie zwrócił poprawnego JSON. Błąd: {e}\n\nOtrzymano:\n{raw_text[:800]}")

    # Walidacja struktury
    try:
        quiz = Quiz.model_validate(data)
    except ValidationError as e:
        raise RuntimeError(f"LLM zwrócił JSON, ale w złej strukturze:\n{e}\n\nOtrzymano:\n{raw_text[:800]}")

    # Uzupełnij meta (na wypadek gdyby model coś pominął)
    meta = dict(quiz.meta or {})
    meta.update({"topic": topic, "detail": detail, "difficulty": difficulty, "n_questions": 5})

    return {"meta": meta, "questions": [q.model_dump() for q in quiz.questions]}


def _call_openai(prompt: str, model: str, api_key: str) -> str:
    """
    OpenAI Python SDK – czyta klucz zwykle z env, ale tu podajemy jawnie (i tak tylko w runtime).
    Przykłady i zalecenia użycia klucza jako env/secret: :contentReference[oaicite:2]{index=2}
    """
    try:
        from openai import OpenAI
    except Exception as e:
        raise RuntimeError("Brak pakietu `openai`. Zainstaluj: pip install openai") from e

    client = OpenAI(api_key=api_key)

    # Responses API (nowe, rekomendowane)
    resp = client.responses.create(
        model=model,
        input=prompt,
    )
    # resp.output_text – gotowy tekst odpowiedzi
    return resp.output_text


def _call_gemini(prompt: str, model: str, api_key: str) -> str:
    """
    Google GenAI SDK – quickstart wskazuje użycie GEMINI_API_KEY jako env/secret. :contentReference[oaicite:3]{index=3}
    """
    try:
        from google import genai
    except Exception as e:
        raise RuntimeError("Brak pakietu `google-genai`. Zainstaluj: pip install google-genai") from e

    client = genai.Client(api_key=api_key)
    resp = client.models.generate_content(
        model=model,
        contents=prompt,
    )
    return (resp.text or "").strip()