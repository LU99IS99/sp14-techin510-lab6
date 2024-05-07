import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Function to extract text from PDF file
def get_text_from_pdf(file):
    reader = PdfReader(file)
    text = []
    for page in reader.pages:
        text.append(page.extract_text())
    return "\n".join(text)

# Function to analyze financial data and generate advice
def analyze_and_advise(text_data, career, annual_income):
    # Here you would need to add actual data analysis logic based on the extracted text
    # For now, let's just prepare a sample advice prompt
    advice_prompt = (
        f"Generate personalized financial advice for a {career} with an annual income in the range of {annual_income}, "
        f"based on their financial transactions documented in the provided text."
    )
    advice = model.generate_content(advice_prompt)
    return advice.text

# Main function
def main():
    st.title("Personal Finance Advisor 🏦")

    # Sidebar for additional user input
    st.sidebar.header("Your Details")
    career = st.sidebar.text_input("Enter your career field")
    income_options = [
        "Less than $10,000",
        "$10,000 - $19,999",
        "$20,000 - $29,999",
        "$30,000 - $39,999",
        "$40,000 - $49,999",
        "$50,000 - $99,999",
        "$100,000 - $149,999",
        "More than $150,000"
    ]
    annual_income = st.sidebar.selectbox("Select your annual income range", income_options)

    # File uploader for bank statements in PDF format
    uploaded_file = st.file_uploader("Upload your bank statement (PDF format)", type="pdf")
    if uploaded_file is not None:
        text_data = get_text_from_pdf(uploaded_file)
        st.write("Bank statement uploaded and processed successfully!")
        st.text_area("Preview of extracted text:", text_data, height=250)
        
        if st.button("Analyze and Advise"):
            with st.spinner("Analyzing your financial data and generating advice..."):
                advice = analyze_and_advise(text_data, career, annual_income)
                st.subheader("Personalized Financial Advice")
                st.write(advice)

if __name__ == "__main__":
    main()
