import os
import pandas as pd
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

# Function to process financial data from CSV
def process_csv_data(data):
    # Assuming data has columns 'Date', 'Description', and 'Amount'
    data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')
    return data

# Function to analyze financial data and generate advice
def analyze_and_advise(text_data, career, annual_income, data_type):
    if data_type == 'pdf':
        # Process PDF data (currently using placeholder text for demonstration)
        advice_prompt = (
            f"Generate personalized financial advice for a {career} with an annual income in the range of {annual_income}, "
            f"based on their financial transactions documented in the provided text."
        )
    elif data_type == 'csv':
        # Process CSV data
        advice_prompt = (
            f"Generate personalized financial advice for a {career} earning {annual_income} annually, "
            f"focusing on high spending and total monthly expenses."
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

    # File uploader for bank statements in PDF and CSV format
    uploaded_file = st.file_uploader("Upload your bank statement (PDF or CSV format)", type=["pdf", "csv"])
    if uploaded_file is not None:
        file_type = uploaded_file.type
        if file_type == "application/pdf":
            text_data = get_text_from_pdf(uploaded_file)
            data_type = 'pdf'
            st.write("PDF file uploaded and processed successfully!")
            st.text_area("Preview of extracted text:", text_data, height=250)
        elif file_type == "text/csv":
            data = pd.read_csv(uploaded_file)
            data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
            data = process_csv_data(data)
            data_type = 'csv'
            st.write("CSV file uploaded and processed successfully!")
            st.write(data.head())  # Display a preview of the data
        
        if st.button("Analyze and Advise"):
            with st.spinner("Analyzing your financial data and generating advice..."):
                advice = analyze_and_advise(text_data if data_type == 'pdf' else data, career, annual_income, data_type)
                st.subheader("Personalized Financial Advice")
                st.write(advice)

if __name__ == "__main__":
    main()
