import streamlit as st
import json
import random

# Titolo e layout
st.set_page_config(page_title="Enrolled Agent Exam Simulator", layout="wide")
st.title("🧾 Enrolled Agent Exam Simulator")
st.markdown("Simula il tuo test di abilitazione con 1000 domande casuali!")

# Funzione per caricare le domande
@st.cache_data
def load_questions():
    with open("enrolled_agent_test_questions_1000.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Caricamento domande
questions = load_questions()

# Selezione numero di domande
num_questions = st.slider("Quante domande vuoi nel test?", 5, 100, 50)

# Selezione casuale delle domande
selected_questions = random.sample(questions, num_questions)

# Dizionario per risposte utente
user_answers = {}

# Mostra domande
st.header("📋 Domande")
for idx, q in enumerate(selected_questions):
    st.subheader(f"{idx + 1}. {q['question']}")
    user_answers[q["id"]] = st.radio(
        label="Seleziona una risposta:",
        options=["", "A", "B", "C"],
        format_func=lambda x: "— Nessuna risposta —" if x == "" else x,
        key=q["id"]
    )

# Calcola punteggio
if st.button("✅ Verifica Risposte"):
    score = 0
    unanswered = 0
    results = []

    for q in selected_questions:
        user_answer = user_answers.get(q["id"], "")
        correct_answer = q["correct_option"]

        if user_answer == "":
            unanswered += 1
            result = "⏭️ Non risposto"
        elif user_answer == correct_answer:
            score += 1
            result = "✅ Corretto"
        else:
            result = f"❌ Errato (giusta: {correct_answer})"

        results.append((q["question"], user_answer, result))

    st.subheader("📊 Risultati")
    st.write(f"Domande corrette: **{score} / {num_questions}**")
    st.write(f"Domande non risposte: **{unanswered}**")

    with st.expander("📖 Dettagli risposta per domanda"):
        for i, (question, user_answer, result) in enumerate(results, 1):
            st.markdown(f"**{i}. {question}**")
            st.markdown(f"Risposta tua: `{user_answer if user_answer else 'Nessuna'}` — {result}")
            st.markdown("---")
