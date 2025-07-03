import streamlit as st
import json
import random

st.set_page_config(page_title="EA Practice Test", layout="wide")
st.title("🧾 Enrolled Agent Practice Test")
st.markdown("Simula il tuo test di abilitazione con 1000 domande casuali!")

# Carica le domande con cache
@st.cache_data
def load_questions():
    with open("enrolled_agent_test_questions_1000.json", "r", encoding="utf-8") as f:
        return json.load(f)

questions = load_questions()

# Numero di domande da estrarre
num_questions = st.slider("Quante domande vuoi esercitarti?", 5, 50, 10)
selected_questions = random.sample(questions, min(num_questions, len(questions)))

responses = []
valid_count = 0

st.subheader("📋 Domande")

for idx, q in enumerate(selected_questions):
    question_text = q.get("question", "Domanda non disponibile")
    options = q.get("options")

    # Verifica che options sia una lista non vuota
    if not isinstance(options, list) or len(options) < 2:
        st.warning(f"⚠️ Domanda {idx + 1} ha opzioni non valide o mancanti. Saltata.")
        continue

    # Incremento contatore domande valide
    valid_count += 1

    st.markdown(f"**{idx + 1}. {question_text}**")
    user_choice = st.radio(
        f"Domanda {idx + 1}",
        options=["🔘 Nessuna risposta selezionata"] + options,
        index=0,
        key=f"question_{idx}"
    )
    responses.append({
        "question": question_text,
        "selected": user_choice,
        "correct": q.get("answer", ""),
        "explanation": q.get("explanation", "Nessuna spiegazione disponibile."),
        "category": q.get("category", "Generale")
    })
    st.markdown("---")

# Se non c’è almeno una domanda valida, informiamo l’utente
if valid_count == 0:
    st.error("❗ Non ci sono domande valide da mostrare. Controlla il tuo file JSON!")
else:
    if st.button("📊 Visualizza Risultati"):
        total = valid_count
        correct = sum(1 for r in responses if r["selected"] == r["correct"])
        skipped = sum(1 for r in responses if r["selected"] == "🔘 Nessuna risposta selezionata")

        st.subheader("📈 Risultati")
        st.write(f"Totale domande valide: **{total}**")
        st.write(f"Corrette: **{correct}**")
        st.write(f"Saltate: **{skipped}**")
        st.write(f"Punteggio: **{(correct / total) * 100:.1f}%**")

        for idx, r in enumerate(responses, 1):
            is_correct = r["selected"] == r["correct"]
            icon = "✅" if is_correct else "❌"
            st.markdown(f"{icon} **Domanda {idx}:** {r['question']}")
            st.markdown(f"- Tua risposta: `{r['selected']}`")
            st.markdown(f"- Risposta corretta: `{r['correct']}`")
            st.markdown(f"- Categoria: _{r['category']}_")
            st.markdown(f"- Spiegazione: {r['explanation']}")
            st.markdown("---")
