from openai import OpenAI
import streamlit as st
from groq import Groq
from avatars import avatar_list

openai_models = ["gpt-4-0125-preview", "gpt-4-turbo-preview", "gpt-3.5-turbo-0125"]
groq_models = ["llama2-70b-4096", "mixtral-8x7b-32768", "gemma-7b-it"]
selected_model = st.selectbox(options=openai_models + groq_models, label= "Select a model", index=3)

openai_api_key = st.secrets["OPEN_AI_API_KEY"]
groq_api_key = st.secrets["GROQ_API_KEY"]


if "selected_avatar" not in st.session_state:
    st.session_state.selected_avatar = avatar_list[0]
    st.session_state.custom_prompt_content = avatar_list[0].custom_prompt


cols = st.columns(len(avatar_list))
for index, avatar in enumerate(avatar_list):
    with cols[index]:
        st.image(avatar.image_path, width=150)

        if st.button(f"Select '{avatar.title}'", key=f"select_{index}"):
            st.session_state.selected_avatar = avatar_list[index]
            st.session_state.custom_prompt_content = st.session_state.selected_avatar.custom_prompt
            st.session_state['sidebar_custom_prompt'] = st.session_state.custom_prompt_content
            # This updates the text_area widget manually to reflect the new avatar's custom prompt.
            st.rerun()

# Sidebar for custom prompt input
with st.sidebar:
    user_input = st.text_area("Custom System Prompt (optional)", value=st.session_state.custom_prompt_content, key="sidebar_custom_prompt")
    
    # Detects any change made by the user to the custom prompt
    if user_input != st.session_state.custom_prompt_content:
        st.session_state.custom_prompt_content = user_input

# Reflect the selected avatar and the custom or selected avatar's prompt
st.write(f"Selected Avatar: {st.session_state.selected_avatar.title}")
#st.write(f"Custom Prompt: {st.session_state.custom_prompt_content}")

# Ensure 'messages' exists in st.session_state, initializing if necessary
if "messages" not in st.session_state or not st.session_state.messages:
    st.session_state.messages = [{"role": "assistant", "content": user_input}]
else:
    # Assuming 'messages' is not empty, update the first message with the new user input
    st.session_state.messages[0]["content"] = user_input


for msg in st.session_state.messages[1:]:
   st.chat_message(msg["role"]).write(msg["content"])
   
if user_prompt := st.chat_input("How can I be of assistance?"):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    st.chat_message("user").write(user_prompt)
    
    if selected_model in openai_models:
        client = OpenAI(api_key=openai_api_key)
    elif selected_model in groq_models:
        client=Groq(api_key=groq_api_key)

    response = client.chat.completions.create(model=selected_model, messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)




# import streamlit as st

# # Main expander for chat completion
# with st.expander("Chat Completion", expanded=True):
#     # Immediate, top-level settings
#     user_prompt = st.text_area("Enter your prompt:", height=150)
#     model = st.selectbox("Choose the model:", ["Model 1", "Model 2", "Model 3"], index=0)  # Example models
#     temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.01)
#     max_tokens = st.number_input("Max Tokens", min_value=1, max_value=1000, value=200, step=1)

#     # Checkbox to toggle advanced settings
#     show_advanced = st.checkbox("Show Advanced Settings")

#     # Conditional display of advanced settings
#     if show_advanced:
#         top_p = st.slider("Top P", min_value=0.0, max_value=1.0, value=0.9, step=0.01)
#         frequency_penalty = st.slider("Frequency Penalty", min_value=0.0, max_value=2.0, value=0.0, step=0.01)
#         presence_penalty = st.slider("Presence Penalty", min_value=0.0, max_value=2.0, value=0.0, step=0.01)
#         stop_sequences = st.text_input("Stop Sequences", value="")
#         echo = st.checkbox("Echo", value=False)

#     submit_button = st.button("Generate Completion")

#     if submit_button:
#         # Placeholder for handling the request and generating a response.
#         st.write(f"Generated completion for the prompt: {user_prompt}")
#         # Note: Integrate your actual model/API call logic here.
