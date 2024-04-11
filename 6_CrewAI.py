from crewai import Agent
import streamlit as st
from langchain_groq import ChatGroq
from crewai import Task
from crewai import Crew, Process
from contextlib import redirect_stdout
import io
import streamlit as st



openai_api_key = st.secrets["OPEN_AI_API_KEY"]
groq_api_key = st.secrets["GROQ_API_KEY"]
serp_api_key = st.secrets["SERP_API_KEY"]
groq_models = ["llama2-70b-4096", "mixtral-8x7b-32768", "gemma-7b-it"]


from crewai_tools import WebsiteSearchTool
WST = WebsiteSearchTool()

llm = ChatGroq(
            temperature=0.7, 
            groq_api_key = groq_api_key, 
            model_name=groq_models[1]
        )


# Creating a senior researcher agent with memory and verbose mode
researcher = Agent(
  role='Senior Researcher',
  goal='Uncover groundbreaking technologies in {topic}',
  verbose=True,
  memory=True,
  backstory=(
    "Driven by curiosity, you're at the forefront of"
    "innovation, eager to explore and share knowledge that could change"
    "the world."
  ),
  tools=[WST],
  allow_delegation=True,
  llm = llm
)

# Creating a writer agent with custom tools and delegation capability
writer = Agent(
  role='Writer',
  goal='Narrate compelling tech stories about {topic}',
  verbose=True,
  memory=True,
  backstory=(
    "With a flair for simplifying complex topics, you craft"
    "engaging narratives that captivate and educate, bringing new"
    "discoveries to light in an accessible manner."
  ),
  tools=[WST],
  allow_delegation=False,
  llm = llm
)


# Research task
research_task = Task(
  description=(
    "Identify the next big trend in {topic}."
    "Focus on identifying pros and cons and the overall narrative."
    "Your final report should clearly articulate the key points"
    "its market opportunities, and potential risks."
  ),
  expected_output='A comprehensive 3 paragraphs long report on the latest AI trends.',
  tools=[WST],
  agent=researcher,
  human_input=True,
)

# Writing task with language model configuration
write_task = Task(
  description=(
    "Compose an insightful article on {topic}."
    "Focus on the latest trends and how it's impacting the industry."
    "This article should be easy to understand, engaging, and positive."
  ),
  expected_output='A 4 paragraph article on {topic} advancements formatted as markdown.',
  tools=[WST],
  agent=writer,
  async_execution=False,
  output_file='new-blog-post.md'  # Example of output customization
)


# Forming the tech-focused crew with enhanced configurations
crew = Crew(
  agents=[researcher, writer],
  tasks=[research_task, write_task],
  process=Process.sequential, # Optional: Sequential task execution is default,
  verbose=True,
  full_output=True
)


if topic := st.chat_input("What would you like to research?"):
    # Starting the task execution process with enhanced feedback
    result = crew.kickoff(inputs={'topic': topic})
    st.text_area("Agent's Thought Process:", result, height=300)

st.write(result)

