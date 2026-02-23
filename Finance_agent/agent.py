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
if prompt := st.chat_input("Ask me anything:"):
    # ... (your chat logic using runner.run_live) ...