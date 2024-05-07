import os
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Function to analyze financial data and generate advice
def analyze_and_advise(data, career, annual_income):
    # Example: Summarize expenses and categorize
    data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')
    monthly_expense = data.groupby(data['Date'].dt.to_period('M')).sum()
    high_spending_categories = data.groupby('Category').sum().sort_values(by='Amount', ascending=False).head(3)
    
    # Generate financial advice taking career and income into account
    advice_prompt = (
        f"Generate personalized financial advice for a {career} earning {annual_income} annually, "
        f"focusing on high spending in {', '.join(high_spending_categories.index.tolist())} and total monthly expenses."
    )
    advice = model.generate_content(advice_prompt)
    return monthly_expense, high_spending_categories, advice.text

# Main function
def main():
    st.title("Personal Finance Advisor 🏦")

    # Sidebar for additional user input
    st.sidebar.header("Your Details")
    career = st.sidebar.text_input("Enter your career field")
    annual_income = st.sidebar.number_input("Enter your annual income (in USD)", min_value=10000, max_value=1000000, step=1000)

    # File uploader for bank statements
    uploaded_file = st.file_uploader("Upload your bank statement (CSV format)", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        data['Date'] = pd.to_datetime(data['Date'])
        st.write("Data Uploaded Successfully!")
        st.write(data.head())  # Display a preview of the data
        
        if st.button("Analyze and Advise"):
            with st.spinner("Analyzing your expenses and generating advice..."):
                monthly_expense, high_spending_categories, advice = analyze_and_advise(data, career, annual_income)
                st.subheader("Monthly Expenses Summary")
                st.bar_chart(monthly_expense)
                st.subheader("High Spending Categories")
                st.write(high_spending_categories)
                st.subheader("Personalized Financial Advice")
                st.write(advice)

if __name__ == "__main__":
    main()
