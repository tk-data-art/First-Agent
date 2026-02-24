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
                # Manually stepping through the async generator
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
    instruction="Be a friendly finance assistant for international students in Dubai."
)

# --- SECTION 3: RUNNER ---
runner = Runner(
    agent=finance_assistance_agent,
    app_name="finance_assistant_app", 
    session_service=InMemorySessionService()
)

# --- SECTION 4: UI LOGIC ---
st.title("💰 Finance Assistant")

if prompt := st.chat_input("How can I help you today?"):
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        # The FIX: We pass the message as a dictionary to bypass AttributeErrors
        user_msg = {"role": "user", "content": prompt}
        
        # Use run_async to handle the turn-based conversation
        async_gen = runner.run_async(
            user_id="user_123", 
            session_id="finance_session_001",
            new_message=user_msg 
        )
        
        # Stream the typing effect
        st.write_stream(to_sync_generator(async_gen))