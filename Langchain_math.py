import langchain
import streamlit as st
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain import hub
from langchain.agents import AgentExecutor
from langchain_experimental.tools import PythonREPLTool
from langchain.agents import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

wiki_api_wrapper = WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=4000)
wikipedia_tool = WikipediaQueryRun(api_wrapper=wiki_api_wrapper)


tools = [PythonREPLTool(), wikipedia_tool]


instructions = """You are an agent designed to answer user questions to the best of your ability.
You pride yourself in the accuracy of the responses you provide. You can,

1) write and execute python code to answer questions if necessary. You have access to a python REPL, which you can use to execute python code. 
2) look up facts and figures on Wikipedia using the wikipedia_tool.

Using these 2 tools you ensure to the best of your ability that your responses are grounded in fact and are as accurate as possible.

For better performance, follow these guidelines:
1) You might know the answer without running any code, but you should still run the code to double-check your answer.
2) If you get an error, debug your code and try again.
3) If you unsure about how to proceed, ask a clarifying question.
4) If despite your best efforts you are unable to come up with an accurate answer, just return "I don't know" as the answer.
"""
base_prompt = hub.pull("langchain-ai/react-agent-template")
prompt = base_prompt.partial(instructions=instructions)
agent = create_react_agent(ChatGroq(temperature=0, model_name="llama3-70b-8192"), tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
input = st.chat_input("What would you like to solve?")
if input:
    st.write(agent_executor.invoke({"input": input}))



