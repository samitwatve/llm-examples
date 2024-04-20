import streamlit as st
from langchain.llms import OpenAI
from langchain.agents import MRKLAgent, MemoryAgent


# Define the Menu (modify this with your actual menu items)
menu = {
    "Appetizers": {
        "Oysters Rockefeller": "Fresh oysters baked with spinach, Pernod, and breadcrumbs.",
        "Beef Carpaccio": "Thinly sliced beef with shaved parmesan, arugula, and truffle oil.",
    },
    "Main Courses": {
        "Filet Mignon": "Tenderloin steak with your choice of sauce and sides.",
        "Dover Sole Meunière": "Whole dover sole pan-fried in brown butter and lemon.",
    },
    "Desserts": {
        "Chocolate Soufflé": "Warm chocolate soufflé with vanilla ice cream.",
        "Cheese Plate": "Selection of artisanal cheeses with accompaniments.",
    },
}

# Initialize Langchain components
llm = OpenAI()
memory_agent = MemoryAgent()  # Stores waiter's notes
agent = MRKLAgent(llm, memory=memory_agent)

def get_initial_greeting():
  """Initial greeting to start conversation"""
  prompt = """You are a waiter at a high-end establishment. You engage customers in a casual but friendly way to learn more about them and their preferences. You keep individualized notes about EACH customer using a memory agent. 

  Start by welcoming the customer(s) and introduce yourself.

  **Internal Monologue:** I have no knowledge about the customer(s) yet.

  **Notes:** (This section will be filled with information as you learn more about the customer(s))
  """
  response = agent.run(prompt)
  return response.text

def process_user_response(user_response):
  """Process user response and update memory agent"""
  # Update prompt based on conversation history and current understanding (stored in memory_agent)
  prompt = f"""The customer says: {user_response}

  **Internal Monologue:** Based on the conversation so far, ... (analyze user response to update understanding)

  **Notes:** {memory_agent.get_memory()} (update notes based on new information)
  """
  response = agent.run(prompt)
  # Update memory_agent with extracted information (party size, dietary restrictions etc.)
  # This part requires additional logic to parse the internal monologue and update memory_agent accordingly
  return response.text

def recommend_menu(notes):
  """Uses Langchain agent to recommend menu based on information in notes"""
  # Access relevant information from notes (party size, dietary restrictions)
  prompt = f"""Based on your understanding of the customer(s) (refer to notes), recommend suitable appetizers, main courses, and desserts from the following menu:

  {menu}

  **Notes:** {notes}
  """
  response = agent.run(prompt)
  return response.text

def main():
  """Main function for the Streamlit app"""
  st.title("The High-End Restaurant Waiter")

  waiter_greeting = get_initial_greeting()
  st.write(waiter_greeting)

  user_response = st.text_input("Customer Response:")

  if user_response:
    waiter_response = process_user_response(user_response)
    st.write(waiter_response)

    # After sufficient interaction, recommend menu
    if st.button("Recommend Menu"):
      notes = memory_agent.get_memory()
      recommendations = recommend_menu(notes)
      st.write(recommendations)

if __name__ == "__main__":
  main()

