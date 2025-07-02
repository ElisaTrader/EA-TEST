
import streamlit as st
import json
import random
import time

st.set_page_config(page_title="Enrolled Agent Test Simulator", layout="wide")

@st.cache_data
def load_questions():
    with open("enrolled_agent_test_questions_1000.json", "r") as file:
        return json.load(file)

def reset_session_state():
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = ["Not answered"] * len(questions)
    st.session_state.start_time = time.time()
    st.session_state.finished = False

questions = load_questions()
total_questions = 20  # Number of questions per session
random.shuffle(questions)
questions = questions[:total_questions]

if "current_question" not in st.session_state:
    reset_session_state()

st.title("📘 Enrolled Agent Exam Simulator")
st.markdown("Test di simulazione con 20 domande a scelta multipla. Il tempo viene tracciato e il punteggio salvato.")

if st.button("🔄 Ricomincia il test"):
    reset_session_state()

if not st.session_state.finished:
    question = questions[st.session_state.current_question]
    st.subheader(f"Domanda {st.session_state.current_question + 1} di {total_questions}")
    st.write(question["question"])
    options = question["options"]
    user_answer = st.radio("Scegli la risposta:", ["Not answered"] + options, index=0, key=f"q_{st.session_state.current_question}")

    if st.button("Avanti"):
        st.session_state.answers[st.session_state.current_question] = user_answer
        if user_answer == question["answer"]:
            st.session_state.score += 1
        if st.session_state.current_question + 1 < total_questions:
            st.session_state.current_question += 1
        else:
            st.session_state.finished = True
else:
    elapsed_time = int(time.time() - st.session_state.start_time)
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    st.success("✅ Test completato!")
    st.markdown(f"**Punteggio finale:** {st.session_state.score} su {total_questions}")
    st.markdown(f"⏱️ Tempo impiegato: {minutes} minuti e {seconds} secondi")
    st.download_button("📥 Scarica risultati", data=json.dumps(st.session_state.answers, indent=2),
                       file_name="risposte_test.json", mime="application/json")
