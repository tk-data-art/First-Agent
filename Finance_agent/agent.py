import streamlit as st
import asyncio
from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.adk.runners import Runner, InMemorySessionService # Check path as discussed

# 1. HELPER
def to_sync_generator(async_gen):
    # ... (keep your existing to_sync_generator code) ...

# 2. DEFINE AGENT FIRST
    finance_assistance_agent = LlmAgent(
    name="finance_assistance_agent",
    model="gemini-2.5-flash", 
    tools=[google_search],
    instruction="Be a friendly finance assistant."
)

# 3. DEFINE RUNNER SECOND (Uses the agent above)
runner = Runner(
    agent=finance_assistance_agent,
    session_service=InMemorySessionService()
)

# 4. UI LOGIC
st.title("💰 Finance Agent")
# Line 27: The "if" statement
if prompt := st.chat_input("How can I help you with your finances?"):
    # Everything below this must be indented by 4 spaces or 1 Tab
    with st.chat_message("user"):
        st.write(prompt) # Line 28 - This must be indented!

    with st.chat_message("assistant"):
        # This code is also inside the "if", so it stays indented
        async_gen = runner.run_live(
            user_id="user_1", 
            session_id="finance_session",
            new_message=prompt
        )
        
        # Use the sync generator helper we built
        st.write_stream(to_sync_generator(async_gen))