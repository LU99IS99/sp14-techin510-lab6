import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Function to generate questions and feedback using the Gemini model
def ai_generate_content(prompt):
    response = model.generate_content(prompt)
    return response.text

# Main function
def main():
    st.title("Mental Health Companion 🌿")
    
    # Sidebar for user input about how they are feeling
    st.sidebar.markdown("### How are you feeling today?")
    emotion_rating = st.sidebar.slider("Rate your feelings (1 being the best, 5 being stressed):", 1, 5, 3)

    # Generate a question based on the emotion rating
    emotion_prompts = [
        "Generate a comforting question for someone feeling at the top of their game.",
        "Generate a motivational question for someone feeling slightly off their peak.",
        "Generate a reflective question for someone feeling neutral.",
        "Generate a supportive question for someone feeling a bit low.",
        "Generate a deep question for someone feeling very stressed."
    ]
    question_prompt = emotion_prompts[emotion_rating - 1]  # Adjust index for 0-based array
    question = ai_generate_content(question_prompt)
    
    # Display question and get user response
    user_response = st.text_input("Reflect on this:", question)

    # Generate feedback based on the user's emotional rating and their response
    if st.button("Submit"):
        feedback_prompt = [
            "Generate positive feedback for a top-rated response:",
            "Generate encouraging feedback for a good response:",
            "Generate balanced feedback for a neutral response:",
            "Generate reassuring feedback for a slightly negative response:",
            "Generate supportive feedback for a stressed response:"
        ]
        feedback_query = feedback_prompt[emotion_rating - 1]  # Adjust index for 0-based array
        feedback = ai_generate_content(f"{feedback_query} {user_response}")
        st.success("Thank you for sharing. Here's something for you:")
        st.info(feedback)

if __name__ == "__main__":
    main()
