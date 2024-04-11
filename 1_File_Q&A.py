from openai import OpenAI
import streamlit as st
from groq import Groq
import custom_agents

openai_models = ["gpt-4-0125-preview", "gpt-4-turbo-preview", "gpt-3.5-turbo-0125"]
groq_models = ["llama2-70b-4096", "mixtral-8x7b-32768", "gemma-7b-it"]
#selected_model = st.selectbox(options=openai_models + groq_models, label= "Select a model", index=3)

openai_api_key = st.secrets["OPEN_AI_API_KEY"]
groq_api_key = st.secrets["GROQ_API_KEY"]

# # Use st.sidebar.expander for sidebar configuration
# with st.sidebar.expander("LLM Settings", expanded=True):
#     # Immediate, top-level settings in the sidebar
#     user_prompt = st.text_area("Customize prompt(optional)", height=150)
#     model = st.selectbox("Choose the model:", openai_models + groq_models, index=0)
#     temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.01)
#     max_tokens = st.number_input("Max Tokens", min_value=1, max_value=4096, value=3000, step=100)

#     # Checkbox to toggle advanced settings in the sidebar
#     show_advanced = st.checkbox("Show Advanced Settings")

#     # Conditional display of advanced settings
#     if show_advanced:
#         top_p = st.slider("Top P", min_value=0.0, max_value=1.0, value=0.9, step=0.01)
#         frequency_penalty = st.slider("Frequency Penalty", min_value=0.0, max_value=2.0, value=0.0, step=0.01)
#         presence_penalty = st.slider("Presence Penalty", min_value=0.0, max_value=2.0, value=0.0, step=0.01)
#         stop_sequences = st.text_input("Stop Sequences", value="")
#         echo = st.checkbox("Echo", value=False)

# # Submit button in the main page area
# submit_button = st.button("Generate Completion")

# if submit_button:
#     # Placeholder for handling the request and generating a response.
#     st.write(f"Generated completion for the prompt: {user_prompt}")
#     # Note: Integrate your actual model/API call logic here.


# Dynamically list agent roles
agent_roles = [attr for attr in dir(custom_agents) if isinstance(getattr(custom_agents, attr), custom_agents.Agent)]

# UI for selecting an agent
selected_agent_role = st.sidebar.selectbox("Select an Agent", options=agent_roles, index=0)

# Get the selected agent object dynamically
selected_agent = getattr(custom_agents, selected_agent_role)


# UI for Agent Parameters
with st.sidebar:
    st.write("Agent Details")
    agent_role = st.text_input("Agent Role", value=selected_agent.role)
    agent_goal = st.text_input("Agent Goal", value=selected_agent.goal)
    agent_backstory = st.text_area("Agent Backstory", value=selected_agent.backstory, height=150)
    verbose = st.checkbox("Verbose", value=selected_agent.verbose)
    allow_delegation = st.checkbox("Allow Delegation", value=selected_agent.allow_delegation)
    memory = st.checkbox("Memory", value=selected_agent.memory)
    # Tools is a placeholder for future implementation
    st.text_input("Tools", value="None", disabled=True)

# LLM Settings Expander
with st.sidebar.expander("LLM Settings", expanded=True):
    # Immediate, top-level settings in the sidebar
    model = st.selectbox("Choose the model:", ["gpt-4-0125-preview", "gpt-4-turbo-preview", "gpt-3.5-turbo-0125", "llama2-70b-4096", "mixtral-8x7b-32768", "gemma-7b-it"], index=0)
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.01)
    max_tokens = st.number_input("Max Tokens", min_value=1, max_value=4096, value=300, step=100)
    
    # Conditional display of advanced settings
    show_advanced = st.checkbox("Show Advanced Settings")
    if show_advanced:
        top_p = st.slider("Top P", min_value=0.0, max_value=1.0, value=0.9, step=0.01)
        frequency_penalty = st.slider("Frequency Penalty", min_value=0.0, max_value=2.0, value=0.0, step=0.01)
        presence_penalty = st.slider("Presence Penalty", min_value=0.0, max_value=2.0, value=0.0, step=0.01)
        stop_sequences = st.text_input("Stop Sequences", value="")
        echo = st.checkbox("Echo", value=False)

# Submit button and action
if st.button("Generate Completion"):
    # For demonstration, let's print the selected agent's modified details
    agent_info = {
        "Role": agent_role,
        "Goal": agent_goal,
        "Backstory": agent_backstory,
        "Verbose": verbose,
        "Allow Delegation": allow_delegation,
        "Memory": memory,
        # Assuming 'llm' would be dynamically created or modified based on LLM settings
        "LLM Settings": {
            "Model": model,
            "Temperature": temperature,
            "Max Tokens": max_tokens,
            "Top P": top_p if show_advanced else "N/A",
            "Frequency Penalty": frequency_penalty if show_advanced else "N/A",
            "Presence Penalty": presence_penalty if show_advanced else "N/A",
            "Stop Sequences": stop_sequences if show_advanced else "N/A",
            "Echo": echo if show_advanced else "N/A",
        }
    }
    st.write(agent_info)
