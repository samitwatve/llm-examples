from openai import OpenAI
import streamlit as st
from groq import Groq
import custom_agents

openai_models = ["gpt-4-0125-preview", "gpt-4-turbo-preview", "gpt-3.5-turbo-0125"]
groq_models = ["llama2-70b-4096", "mixtral-8x7b-32768", "gemma-7b-it"]
openai_api_key = st.secrets["OPEN_AI_API_KEY"]
groq_api_key = st.secrets["GROQ_API_KEY"]

# Use st.sidebar.expander for sidebar configuration
with st.sidebar.expander("LLM Settings", expanded=True):
    # Immediate, top-level settings in the sidebar
    user_prompt = st.text_area("Customize prompt(optional)", height=150)
    model = st.selectbox("Choose the model:", openai_models + groq_models, index=0)
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.01)
    max_tokens = st.number_input("Max Tokens", min_value=1, max_value=4096, value=3000, step=100)

    # Checkbox to toggle advanced settings in the sidebar
    show_advanced = st.checkbox("Show Advanced Settings")

    # Conditional display of advanced settings
    if show_advanced:
        top_p = st.slider("Top P", min_value=0.0, max_value=1.0, value=0.9, step=0.01)
        frequency_penalty = st.slider("Frequency Penalty", min_value=0.0, max_value=2.0, value=0.0, step=0.01)
        presence_penalty = st.slider("Presence Penalty", min_value=0.0, max_value=2.0, value=0.0, step=0.01)
        stop_sequences = st.text_input("Stop Sequences", value="")
        echo = st.checkbox("Echo", value=False)

# Submit button in the main page area
submit_button = st.button("Generate Completion")

if submit_button:
    # Placeholder for handling the request and generating a response.
    st.write(f"Generated completion for the prompt: {user_prompt}")
    # Note: Integrate your actual model/API call logic here.


