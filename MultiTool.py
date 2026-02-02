import streamlit as st
from google import genai
from google.genai import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import re
import io
import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

def run_ai_teaching_assistant():
    st.title("???? AI Teahing Assistant")
    st.write("Ask me anything about various subjects, and ill provide an insightful answer.")
    if "history_ata" not in st.session_state:
        st.session_state.history_ata = []

    col_clear, col_export = st.columns([1, 2])

    with col_clear:
        if st.button("???? Clear Conversation", key="clear_ata"):
            st.session_state.history_ata = []
        
    with col_export:
        if st.session_state.history_ata:
            export_text = ""
            for idx, qa in enumerate(st.session_state.history_ata, start=1):
                export_text += f"Q{idx}: {qa['question']}\n"
                export_text += f"A{idx}: {qa['answer']}\n\n"

            bio = io.BytesIO()
            bio.write(export_text.encode("utf-8"))
            bio.seek(0)

            st.download_button(
                label="???? Export Chat History",
                data=bio,
                file_name="AI_Teaching_Assistant_Coversation.txt"
                mime="text/plain",
            )
    user_input = st.text_input("Enter your question here:", key="input_ata")

    if st.button("Ask", key="ask_ata"):
        if user_input.strip():
            with st.spinner("Generating AI response...."):
                response = generate_response(user_input.strip(), temperature=0.3)
            st.session_state.history_ata.append({"question": user_input.strip(), "answer": response})
            st.experimental_rerun()
        else:
            st.warning("Please ener a question before clicking Ask.")

    st.markdown("### Conversation History")
    for idx, qa in enumerate(st.session_state.history_ata, start=1):
        st.markdown(f"**Q{idx}:** {qa['question']}")
        st.markdown(f"**A{idx}:** {qa['answer']}")

def generate_response(prompt, temperature=0.3):
    try:
        contents = [types.content(role="user", parts=[types.Part.from_text(text=prompt)])]
        config_params = types.GenerateContentConfig(temperature=temperature)
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=contents, config=config_params)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
    
def generate_math_response(prompt, temperature=0.1):
    system_prompt = """You are a Math Mastermind - an expoert mathematics problem solver with expectional abiliteds in:
    - Algebra, Calculus, Geometry, Trignometry
    - Statistics, Probability, Linear Algebra
    - Discrete Mathematics, Number Theory
    - Mathematical Proofs and Logic
    - Applied Mathematics and word Problems
    
    For every math problem:
    1. Show clear step-by-step solutions
    2. Explain the mathematical reasoning
    3. Provide alternative solving methods when applicable
    4. Verify your answer when possible
    5. Use proper mathematical notation
    6. Break down complex problems into manageble parts
    
    Format your responses with:
    - Clear problem identification
    - step-by-step solution process
    - Final answer highlighted
    - Brief explaination of concepts used
    
    Always be precise, thorough, and educational in your mathematical explainations."""
    try:
        full_prompt = f"{system_prompt}n\Math Problem: {prompt}"
        contents = [types.Content(role="user", parts=[types.Part.from_text(text=full_prompt)])]
        config_params = types.GenerateContentConfig(temperature=temperature)
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=contents, config=config_params)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"