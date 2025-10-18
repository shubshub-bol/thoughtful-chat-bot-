import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
import time

# Load environment variables from a .env file at the start
load_dotenv()

# Suppress the gRPC warning
os.environ['GRPC_VERBOSITY'] = 'NONE'

def set_gemini_background():
    """
    Sets a "liquid glass" themed animated background and UI styles for the Streamlit app.
    This version fixes scrolling, input box positioning, and adds a clickable header.
    """
    # LinkedIn SVG Icon - corrected and styled
    linkedin_svg = """
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor" class="linkedin-icon">
      <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
    </svg>
    """

    page_bg_img = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    @keyframes morph {{
        0% {{ border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; transform: rotate(0deg) scale(1.2); }}
        50% {{ border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%; transform: rotate(180deg) scale(1.1); }}
        100% {{ border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; transform: rotate(360deg) scale(1.2); }}
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(15px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Main app container styling */
    [data-testid="stAppViewContainer"] {{
        background-color: #111827;
        position: relative;
        overflow: hidden; /* Keep hidden for blob animation */
        color: #e0e0e0;
        font-family: 'Poppins', sans-serif;
    }}

    /* Pseudo-element for the animated blob */
    [data-testid="stAppViewContainer"]::before {{
        content: '';
        position: absolute;
        top: 20%; left: 25%;
        width: 50%; height: 60%;
        background: linear-gradient(135deg, rgba(76, 0, 255, 0.5), rgba(0, 191, 255, 0.5));
        animation: morph 15s ease-in-out infinite;
        filter: blur(80px);
        z-index: 0;
    }}
    
    /* Make all content relative to stay on top of the background */
    .stApp > div {{
        z-index: 1;
        position: relative;
    }}
    
    /* Hide the default Streamlit header */
    [data-testid="stHeader"] {{
        background-color: rgba(0, 0, 0, 0);
        z-index: 101;
    }}

    /* --- CHAT INPUT STICKY FIX --- */
    /* This ensures the input bar is always at the bottom */
    section[data-testid="stBottom"] {{
        background-color: transparent !important;
        border: none !important;
        padding: 0 1rem 1rem 1rem;
        z-index: 2;
    }}

    /* Style the pill-shaped chat input box */
    [data-testid="stChatInput"] {{
        background-color: rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(12px);
        border-radius: 50px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }}
    [data-testid="stChatInput"]:focus-within {{
        border-color: rgba(173, 216, 230, 0.7);
        box-shadow: 0 0 10px rgba(173, 216, 230, 0.3);
    }}
    [data-testid="stChatInput"] textarea::placeholder {{
        color: rgba(255, 255, 255, 0.6);
        font-family: 'Poppins', sans-serif;
    }}
    [data-testid="stChatInput"] button {{
        background-color: #333; border: none; border-radius: 50%;
        width: 36px; height: 36px; display: flex;
        justify-content: center; align-items: center;
        transition: background-color 0.3s ease; margin: 5px;
    }}
    [data-testid="stChatInput"] button:hover {{ background-color: #444; }}
    [data-testid="stChatInput"] button svg {{ display: none; }}
    [data-testid="stChatInput"] button::after {{
        content: '➤'; font-size: 18px; color: white;
        transform: rotate(0deg); line-height: 1;
    }}
    
    /* --- CHAT MESSAGE STYLES --- */
    [data-testid="stChatMessage"] {{
        background-color: rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        animation: fadeIn 0.5s ease-out;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }}

    /* --- INITIAL VIEW STYLING --- */
    .initial-view-container {{
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        /* Use viewport height minus an approximation for the input bar */
        height: calc(100vh - 100px);
    }}
    
    .hello-text {{
        font-family: 'Poppins', sans-serif !important;
        font-size: 3.5em !important;
        font-weight: 600 !important;
        color: #f0f0f0 !important;
        padding-bottom: 20px !important;
        letter-spacing: -2px !important;
    }}
    
    /* --- HEADER MARK WITH CLICKABLE LOGO --- */
    .header-mark {{
        position: fixed;
        top: 25px; left: 30px;
        display: flex; align-items: center; gap: 10px;
        font-size: 0.9em; font-weight: 400;
        color: rgba(255, 255, 255, 0.7);
        z-index: 100;
    }}
    .header-mark a {{
        display: inline-block; line-height: 0;
        transition: transform 0.2s ease-in-out;
    }}
    .header-mark a:hover {{ transform: scale(1.1); }}
    .linkedin-icon {{
        width: 20px; height: 20px;
        color: rgba(255, 255, 255, 0.7);
    }}
    .linkedin-icon:hover {{ color: rgba(255, 255, 255, 1.0); }}
    </style>
    
    <div class="header-mark">
        <span>Developed by Shubham Yadav</span>
        <a href="https://www.linkedin.com/in/shubham-yadav-ds/" target="_blank" rel="noopener noreferrer">
            {linkedin_svg}
        </a>
    </div>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

def main():
    """
    This function runs the Streamlit chatbot application.
    """
    st.set_page_config(page_title="Gemini Chatbot", page_icon="✨", layout="centered")
    set_gemini_background()

    USER_AVATAR = "https://i.ibb.co/Xz6C7V6/user-avatar.png"
    ASSISTANT_AVATAR = "https://i.ibb.co/1npG22W/gemini-avatar.png"

    try:
        model = ChatGoogleGenerativeAI(model='models/gemini-1.5-flash', stream=True)
    except Exception as e:
        st.error("Failed to initialize the Gemini model. Please check your API key.")
        st.error(f"Error details: {e}")
        return

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display initial message if the chat is empty
    if not st.session_state.messages:
        st.markdown("""
            <div class="initial-view-container">
                <p class="hello-text">Hello there!</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Display the entire chat history
        for message in st.session_state.messages:
            avatar = USER_AVATAR if message["role"] == "user" else ASSISTANT_AVATAR
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    # Main chat input and response logic
    if prompt := st.chat_input("Ask Gemini", key="main_chat_input"):
        # Add user message to state and display it immediately
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display the user's message
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(prompt)

        # Generate and stream AI response
        with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
            try:
                # Prepare history for the model
                history = st.session_state.messages[-10:]
                langchain_messages = [
                    HumanMessage(content=msg["content"]) if msg["role"] == "user"
                    else AIMessage(content=msg["content"])
                    for msg in history
                ]
                config = {"generation_config": {"response_mime_type": "text/plain"}}

                # Define the streaming function
                def stream_response():
                    for chunk in model.stream(langchain_messages, config=config):
                        yield chunk.content
                
                # Use write_stream to display the response and capture the full text
                full_response = st.write_stream(stream_response)
                
                # Add the complete AI response to session state for history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
                # A small delay and rerun can help ensure the layout updates correctly
                # after the first message is sent, transitioning from the initial view.
                if len(st.session_state.messages) == 2: # Only rerun after the very first exchange
                    time.sleep(0.1)
                    st.rerun()

            except Exception as e:
                st.error(f"An error occurred while getting the response: {e}")

if __name__ == "__main__":
    if os.getenv("GOOGLE_API_KEY") is None:
        st.error("GOOGLE_API_KEY environment variable not found.")
        st.info("Please create a `.env` file and add your key: `GOOGLE_API_KEY='your-api-key-here'`")
    else:
        main()

