import streamlit as st
from openai import OpenAI
import hashlib

# List of emojis to use
EMOJI_LIST = [
    "🙂", "😎", "🤓", "😇", "😂", "😍", "🤡", "😃", "😅", "😎", 
    "😜", "🤗", "🤔", "😴", "😱", "😡", "🤠", "😈", "😇", "👻"
]

# Function to generate a unique emoji based on username
def generate_user_icon(username):
    hash_value = int(hashlib.md5(username.encode()).hexdigest(), 16)
    emoji_index = hash_value % len(EMOJI_LIST)
    return EMOJI_LIST[emoji_index]

# Setting page layout
st.set_page_config(
    page_title="Multithread Chatbot with OpenAI GPT 3.5",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Sidebar for API Key and User Info
st.sidebar.header("About App")
st.sidebar.markdown('This is a multithreaded chatbot with OpenAI GPT 3.5 capable of iteration created by <a href="https://ai.jdavis.xyz" target="_blank">0xjdavis</a>.', unsafe_allow_html=True)

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
username = st.sidebar.text_input("Enter your username:")

if not openai_api_key:
    st.sidebar.info("Please add your OpenAI API key to continue.", icon="🗝️")
elif not username:
    st.sidebar.info("Please enter a username to continue.", icon="🗣️")
else:
    # Create an OpenAI client
    client = OpenAI(api_key=openai_api_key)
    
    # Generate a unique icon for the user
    user_icon = generate_user_icon(username)
    
    # Show title and description
    st.title("Multithread Chatbot with OpenAI GPT 3.5")
    st.write("This is a multi-user chatroom where one participant is an AI chatbot. Use 'nurt' to trigger AI suggestions.")
    
    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        icon = message.get("icon", "👤")
        content = message.get("content", "")
        sender_name = message.get("sender_name", "")
        st.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <div style="position: relative;">
                    <span style="font-size: 24px; margin-right: 8px; cursor:pointer;" title="{sender_name}">{icon}</span>
                </div>
                <div style="background-color: {'#f1f1f1' if sender_name != 'Assistant' else '#e1f5fe'}; padding: 8px; border-radius: 8px;">
                    {content}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Create a chat input field for user input
    if prompt := st.chat_input("What's on your mind?"):
        # Add the user's message to the chat history
        st.session_state.chat_history.append({"icon": user_icon, "content": prompt, "sender_name": username})
        
        # Check if the trigger word "nurt" is in the prompt
        if "nurt" in prompt.lower():
            # Generate a response using the OpenAI API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user" if m["sender_name"] != "Assistant" else "assistant", "content": m["content"]}
                    for m in st.session_state.chat_history
                ],
            )
            
            # Extract the assistant's response
            assistant_message = response.choices[0].message.content
            
            # Add the assistant's message to the chat history
            st.session_state.chat_history.append({"icon": "🤖", "content": assistant_message, "sender_name": "Assistant"})
        
        # Rerun the app to display the new messages
        st.rerun()

# Calendly
st.sidebar.markdown("""
    <hr />
    <center>
    <div style="border-radius:8px;padding:8px;background:#fff";width:100%;">
    <img src="https://avatars.githubusercontent.com/u/98430977" alt="Oxjdavis" height="100" width="100" border="0" style="border-radius:50%"/>
    <br />
    <span style="height:12px;width:12px;background-color:#77e0b5;border-radius:50%;display:inline-block;"></span> <b>I'm available for new projects!</b><br />
    <a href="https://calendly.com/0xjdavis" target="_blank"><button style="background:#126ff3;color:#fff;border: 1px #126ff3 solid;border-radius:8px;padding:8px 16px;margin:10px 0">Schedule a call</button></a><br />
    </div>
    </center>
    <br />
""", unsafe_allow_html=True)

# Copyright
st.sidebar.caption("©️ Copyright 2024 J. Davis")
