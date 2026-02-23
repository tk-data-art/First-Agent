from google.adk.agents import LlmAgent
from google.adk.tools import google_search # Corrected path


finance_assistance_agent = LlmAgent(
    name= "finance_assistance_agent",
    model="gemini-2.5-flash",
    description= "A simple finance assistant that helps with user's finance goals.",
    instruction= """You are a friendly assistant.
    You can help user's generic questions on finance and help plan their finance goals.
    Be more friendly and positive.""",

    tools= [google_search],
)

root_agent = finance_assistance_agent

import streamlit as st

# ... (Keep your existing agent definition code above) ...

st.title("Finance Assistance Agent")
st.write("Hello! I am your friendly finance assistant. How can I help you today?")

# Create a text input for the user
user_input = st.chat_input("Type your finance question here...")

if user_input:
    # Display the user message
    with st.chat_message("user"):
        st.write(user_input)

    # Get the response from your ADK agent
    with st.chat_message("assistant"):
        # This assumes your ADK agent has a .run() or .chat() method
        response = finance_assistance_agent.chat(prompt)
        st.write(response)