from google.adk.types import Message
import streamlit as st
import asyncio
from google.adk.agents import LlmAgent
from google.adk.runners import Runner, InMemorySessionService
from google.adk.tools import google_search

# --- SECTION 1: HELPER (Async to Sync) ---
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
    instruction="Be a friendly finance assistant for students in Dubai."
)

# --- SECTION 3: RUNNER ---
# app_name is REQUIRED here
runner = Runner(
    agent=finance_assistance_agent,
    app_name="finance_assistant_app", 
    session_service=InMemorySessionService()
)

# --- SECTION 4: UI LOGIC ---
st.title("💰 Finance Assistant")

if prompt := st.chat_input("Ask about your finance goals:"):
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        # 1. Wrap the string in a Message object
        # This fixes the AttributeError: 'str' object has no attribute 'role'
        user_msg = Message(role="user", content=prompt)
        
        # 2. Start the async run with the properly formatted message
        async_gen = runner.run_async(
            user_id="user_123", 
            session_id="finance_session_001",
            new_message=user_msg 
        )
        
        # 3. Stream it to the UI
        st.write_stream(to_sync_generator(async_gen))