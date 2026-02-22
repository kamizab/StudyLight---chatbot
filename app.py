import streamlit as st
from src.state import init_state, reset_all

st.set_page_config(
    page_title="StudyLight",
    page_icon="💡",
    layout="centered",
)

init_state()

st.title("💡 StudyLight")
st.subheader("Witaj w aplikacji do szybkich quizów z chatbotem.")

st.write(
    "- Bot dopyta o temat i poziom trudności\n"
    "- Wygeneruje quiz wielokrotnego wyboru\n"
    "- Na końcu zobaczysz wynik i omówienie"
)

c1, c2 = st.columns(2)

with c1:
    st.page_link("pages/1_Quiz_Bot.py", label="🚀 Przejdź do quiz bota", use_container_width=True)

with c2:
    if st.button("🧹 Reset", use_container_width=True):
        reset_all()
        st.rerun()