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
st.write(f"Custom Prompt: {st.session_state.custom_prompt_content}")


allowed_types = ['txt', 'xls', 'pdf', 'doc', 'md', 'json', 'py', 'R']
uploaded_file = st.sidebar.file_uploader("Choose a file", type=allowed_types)


def parse_file(uploaded_file):
    """
    Parses the content of an uploaded file.
    
    Args:
    uploaded_file: The uploaded file object from Streamlit's file_uploader.

    Returns:
    A string containing the content of the file.
    """
    # Ensure there is a file to process
    if uploaded_file is not None:
        # Determine the file type from the file name
        file_type = uploaded_file.name.split('.')[-1]
        
        # Process a Python file
        if file_type == 'py':
            # Read the content of the file
            content = uploaded_file.getvalue().decode("utf-8")
            return content
        # Placeholder for additional file types
        # elif file_type == 'txt':
        #     ...
    else:
        # Return None or an appropriate message if no file is uploaded
        return None

if uploaded_file is not None:
    st.write(parse_file(uploaded_file))


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

