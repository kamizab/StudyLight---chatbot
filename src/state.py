import streamlit as st

def init_state() -> None:
    defaults = {
        "chat_history": [],

        # Flow: ask_topic -> ask_detail -> ask_difficulty -> quiz
        "flow_step": "ask_topic",

        "topic": "",
        "detail": "",
        "difficulty": None,

        "quiz": None,          # dict
        "answers": {},         # qid -> selected option index
        "submitted": False,
        "score": None,

        # opcjonalnie: wiadomości diagnostyczne
        "last_error": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def reset_quiz_flow() -> None:
    st.session_state.chat_history = []
    st.session_state.flow_step = "ask_topic"
    st.session_state.topic = ""
    st.session_state.detail = ""
    st.session_state.difficulty = None
    st.session_state.quiz = None
    st.session_state.answers = {}
    st.session_state.submitted = False
    st.session_state.score = None
    st.session_state.last_error = None

def reset_all() -> None:
    for k in list(st.session_state.keys()):
        del st.session_state[k]