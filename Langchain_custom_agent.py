import streamlit as st
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.agents.tools import Tool
from langchain.chains import LLMMathChain
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.tools import PythonREPLTool
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableConfig
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchResults
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.utilities import SerpAPIWrapper

wiki_api_wrapper = WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=4000)
wikipedia_tool = WikipediaQueryRun(api_wrapper=wiki_api_wrapper)
search_wrapper = DuckDuckGoSearchAPIWrapper(region="US", time="d", max_results=2)
memory = ChatMessageHistory(session_id="test-session")


openai_api_key = st.secrets["OPEN_AI_API_KEY"]
groq_api_key = st.secrets["GROQ_API_KEY"]
serpapi_api_key = st.secrets["SERP_API_KEY"]


params = {"engine": "bing", "gl": "us", "hl": "en",}
SERP_search = SerpAPIWrapper(serpapi_api_key = serpapi_api_key, params = params)
DDGsearch = DuckDuckGoSearchResults(api_wrapper=search_wrapper)
# search_tool = Tool(
#             name = "Duck Duck Go Search Results Tool",
#             func = DDGsearch.run,
#             description="Useful for search for information on the internet"
#         )
search_tool = Tool(
            name = "Search Results Tool",
            func = SERP_search.run,
            description="Useful for search for information on the internet"
        )

tools = [PythonREPLTool(), wikipedia_tool, search_tool]

instructions = """You are an agent designed to answer user questions to the best of your ability.
You pride yourself in the accuracy of the responses you provide. You can,

1) write and execute python code to answer questions if necessary. You have access to a python REPL, which you can use to execute python code. 
2) look up encyclopedia like articles on Wikipedia using the wikipedia_tool.
3) look up facts and figures on the internet using the Search Results Tool

Using these tools you ensure to the best of your ability that your responses are grounded in fact and are as accurate as possible.

For better performance, follow these guidelines:
1) You might know the answer without running any code, but you should still run the code to double-check your answer.
2) Similarly you might know the answer without looking up facts and figures, but you should still cross-check your answers 
   with information on wikipedia or the broader internet. Sometimes counter-intuitive results will be revealed 
   to you. 
3) If you get an error, debug your code and try again or use the tools available to find solutions
4) If you're unsure about how to proceed or stuck at a particular step, ask the human user for clarication and help.
5) If despite your best efforts you are unable to come up with an accurate answer, just return "I don't know" as the answer. 
   Under no circumstances should you try to come up with an incorrect answer.
"""

##The base prompt is pulled from https://smith.langchain.com/hub/langchain-ai/react-agent-template
## https://medium.com/@terrycho/how-langchain-agent-works-internally-trace-by-using-langsmith-df23766e7fb4


base_prompt = hub.pull("langchain-ai/react-agent-template")
# base_prompt = hub.pull("hwchase17/react")
prompt = base_prompt.partial(instructions=instructions)

agent = create_react_agent(ChatGroq(temperature=0, model_name="llama3-70b-8192"), tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Create an in-memory chat history
memory = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in memory:
        memory[session_id] = ChatMessageHistory()
    return memory[session_id]


agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    # This is needed because in most real world scenarios, a session id is needed
    # It isn't really used here because we are using a simple in memory ChatMessageHistory
    input_messages_key="input",
    history_messages_key="chat_history",
    handle_parsing_errors = True,
    early_stopping_method = "generate",
    max_execution_time = 120,
    max_iterations = 3,
    memory=memory
)

session_id = "test-session"
output_container = st.empty()
input = st.chat_input("How tall is Mt Everest?")
if input:
    output_container = output_container.container()
    output_container.chat_message("user").write(input)

    answer_container = output_container.chat_message("assistant", avatar="🦜")
    st_callback = StreamlitCallbackHandler(answer_container)
    cfg = RunnableConfig()
    cfg["callbacks"] = [st_callback]
    cfg["configurable"] = {"session_id": session_id}
    #cfg["max_iterations"] = 3

    answer2 = agent_with_chat_history.invoke({"input": input, "chat_history": []}, cfg)
    answer_container.write(answer2["output"])
    st.write(get_session_history(session_id))
