import streamlit as st
from PyPDF2 import PdfReader
from google import genai
from dotenv import load_dotenv
import os

# -------------------------
# Load Gemini API Key
# -------------------------

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# -------------------------
# Session State
# -------------------------

if "generated_questions" not in st.session_state:
    st.session_state.generated_questions = ""

# -------------------------
# Page Config
# -------------------------

st.set_page_config(
    page_title="AI Interview Question Generator",
    page_icon="🎯",
    layout="wide"
)

# -------------------------
# Title
# -------------------------

st.title("🎯 AI Interview Question Generator")

st.write(
    "Generate personalized interview questions, ATS analysis, and practice interviews using Gemini AI."
)

# -------------------------
# Inputs
# -------------------------

difficulty = st.selectbox(
    "Select Difficulty Level",
    ["Easy", "Medium", "Hard"]
)

company = st.selectbox(
    "Target Company",
    [
        "General",
        "Google",
        "Amazon",
        "Microsoft",
        "Adobe",
        "Atlassian",
        "Goldman Sachs",
        "Uber",
        "Flipkart"
    ]
)

num_questions = st.selectbox(
    "Questions Per Category",
    [3, 5, 7, 10]
)

# -------------------------
# Resume Upload
# -------------------------

uploaded_file = st.file_uploader(
    "Upload Your Resume (PDF)",
    type=["pdf"]
)

# -------------------------
# Resume Processing
# -------------------------

if uploaded_file:

    st.success("✅ Resume uploaded successfully!")

    pdf = PdfReader(uploaded_file)

    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    # -------------------------
    # Show Resume
    # -------------------------

    with st.expander("📄 View Extracted Resume"):
        st.write(text)

    # -------------------------
    # ATS Analysis
    # -------------------------

    if st.button("📊 Analyze Resume (ATS Score)"):

        with st.spinner("Analyzing Resume..."):

            ats_response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"""
You are an ATS (Applicant Tracking System) expert.

Analyze the following resume and provide:

1. ATS Score (out of 100)

2. Strengths

3. Weaknesses

4. Missing Skills

5. Suggestions for Improvement

Keep the response structured and professional.

Resume:

{text}
"""
            )

        st.subheader("📊 ATS Resume Analysis")

        st.markdown(ats_response.text)

    # -------------------------
    # Generate Questions
    # -------------------------

    if st.button("🚀 Generate Interview Questions"):

        with st.spinner("Generating Questions..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"""
You are an experienced technical interviewer.

Target Company: {company}

Difficulty Level: {difficulty}

Generate {num_questions} interview questions for EACH category.

Create the following sections:

# HR Questions

# Technical Questions

# DSA Questions

# Project Questions

Requirements:

- Questions should be based on the uploaded resume.
- Questions should match the selected difficulty.
- Questions should resemble real interview questions asked by {company}.
- Do NOT provide answers.
- Format output clearly.

Resume:

{text}
"""
            )

        st.session_state.generated_questions = response.text

        st.success("✅ Questions Generated Successfully!")

    # -------------------------
    # Display Questions
    # -------------------------

    if st.session_state.generated_questions:

        st.subheader("📌 Generated Interview Questions")

        st.markdown(st.session_state.generated_questions)

        st.download_button(
            label="⬇ Download Questions",
            data=st.session_state.generated_questions,
            file_name="interview_questions.txt",
            mime="text/plain"
        )

        # -------------------------
        # Mock Interview Mode
        # -------------------------

        st.divider()

        st.header("🎤 Mock Interview Practice")

        st.write(
            "Paste one of the generated questions below and answer it."
        )

        selected_question = st.text_area(
            "Interview Question",
            height=100
        )

        user_answer = st.text_area(
            "Your Answer",
            height=200
        )

        if st.button("📊 Evaluate My Answer"):

            if selected_question and user_answer:

                with st.spinner("Evaluating Answer..."):

                    feedback = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=f"""
You are a senior interviewer.

Question:
{selected_question}

Candidate Answer:
{user_answer}

Evaluate the answer and provide:

1. Score out of 10

2. Strengths

3. Weaknesses

4. Improvements

5. A Sample Ideal Answer

Be detailed and professional.
"""
                    )

                st.subheader("📋 Interview Feedback")

                st.markdown(feedback.text)

            else:
                st.warning(
                    "Please enter both a question and an answer."
                )