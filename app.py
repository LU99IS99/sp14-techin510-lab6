import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Function to generate targeted questions based on emotional state
def generate_questions(emotion_rating):
    # Define questions for each level of emotion
    questions = {
        1: "What are some achievements that make you proud of yourself?",
        2: "What's a small victory you had recently that you can build on?",
        3: "What are things you usually enjoy that you've been avoiding?",
        4: "What’s been worrying you lately, and what might help?",
        5: "Describe a recent situation where you felt overwhelmed or stressed."
    }
    return questions.get(emotion_rating, "How can I assist you further?")

# Function to provide feedback based on user's emotional rating
def provide_feedback(emotion_rating):
    feedback = {
        1: "You're the best! Trust yourself!",
        2: "Remember, every step forward is progress.",
        3: "You're doing well. Let's try to reconnect with what brings you joy.",
        4: "It’s okay to have rough days. Let's think about positive changes.",
        5: "You're good! Taking time to reflect is a strong first step."
    }
    return feedback.get(emotion_rating, "Keep going, you're doing great!")

# Main function
def main():
    st.title("Mental Health Companion 🌿")
    
    # Sidebar for user input about how they are feeling
    st.sidebar.markdown("### How are you feeling today?")
    emotion_rating = st.sidebar.slider("Rate your feelings (1 being the best, 5 being stressed):", 1, 5, 3)
    question = generate_questions(emotion_rating)
    
    # Display question based on emotional state
    user_response = st.text_input("Reflect on this:", question)

    # Button to submit response and get feedback
    if st.button("Submit"):
        feedback = provide_feedback(emotion_rating)
        st.success("Thank you for sharing. Here's something for you:")
        st.info(feedback)

if __name__ == "__main__":
    main()
