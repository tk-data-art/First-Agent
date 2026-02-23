import streamlit as st
import asyncio
from google.adk.agents import LlmAgent
from google.adk.runners import Runner, InMemorySessionService
from google.adk.tools import google_search

# 1. THE HELPER
def to_sync_generator(async_gen):
    # ... (keep your existing generator code) ...

# 2. THE AGENT (Define this FIRST)
    finance_assistance_agent = LlmAgent(
    name="finance_assistance_agent",
    model="gemini-2.0-flash", 
    tools=[google_search],
    instruction="Be a friendly finance assistant."
)

# 3. THE RUNNER (Define this SECOND)
runner = Runner(
    agent= finance_assistance_agent, # This now exists!
    session_service=InMemorySessionService()
)

# 4. THE UI
st.title("💰 Finance Assistant")
if prompt := st.chat_input("Ask me something:"):
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        async_gen = runner.run_live(
            user_id="user_1", 
            session_id="finance_session",
            new_message=prompt
        )
        st.write_stream(to_sync_generator(async_gen))