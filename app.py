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
st.write("Generate personalized interview questions from your resume using Gemini AI.")

# -------------------------
# User Inputs
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
# Process Resume
# -------------------------

if uploaded_file:

    st.success("✅ Resume uploaded successfully!")

    pdf = PdfReader(uploaded_file)

    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    with st.expander("📄 View Extracted Resume"):
        st.write(text)

    # -------------------------
    # Generate Questions
    # -------------------------

    if st.button("🚀 Generate Interview Questions"):

        with st.spinner("Generating questions... Please wait."):

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
- Format output cleanly.

Resume:

{text}
"""
            )

        st.subheader("📌 Generated Interview Questions")

        st.markdown(response.text)

        st.download_button(
            label="⬇ Download Questions",
            data=response.text,
            file_name="interview_questions.txt",
            mime="text/plain"
        )

        st.success("Questions generated successfully!")