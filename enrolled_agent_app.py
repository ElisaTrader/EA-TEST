import streamlit as st
import json
import random

st.set_page_config(page_title="EA Practice Test", layout="wide")

# Carica le domande con cache
@st.cache_data
def load_questions():
    with open("enrolled_agent_test_questions_1000.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

# Carica le domande
questions = load_questions()

st.title("🧾 Enrolled Agent Practice Test")
st.markdown("Simula il tuo test di abilitazione con 1000 domande casuali!")

num_questions = st.slider("Quante domande vuoi esercitarti?", 5, 50, 10)
selected_questions = random.sample(questions, num_questions)

responses = []

st.subheader("📋 Domande")

for idx, q in enumerate(selected_questions):
    question_text = q.get("question", f"[Domanda mancante {idx}]")
    options = q.get("options")

    if not isinstance(options, list) or not options:
        st.error(f"⚠️ Domanda {idx + 1} ha opzioni non valide o mancanti. Saltata.")
        continue  # passa alla prossima domanda

    st.markdown(f"**{idx + 1}. {question_text}**")

    user_answer = st.radio(
        f"Domanda {idx + 1}",
        options=["🔘 Nessuna risposta selezionata"] + options,
        index=0,
        key=f"question_{idx}"
    )

    responses.append({
        "question": question_text,
        "selected": user_answer,
        "correct": q.get("answer", ""),
        "explanation": q.get("explanation", "Nessuna spiegazione disponibile."),
        "category": q.get("category", "Generale")
    })
    st.markdown("---")

if st.button("📊 Visualizza Risultati"):
    st.subheader("📈 Risultati")

    total = len(responses)
    correct = sum(1 for r in responses if r["selected"] == r["correct"])
    skipped = sum(1 for r in responses if r["selected"] == "🔘 Nessuna risposta selezionata")

    st.write(f"Totale domande: **{total}**")
    st.write(f"Corrette: **{correct}**")
    st.write(f"Saltate: **{skipped}**")
    st.write(f"Punteggio: **{(correct / total) * 100:.1f}%**")

    for r in responses:
        is_correct = r["selected"] == r["correct"]
        color = "✅" if is_correct else "❌"
        st.markdown(f"{color} **Domanda:** {r['question']}")
        st.markdown(f"• Tua risposta: `{r['selected']}`")
        st.markdown(f"• Corretta: `{r['correct']}`")
        st.markdown(f"• Categoria: _{r['category']}_")
        st.markdown(f"• Spiegazione: {r['explanation']}")
        st.markdown("---")
