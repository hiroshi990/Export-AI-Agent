import streamlit as st
import os
import json
import asyncio
from main import execute
from PIL import Image


im=Image.open(r"E:/export/utilities/Import.png")
executor = execute()
# Set up the page layout
st.set_page_config(page_title="Export Assistance AI", layout="wide",page_icon=im)
hide_default_format = """
    <style>
    #MainMenu {visibility: hidden; }
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_default_format, unsafe_allow_html=True)

st.markdown(
    """
<style>
    .st-emotion-cache-janbn0 {
        flex-direction: row-reverse;
        text-align: right;
    }
</style>
""",
    unsafe_allow_html=True,
)

messages = [{
    "author": "user",
    "message": "hi",
}, {
    "author": "assistant",
    "message": "I'm a bot"
}] * 3


st.title("🚛 Your AI Export Assistance")

# Sidebar for session controls
st.sidebar.title("Export Assistance AI")
st.sidebar.markdown("Your expert assistant for goods export to the USA & Europe.")

user_emoji="👤"
bot_emoji="🤖"




# Function to handle chat response
async def get_response(user_input):
    return await asyncio.to_thread(executor.run, user_input)

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Clear Chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"],
                        avatar=bot_emoji if message["role"] == "assistant" else user_emoji):
        st.markdown(message["content"])

# User input field
user_input = st.chat_input("Ask me about export regulations, compliance, or procedures...")

if user_input:
    # Append user input to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user",
                        avatar=user_emoji):
        st.markdown(user_input)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = asyncio.run(get_response(user_input))
            st.markdown(response)

    # Append AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

