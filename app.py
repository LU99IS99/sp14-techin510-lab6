import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')
conversation = []


def ai_gen(prompts):
    response = model.generate_content(prompts)
    return response.text


# Function to extract text from PDF file
def get_text(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text


# Main function
def main():
    st.title("Mock Interview System📑")  # Add the heading "feedback Generator"
    company = st.sidebar.text_input("Input interview company")
    position = st.sidebar.text_input("Input interview position")
    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = None
    if 'resume_suggestion' not in st.session_state:
        st.session_state.resume_suggestion = None
    if 'resume_question' not in st.session_state:
        st.session_state.resume_question = None
    if 'resume_answer' not in st.session_state:
        st.session_state.resume_answer = None
    uploaded_file = st.sidebar.file_uploader("Upload your resume (PDF)", type="pdf")
    if uploaded_file is not None:
        st.sidebar.write("Resume Uploaded Successfully!")
        st.session_state.resume_text = get_text(uploaded_file)
    if st.session_state.resume_text is not None:
        if st.sidebar.button("Generate Mock Intervew"):
            with st.spinner("Your mock interview is being generated!! Hang Tight!"):
                # Generate feedback if both resume and job description are provided
                suggestions = ai_gen(['Generate 5 suggestions based on my resume', st.session_state.resume_text])
                st.session_state.resume_suggestion = suggestions
                questions = ai_gen(["I'm going to have an interview with %s for the %s position. give me 5 questions according to my resume" % (company, position), st.session_state.resume_text])
                st.session_state.resume_question = questions
        if st.sidebar.button("restart"):
            st.session_state.resume_text = None
            st.session_state.resume_suggestion = None
            st.session_state.resume_question = None
            st.session_state.resume_answer = None
            st.experimental_rerun()
    if st.session_state.resume_suggestion is not None or st.session_state.resume_question:
        st.subheader("Resume Suggestion")
        st.write(st.session_state.resume_suggestion)
        st.subheader("Mock Interview Questions")
        st.write(st.session_state.resume_question)
        st.subheader("Mock Interview Answer")
        st.session_state.resume_answer = st.text_input("Input your answers")
    if st.session_state.resume_answer is not None:
        if st.button("Submit Answer"):
            sss = "Questions:" + st.session_state.resume_question + "Answers:" + str(st.session_state.resume_answer)
            rate = ai_gen([
                "Rate me from 1 to 10. 1 is lowest, 10 is highest. and generate a short comment based on my answers to the questions",
                sss])
            st.write(rate)


if __name__ == "__main__":
    main()