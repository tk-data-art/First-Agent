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

# Create the input box and assign the text to the variable "prompt"
if prompt := st.chat_input("How can I help you with your finances?"):
    
    # Now you can use "prompt" because it was defined in the line above
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
    # 1. Start the live run
        response_stream = finance_assistance_agent.run_live(prompt)
    
    # 2. Use st.write_stream to automatically handle the async_generator
    # This will create that cool "typing" effect on your website!
        full_response = st.write_stream(response_stream)