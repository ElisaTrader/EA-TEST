import streamlit as st
import json
import random

# Carica le domande
@st.cache_data
def load_questions():
    with open("enrolled_agent_test_questions_1000.json", "r") as file:
        return json.load(file)

questions = load_questions()

st.title("🧾 Enrolled Agent Practice Test")
st.markdown("Simula il tuo test di abilitazione con 1000 domande casuali!")

num_questions = st.slider("Quante domande vuoi praticare?", 5, 100, 20)

selected_questions = random.sample(questions, num_questions)
user_answers = {}

for idx, q in enumerate(selected_questions):
    st.markdown(f"**{idx + 1}. {q['question']}**")
    options = ["", "A", "B", "C"]
    choice = st.radio(
        f"Seleziona una risposta:", options=options,
        format_func=lambda x: {"": "Nessuna risposta", "A": "A", "B": "B", "C": "C"}[x],
        key=f"question_{idx}"
    )
    user_answers[idx] = choice

if st.button("Verifica Risposte"):
    score = 0
    for idx, q in enumerate(selected_questions):
        if user_answers[idx] == q["answer"]:
            score += 1
    st.success(f"Hai risposto correttamente a {score} domande su {num_questions} ({score / num_questions * 100:.2f}%).")
