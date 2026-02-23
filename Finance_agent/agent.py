#from google.adk.agents import LlmAgent
#from google.adk.tools import google_search # Corrected path

import streamlit as st
st.title("Hello World")

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