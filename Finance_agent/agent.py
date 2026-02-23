from google.adk.runners import Runner
from google.adk.session_services import InMemorySessionService

# 1. Create the memory service
session_service = InMemorySessionService()

# 2. Pass it to the Runner as a keyword-only argument
runner = Runner(
    agent=finance_assistance_agent,
    session_service=session_service
)



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

# import asyncio

# # 1. Helper to turn async into sync
# def to_sync_generator(async_gen):
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     try:
#         while True:
#             try:
#                 # Use the loop to pull the next chunk
#                 yield loop.run_until_complete(anext(async_gen))
#             except StopAsyncIteration:
#                 break
#     finally:
#         loop.close()

# # 2. Main Chat UI
# if prompt := st.chat_input("How can I help you with your finances?"):
#     with st.chat_message("user"):
#         st.write(prompt)

#     with st.chat_message("assistant"):
#         # Define the async generator call
#         async_gen = finance_assistance_agent.run_live({"user_input": prompt})
        
#         # Pass it through the helper to make it compatible with st.write_stream
#         st.write_stream(to_sync_generator(async_gen))



# ... (your agent and helper function code) ...

# Create a Runner to manage the agent
runner = Runner(agent=finance_assistance_agent)

if prompt := st.chat_input("How can I help you with your finances?"):
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        # The Runner handles the "model_copy" logic internally for you
        async_gen = runner.run_live(
            user_id="user_1", 
            session_id="finance_session",
            new_message=prompt # Pass the string directly here
        )
        
        # Use our helper to stream it to the UI
        st.write_stream(to_sync_generator(async_gen))