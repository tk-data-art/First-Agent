import streamlit as st
import asyncio
from google.adk.agents import LlmAgent
from google.adk.runners import Runner, InMemorySessionService
from google.adk.tools import google_search

# 1. HELPER FUNCTION (Must be defined before the UI uses it)
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

# 2. AGENT DEFINITION (Define this BEFORE the Runner)
finance_assistance_agent = LlmAgent(
    name="finance_assistance_agent",
    model="gemini-2.0-flash", 
    tools=[google_search],
    instruction="You are a friendly finance assistant."
)

# 3. RUNNER INITIALIZATION
# This satisfies the requirement for both 'app_name' and 'agent'
runner = Runner(
    agent=finance_assistance_agent,
    app_name="finance_assistant_app", 
    session_service=InMemorySessionService()
)
# 4. STREAMLIT UI LOGIC
st.title("💰 Finance Assistant")

if prompt := st.chat_input("How can I help you today?"):
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        # The Runner manages the conversation state
        async_gen = runner.run_live(
            user_id="user_1", 
            session_id="finance_session",
            new_message=prompt
        )
        # Pass the stream to our helper
        st.write_stream(to_sync_generator(async_gen))