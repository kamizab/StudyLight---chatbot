import streamlit as st
from src.llm_client import generate_quiz_with_llm

def push_assistant(msg: str) -> None:
    st.session_state.chat_history.append({"role": "assistant", "content": msg})

def push_user(msg: str) -> None:
    st.session_state.chat_history.append({"role": "user", "content": msg})

def ensure_first_bot_message() -> None:
    if not st.session_state.chat_history:
        push_assistant("Cześć! Zrobię dla Ciebie quiz. Na jaki **temat** ma być quiz?")

def handle_user_message(msg: str) -> None:
    msg = (msg or "").strip()
    if not msg:
        return

    push_user(msg)
    step = st.session_state.flow_step

    if step == "ask_topic":
        st.session_state.topic = msg
        st.session_state.flow_step = "ask_detail"
        push_assistant(
            "Super. Doprecyzuj temat, żeby quiz był konkretny.\n\n"
            "Np. zamiast „Algebra” → „macierze, wyznaczniki, rząd macierzy”."
        )
        return

    if step == "ask_detail":
        st.session_state.detail = msg
        st.session_state.flow_step = "ask_difficulty"
        push_assistant("Jaki poziom trudności? Podaj liczbę od **1 do 10**.")
        return

    if step == "ask_difficulty":
        try:
            d = int(msg)
        except ValueError:
            push_assistant("Potrzebuję liczby od **1 do 10**. Spróbuj jeszcze raz.")
            return

        if not (1 <= d <= 10):
            push_assistant("Poziom musi być w zakresie **1–10**. Podaj poprawną liczbę.")
            return

        st.session_state.difficulty = d

        push_assistant(
            f"OK! Generuję quiz.\n\n"
            f"**Temat:** {st.session_state.topic}\n"
            f"**Doprecyzowanie:** {st.session_state.detail}\n"
            f"**Trudność:** {st.session_state.difficulty}/10"
        )

        try:
            st.session_state.quiz = generate_quiz_with_llm(
                topic=st.session_state.topic,
                detail=st.session_state.detail,
                difficulty=st.session_state.difficulty,
            )
            st.session_state.flow_step = "quiz"
            push_assistant("Gotowe ✅ Przejdź niżej i rozwiąż quiz.")
        except Exception as e:
            st.session_state.last_error = str(e)
            push_assistant("Coś poszło nie tak przy generowaniu quizu. Zmień parametry lub sprawdź konfigurację klucza.")
            # zostajemy na ask_difficulty, żeby można było poprawić
            st.session_state.flow_step = "ask_difficulty"

        return

    if step == "quiz":
        push_assistant("Jesteś w trakcie quizu — zaznacz odpowiedzi poniżej. Jeśli chcesz nowy quiz, kliknij „Wygeneruj ponownie”.")