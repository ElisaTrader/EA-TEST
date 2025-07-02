import streamlit as st
import json
import random

st.set_page_config(page_title="Enrolled Agent Test Simulator", layout="wide")

# ✅ Carica le domande da file JSON
@st.cache_data
def load_questions():
    with open("enrolled_agent_test_questions_1000.json", "r") as file:
        return json.load(file)

questions = load_questions()

# ✅ Titolo app
st.title("🧾 Enrolled Agent Test Simulator")
st.markdown("Simula il tuo test di abilitazione con **1000 domande casuali**!")

# ✅ Numero domande da mostrare
num_questions = st.slider("Numero di domande da simulare:", 5, min(50, len(questions)), 50)

# ✅ Pesca domande casuali
selected_questions = random.sample(questions, num_questions)

# ✅ Dizionario per risposte utente
user_answers = {}

# ✅ Visualizza ogni domanda
for q in selected_questions:
    st.write(f"**{q['question']}**")
    options = list(q["options"].items())

    default_option = "---"  # Nessuna risposta predefinita
    user_answers[q["id"]] = st.radio(
        label="Seleziona una risposta:",
        options=[default_option] + [opt[0] for opt in options],
        key=q["id"]
    )

st.write("---")

# ✅ Quando si clicca su 'Verifica Risposte'
if st.button("🔍 Verifica Risposte"):
    correct_count = 0
    unanswered = 0

    for q in selected_questions:
        user_choice = user_answers.get(q["id"], "---")
        correct = q["correct_option"]

        if user_choice == "---":
            unanswered += 1
            st.warning(f"Domanda: **{q['question']}** — ❌ Non risposto (corretta: {correct})")
        elif user_choice == correct:
            correct_count += 1
            st.success(f"Domanda: **{q['question']}** — ✅ Corretta")
        else:
            st.error(f"Domanda: **{q['question']}** — ❌ Sbagliata (corretta: {correct})")

    st.markdown(f"### 🧮 Totale corrette: `{correct_count}` su `{num_questions}`")
    st.markdown(f"🟡 Domande senza risposta: `{unanswered}`")

