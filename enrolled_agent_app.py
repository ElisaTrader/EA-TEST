import streamlit as st
import json
import random

# Carica le domande dal file JSON
@st.cache_data
def load_questions():
    with open("enrolled_agent_test_questions_1000.json", "r", encoding="utf-8") as f:
        return json.load(f)

questions = load_questions()

st.title("🧾 Enrolled Agent Practice Test")
st.markdown("Test your knowledge with multiple-choice questions based on the EA exam.")

# Scelta numero di domande
num_questions = st.slider("Select number of questions:", 5, 50, 10)
selected_questions = random.sample(questions, num_questions)

user_answers = {}

st.divider()
for idx, q in enumerate(selected_questions):
    st.subheader(f"Question {idx + 1}:")
    st.write(q["question"])
    user_answers[q["id"]] = st.radio(
        label="Select an answer:",
        options=["A", "B", "C"],
        key=q["id"]
    )

st.divider()

if st.button("Submit Test"):
    score = 0
    st.subheader("📊 Results")
    for q in selected_questions:
        correct = q["correct_option"]
        user_ans = user_answers[q["id"]]
        is_correct = user_ans == correct
        if is_correct:
            score += 1
        st.markdown(f"**Q: {q['question']}**")
        st.markdown(f"Your answer: {user_ans} {'✅' if is_correct else '❌'}")
        if not is_correct:
            st.markdown(f"Correct answer: **{correct}**")
        st.markdown("---")

    st.success(f"You scored {score} out of {num_questions}.")
