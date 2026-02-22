import streamlit as st
from src.state import init_state, reset_quiz_flow, reset_all
from src.chat_flow import handle_user_message, ensure_first_bot_message
from src.quiz_engine import grade_quiz

init_state()

st.title("🤖 Quiz Bot")
st.caption("Chatbot do generowania quizów (Streamlit)")

# Pasek akcji
top = st.columns([1, 1, 1])
with top[0]:
    st.page_link("app.py", label="🏠 Start", use_container_width=True)

with top[1]:
    if st.button("🔁 Wygeneruj ponownie", use_container_width=True):
        reset_quiz_flow()
        ensure_first_bot_message()
        st.rerun()

with top[2]:
    if st.button("🧹 Reset wszystko", use_container_width=True):
        reset_all()
        st.rerun()

st.divider()

ensure_first_bot_message()

# (opcjonalnie) debug błędów bez pokazywania sekretów
if st.session_state.last_error:
    with st.expander("Diagnostyka (błąd generowania)", expanded=False):
        st.code(st.session_state.last_error)

# Chat transcript
for m in st.session_state.chat_history:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Input
user_msg = st.chat_input("Napisz odpowiedź…")
if user_msg is not None:
    handle_user_message(user_msg)
    st.rerun()

st.divider()

# Quiz UI
quiz = st.session_state.quiz
if quiz and st.session_state.flow_step == "quiz":
    st.subheader("📝 Quiz")

    meta = quiz.get("meta", {})
    with st.expander("Parametry quizu", expanded=False):
        st.write(f"**Temat:** {meta.get('topic','')}")
        st.write(f"**Doprecyzowanie:** {meta.get('detail','')}")
        st.write(f"**Trudność:** {meta.get('difficulty','')}/10")
        st.write(f"**Liczba pytań:** {meta.get('n_questions','')}")

    for q in quiz["questions"]:
        st.markdown(f"**{q['id'].upper()}** — {q['prompt']}")

        key = f"ans_{q['id']}"
        previous = st.session_state.answers.get(q["id"])
        index = previous if previous is not None else 0

        chosen = st.radio(
            label="Wybierz odpowiedź:",
            options=list(range(len(q["options"]))),
            format_func=lambda i: q["options"][i],
            index=index,
            key=key,
        )
        st.session_state.answers[q["id"]] = chosen
        st.write("")

    if not st.session_state.submitted:
        if st.button("✅ Zakończ i policz wynik", use_container_width=True):
            score, total = grade_quiz(quiz, st.session_state.answers)
            st.session_state.score = score
            st.session_state.submitted = True
            st.rerun()

    if st.session_state.submitted:
        total = len(quiz["questions"])
        score = st.session_state.score or 0
        st.success(f"Twój wynik: **{score}/{total}**")

        st.subheader("🔎 Omówienie")
        for q in quiz["questions"]:
            selected = st.session_state.answers.get(q["id"])
            correct_i = q["correct_index"]
            is_ok = (selected == correct_i)

            st.markdown(f"**{q['id'].upper()}**")
            st.write(q["prompt"])
            st.write(f"Twoja odpowiedź: {q['options'][selected]}")
            st.write(f"Poprawna odpowiedź: {q['options'][correct_i]}")

            if is_ok:
                st.success("✅ Poprawnie")
            else:
                st.error("❌ Niepoprawnie")

            st.info(q["explanation"])
            st.divider()