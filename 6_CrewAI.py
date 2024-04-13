import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from crewai_tools import BaseTool

# Streamlit secrets for API keys
openai_api_key = st.secrets["OPEN_AI_API_KEY"]
groq_api_key = st.secrets["GROQ_API_KEY"]
serp_api_key = st.secrets["SERP_API_KEY"]
groq_models = ["llama2-70b-4096", "mixtral-8x7b-32768", "gemma-7b-it"]

# Setup the language model
llm = ChatGroq(temperature=0.7, groq_api_key=groq_api_key, model_name=groq_models[1])

# Notes management tool
class NotesTool(BaseTool):
    name = "Notes Tool"
    description = "Manages a dynamic notes system to track user preferences and habits."

    def __init__(self):
        self.notes = {}

    def add_or_update_note(self, category, detail):
        self.notes[category] = detail

    def get_notes(self):
        return self.notes

    def _run(self, command: str, **kwargs):
        if command == "update":
            self.add_or_update_note(kwargs['category'], kwargs['detail'])
        elif command == "get":
            return self.get_notes()
        return "Notes updated"

notes_tool = NotesTool()

# Waiter agent setup
waiter = Agent(
    role='Waiter',
    goal='Engage in casual conversation while updating and maintaining user preference notes.',
    tools=[notes_tool],
    verbose=True,
    memory=True,
    backstory=(
        "As a dedicated Waiter, you are skilled in remembering customers' likes and dislikes, "
        "always ready to provide personalized service based on your detailed notes."
    )
)

# Task definition for the Waiter
conversation_task = Task(
    description=(
        "Engage the user in conversation, listen for any preference updates, and adjust notes accordingly."
    ),
    expected_output='Updated notes reflecting the conversation.',
    tools=[notes_tool],
    agent=waiter,
)

# Crew setup
crew = Crew(
    agents=[waiter],
    tasks=[conversation_task]
)

# Streamlit UI
st.title("Waiter Assistant")
user_input = st.text_input("Talk to the Waiter:", "")
if st.button("Update Conversation"):
    # Mock example to kickoff with user input
    crew.kickoff(inputs={'command': 'update', 'category': 'conversation', 'detail': user_input})
    st.write("Notes updated:")
    st.json(notes_tool.get_notes())

