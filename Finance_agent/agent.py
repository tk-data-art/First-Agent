import streamlit as st
import asyncio
from google.adk.agents import LlmAgent
from google.adk.runners import Runner, InMemorySessionService
from google.adk.tools import google_search

# --- SECTION 1: HELPER ---
def to_sync_generator(async_gen):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        while True:
            try:
                yield loop.run_until_complete(anext(async_gen))
            except StopAsyncIteration:
                break
    finally:
        loop.close()

# --- SECTION 2: AGENT ---
finance_assistance_agent = LlmAgent(
    name="finance_assistance_agent",
    model="gemini-2.0-flash", 
    tools=[google_search],
    instruction="Be a friendly finance assistant."
)

# --- SECTION 3: RUNNER ---
runner = Runner(
    agent=finance_assistance_agent,
    app_name="finance_assistant_app", 
    session_service=InMemorySessionService()
)

# --- SECTION 4: UI LOGIC (Add the fix here) ---
st.title("💰 Finance Assistant")

if prompt := st.chat_input("How can I help you with your finances?"):
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        # The FIX: Using 'input' instead of 'new_message'
        async_gen = runner.run_live(
            user_id="user_1", 
            session_id="finance_session",
            input=prompt 
        )
        
        # Use our helper to stream it to the UI
        st.write_stream(to_sync_generator(async_gen))