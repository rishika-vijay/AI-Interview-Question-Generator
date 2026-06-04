import streamlit as st
from PyPDF2 import PdfReader
from google import genai
from dotenv import load_dotenv
import os

# Load API Key
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# App Title
st.title("AI Interview Question Generator")

# Difficulty Selection
difficulty = st.selectbox(
    "Select Difficulty",
    ["Easy", "Medium", "Hard"]
)

# Company Selection
company = st.selectbox(
    "Target Company",
    [
    "General",
    "Google",
    "Amazon",
    "Microsoft",
    "Goldman Sachs",
    "Atlassian",
    "Adobe",
    "Uber",
    "Flipkart"
]
)

# Resume Upload
uploaded_file = st.file_uploader(
    "Upload your Resume",
    type=["pdf"]
)

if uploaded_file:

    st.success("Resume uploaded successfully!")

    # Read PDF
    pdf = PdfReader(uploaded_file)

    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    # Show Resume Content
    with st.expander("View Extracted Resume"):
        st.write(text)

    # Generate Questions Button
    if st.button("Generate Interview Questions"):

        with st.spinner("Generating Questions..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"""
You are an experienced interviewer.

Generate {difficulty} level interview questions.

Target Company: {company}

Based on the resume below generate:

# HR Questions
Generate 5 questions.

# Technical Questions
Generate 5 questions.

# DSA Questions
Generate 5 questions.

# Project Questions
Generate 5 questions.

Make the questions specific to the resume.

Do not provide answers.

Resume:

{text}
"""
            )

        st.subheader("Generated Questions")

        st.markdown(response.text)

        st.download_button(
        label="Download Questions",
        data=response.text,
        file_name="interview_questions.txt",
        mime="text/plain"
)