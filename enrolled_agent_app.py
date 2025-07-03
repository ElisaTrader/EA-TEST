import streamlit as st
import json
import random

st.set_page_config(page_title="EA Practice Test", layout="wide")
st.title("🧾 Enrolled Agent Practice Test")
st.markdown("Simula il tuo test di abilitazione con 1000 domande casuali!")

@st.cache_data
def load_questions():
    with open("enrolled_agent_test_questions_1000.json", "r", encoding="utf-8") as f:
        return json.load(f)

questions = load_questions()

num_questions = st.slider("Quante domande vuoi esercitarti?", 5, 50, 10)
selected_questions = random.sample(questions, min(num_questions, len(questions)))

responses = []
valid_count = 0

st.subheader("📋 Domande")

for idx, q in enumerate(selected_questions):
    # Recupero domanda
    question_text = q.get("question") or q.get("text") or f"[Domanda mancante {idx+1}]"
    # Recupero opzioni
    options = q.get("options") or q.get("choices") or q.get("answers") or []
    if isinstance(options, str):
        options = [opt.strip() for opt in options.split(",") if opt.strip()]
    if not isinstance(options, list) or len(options) < 2:
        st.warning(f"⚠️ Domanda {idx+1} malformata, opzioni non valide. Saltata.")
        continue
    valid_count += 1

    # Recupero risposta corretta
    correct = q.get("answer") or q.get("correct") or q.get("correct_option") or ""

    st.markdown(f"**{valid_count}. {question_text}**")
    user_choice = st.radio(
        f"Domanda {valid_count}",
        options=["🔘 Nessuna risposta selezionata"] + options,
        index=0,
        key=f"question_{idx}"
    )
    responses.append({
        "question": question_text,
        "selected": user_choice,
        "correct": correct,
        "explanation": q.get("explanation", "Nessuna spiegazione."),
        "category": q.get("category", "")
    })
    st.markdown("---")

# Se non ci sono domande valide
if valid_count == 0:
    st.error("❗ Non ci sono domande valide. Controlla il JSON!")
else:
    if st.button("📊 Visualizza Risultati"):
        correct = sum(1 for r in responses if r["selected"] == r["correct"])
        skipped = sum(1 for r in responses if r["selected"] == "🔘 Nessuna risposta selezionata")
        st.write(f"**Totale domande:** {valid_count}")
        st.write(f"**Corrette:** {correct}")
        st.write(f"**Saltate:** {skipped}")
        st.write(f"**Punteggio:** {(correct/valid_count)*100:.1f}%")
        for i, r in enumerate(responses, 1):
            icon = "✅" if r["selected"] == r["correct"] else "❌"
            st.markdown(f"{icon} **Domanda {i}:** {r['question']}")
            st.markdown(f"- Tua risposta: `{r['selected']}`")
            st.markdown(f"- Corretta: `{r['correct']}`")
            st.markdown("---")
