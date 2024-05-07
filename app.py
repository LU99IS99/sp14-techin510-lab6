import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Function to generate mental health support advice
def ai_gen_support(prompts):
    response = model.generate_content(prompts)
    return response.text

# Main function
def main():
    st.title("Mental Health Companion 🌿")
    
    # Sidebar for user input about how they are feeling
    user_feeling = st.sidebar.text_area("How are you feeling today?", help="Describe your feelings or any stress you are experiencing.")

    # Button to generate support message
    if st.sidebar.button("Get Support"):
        with st.spinner("Finding some ways to help you..."):
            # Generate mental health advice based on user's feelings
            support_message = ai_gen_support([
                "Provide supportive advice and mindfulness exercises for someone feeling:", 
                user_feeling
            ])
            st.session_state.support_message = support_message
    
    # Display the generated advice
    if 'support_message' in st.session_state:
        st.subheader("Here’s some advice and support for you:")
        st.write(st.session_state.support_message)

    # Clear state button
    if st.sidebar.button("Clear"):
        if 'support_message' in st.session_state:
            del st.session_state.support_message
        st.experimental_rerun()

if __name__ == "__main__":
    main()
