import streamlit as st
import json
import random

st.set_page_config(page_title="Simulatore Test Enrolled Agent", layout="wide")

@st.cache_data
def load_questions():
    with open("enrolled_agent_test_questions_1000.json", "r") as file:
        return json.load(file)

questions = load_questions()

st.title("📘 Simulatore Test Enrolled Agent")
st.markdown("Simula il tuo test di abilitazione con 1000 domande casuali!")

num_questions = st.slider("Numero di domande nel test:", 10, 100, 20)

selected_questions = random.sample(questions, num_questions)

user_answers = []
score = 0

for idx, q in enumerate(selected_questions):
    st.subheader(f"{idx + 1}. {q['question']}")
    options = q["options"]
    user_choice = st.radio(
        "Seleziona una risposta:",
        ["🔘 Nessuna risposta selezionata"] + options,
        key=f"question_{idx}",
        index=0
    )
    user_answers.append((q, user_choice))

if st.button("🔎 Correggi il test"):
    st.subheader("Risultati:")
    for idx, (q, user_choice) in enumerate(user_answers):
        correct = q["correct"]
        is_correct = user_choice == correct
        if user_choice == "🔘 Nessuna risposta selezionata":
            result_text = f"❌ Non risposto. Risposta corretta: **{correct}**"
        elif is_correct:
            result_text = f"✅ Corretta: **{user_choice}**"
            score += 1
        else:
            result_text = f"❌ Sbagliata. Hai scelto: {user_choice}. Corretta: **{correct}**"
        st.markdown(f"**Domanda {idx + 1}**: {result_text}")

    st.success(f"💯 Punteggio finale: **{score} / {num_questions}**")
