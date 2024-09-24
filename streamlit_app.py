import streamlit as st
from openai import OpenAI
import json
import os
import time
import hashlib

CHAT_HISTORY_FILE = "chat_history.json"
UPDATE_INTERVAL = 1  # seconds

# Initialize the chat history file if it doesn't exist
if not os.path.exists(CHAT_HISTORY_FILE):
    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump([], f)

# Function to read chat history from the file
def read_chat_history():
    with open(CHAT_HISTORY_FILE, "r") as f:
        return json.load(f)

# Function to write chat history to the file
def write_chat_history(messages):
    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump(messages, f)

# Function to generate a unique emoji based on username
def generate_user_icon(username):
    # Hash the username to get a consistent, but unique result
    hash_value = int(hashlib.md5(username.encode()).hexdigest(), 16)
    emoji_index = hash_value % len(EMOJI_LIST)
    return EMOJI_LIST[emoji_index]

# List of emojis to use
EMOJI_LIST = [
    "🙂", "😎", "🤓", "😇", "😂", "😍", "🤡", "😃", "😅", "😎", 
    "😜", "🤗", "🤔", "😴", "😱", "😡", "🤠", "😈", "😇", "👻"
]

# Setting page layout
st.set_page_config(
    page_title="Multithread Chatbot with OpenAI GPT 3.5 with a Bot Trigger",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Sidebar for API Key and User Info
st.sidebar.header("About App")
st.sidebar.markdown('This is a multithreaded chatbot with OpenAI GPT 3.5 capable of iteration where the chatbot only responds when triggered created by <a href="https://ai.jdavis.xyz" target="_blank">0xjdavis</a>.', unsafe_allow_html=True)

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
username = st.sidebar.text_input("Enter your username:")

if not openai_api_key:
    st.sidebar.info("Please add your OpenAI API key to continue.", icon="🗝️")
elif not username:
    st.sidebar.info("Please enter a username to continue.", icon="🗣️")
else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Generate a unique icon for the user.
    user_icon = generate_user_icon(username)

    # Load the chat history from the file.
    chatroom_messages = read_chat_history()

    # Show title and description.
    st.title("Multithread Chatbot with OpenAI GPT 3.5 with a Bot Trigger")
    st.write("This is a multi-user chatroom where one participant is an AI chatbot.")
    st.write("Use the word `nurt` to trigger the bot.")

    # Display all chatroom messages with user icons and tooltips
    for message in chatroom_messages:
        icon = message.get("icon", "👤")
        content = message.get("content", "")
        role = message.get("role", "user")
        sender_name = message.get("sender_name", "")

        # Format the chat display with hover effect for the icon
        st.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <div style="position: relative;">
                    <span style="font-size: 24px; margin-right: 8px; cursor:pointer;" title="{sender_name}">{icon}</span>
                </div>
                <div style="background-color: {'#f1f1f1' if role == 'user' else '#e1f5fe'}; padding: 8px; border-radius: 8px;">
                    {content}
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Create a chat input field for user input.
    if prompt := st.chat_input("What's on your mind?"):
        # Add the user's message to the chat history and display it.
        chatroom_messages.append({"role": "user", "icon": user_icon, "content": f"{prompt}", "sender_name": username})
        write_chat_history(chatroom_messages)

        # Display the user's message immediately
        st.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <div style="position: relative;">
                    <span style="font-size: 24px; margin-right: 8px; cursor: pointer;" title="{username}">{user_icon}</span>
                </div>
                <div style="background-color: #f1f1f1; padding: 8px; border-radius: 8px;">
                    {prompt}
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Check if the prompt starts with "nurt"
        if prompt.lower().startswith("nurt"):
            # Generate a response using the OpenAI API.
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in chatroom_messages
                ],
            )

            # Extract the assistant's response from the OpenAI response object.
            assistant_message = response.choices[0].message.content

            # Add the assistant's message to the chat history and display it.
            chatroom_messages.append({"role": "assistant", "icon": "🤖", "content": f"{assistant_message}"})
            write_chat_history(chatroom_messages)

            # Display the assistant's message immediately
            st.markdown(f"""
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <div style="position: relative;">
                        <span style="font-size: 24px; margin-right: 8px; cursor:pointer;" title="Assistant">🤖</span>
                    </div>
                    <div style="background-color: #e1f5fe; padding: 8px; border-radius: 8px;">
                        {assistant_message}
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # Calendly
    st.sidebar.markdown("""
        <hr />
        <center>
        <div style="border-radius:8px;padding:8px;background:#fff";width:100%;">
        <img src="https://avatars.githubusercontent.com/u/98430977" alt="Oxjdavis" height="100" width="100" border="0" style="border-radius:50%"/>
        <br />
        <span style="height:12px;width:12px;background-color:#77e0b5;border-radius:50%;display:inline-block;"></span> <b style="color:#000000">I'm available for new projects!</b><br />
        <a href="https://calendly.com/0xjdavis" target="_blank"><button style="background:#126ff3;color:#fff;border: 1px #126ff3 solid;border-radius:8px;padding:8px 16px;margin:10px 0">Schedule a call</button></a><br />
        </div>
        </center>
        <br />
    """, unsafe_allow_html=True)

    # Copyright
    st.sidebar.caption("©️ Copyright 2024 J. Davis")

    # Auto-refresh the chat every few seconds to show new messages.
    while True:
        time.sleep(UPDATE_INTERVAL)
        new_messages = read_chat_history()
        if new_messages != chatroom_messages:
            st.rerun()
