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
    
    with st.chat_message("assistant"):
        # 1. Create a placeholder for the "typing" effect
        placeholder = st.empty()
        full_text = ""
        
        # 2. Pass the prompt as a dictionary to fix the AttributeError
        # We wrap it in {"user_input": prompt} so the ADK can process it
        response_stream = finance_assistance_agent.run_live({"user_input": prompt})
        
        # 3. Manually loop through the async generator
        for chunk in response_stream:
            # Check if the chunk is an object with .text or just a string
            content = chunk.text if hasattr(chunk, 'text') else str(chunk)
            full_text += content
            # Update the UI in real-time with a cursor effect
            placeholder.markdown(full_text + "▌")
        
        # 4. Final update to remove the cursor
        placeholder.markdown(full_text)