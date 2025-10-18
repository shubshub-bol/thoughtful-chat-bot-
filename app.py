import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

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
        from {{
            opacity: 0;
            transform: translateY(15px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    /* Main app container styling */
    [data-testid="stAppViewContainer"] {{
        background-color: #111827; /* Dark gray base */
        position: relative;
        color: #e0e0e0;
        font-family: 'Poppins', sans-serif;
        /* CRITICAL FIX: Ensure the container itself doesn't hide overflow */
        overflow: hidden; 
    }}

    /* Pseudo-element for the animated blob */
    [data-testid="stAppViewContainer"]::before {{
        content: '';
        position: absolute;
        top: 20%;
        left: 25%;
        width: 50%;
        height: 60%;
        background: linear-gradient(135deg, rgba(76, 0, 255, 0.5), rgba(0, 191, 255, 0.5));
        animation: morph 15s ease-in-out infinite;
        filter: blur(80px);
        z-index: 0;
    }}
    
    /* Ensure all content is above the background animation */
    /* Use a class for the main layout to avoid affecting other elements */
    .main-content-wrapper {{
        position: relative;
        z-index: 1;
        display: flex;
        flex-direction: column;
        height: 100vh; /* Make the wrapper take full viewport height */
    }}
    
    /* Hide the default Streamlit header */
    [data-testid="stHeader"] {{
        background-color: rgba(0, 0, 0, 0);
        z-index: 101; /* Ensure header is above content */
    }}

    /* --- CHAT AREA SCROLLING FIX --- */
    /* Target the container that holds the chat messages */
    .st-emotion-cache-1jicfl2 {{
        flex-grow: 1; /* Allow this container to grow and fill available space */
        overflow-y: auto; /* Enable vertical scrolling for the chat area */
        padding-bottom: 20px; /* Add some space at the bottom */
    }}

    /* Custom scrollbar for a cleaner look */
    .st-emotion-cache-1jicfl2::-webkit-scrollbar {{
        width: 6px;
    }}
    .st-emotion-cache-1jicfl2::-webkit-scrollbar-track {{
        background: rgba(0,0,0,0.1);
        border-radius: 10px;
    }}
    .st-emotion-cache-1jicfl2::-webkit-scrollbar-thumb {{
        background: rgba(255,255,255,0.2);
        border-radius: 10px;
    }}
    .st-emotion-cache-1jicfl2::-webkit-scrollbar-thumb:hover {{
        background: rgba(255,255,255,0.3);
    }}

    /* --- CHAT INPUT STYLES --- */
    /* This section remains largely the same, but it will now be correctly positioned at the bottom */
    section[data-testid="stBottom"] {{
        background-color: transparent !important;
        border: none !important;
        padding: 0 1rem 1rem 1rem; /* Adjust padding */
        z-index: 2; /* Keep input on top */
    }}

    /* Style the pill-shaped chat input box */
    [data-testid="stChatInput"] {{
        background-color: rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(12px);
        border-radius: 50px; /* Pill shape */
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
        justify-content: center; /* Center vertically in its container */
        align-items: center;
        flex-grow: 1; /* Allow it to take up all available space */
        text-align: center;
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
        top: 25px;
        left: 30px;
        display: flex;
        align-items: center;
        gap: 10px; /* Space between name and icon */
        font-size: 0.9em;
        font-weight: 400;
        color: rgba(255, 255, 255, 0.7);
        z-index: 100;
    }}
    .header-mark a {{
        display: inline-block;
        line-height: 0; /* Align icon properly */
        transition: transform 0.2s ease-in-out;
    }}
    .header-mark a:hover {{
        transform: scale(1.1);
    }}
    .linkedin-icon {{
        width: 20px;
        height: 20px;
        color: rgba(255, 255, 255, 0.7);
    }}
    .linkedin-icon:hover {{
        color: rgba(255, 255, 255, 1.0);
    }}
    </style>
    
    <!-- Header Mark HTML with clickable link -->
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
    # --- Page Configuration ---
    st.set_page_config(
        page_title="Gemini Chatbot",
        page_icon="✨",
        layout="centered"
    )

    set_gemini_background()

    # --- AVATAR ICONS ---
    USER_AVATAR = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgZmlsbD0iI2YwZjBmMCIgdmlld0JveD0iMCAwIDI1NiAyNTYiPjxwYXRoIGQ9Ik0yMzAuOTIsMjEyYy0xNS4yMy0yNi4zMy0zOC43LTQ1LjIxLTY2LjA5LTU0LjE2YTcyLDcyLDAsMSwwLTczLjY2LDBDNjMuNzgsMTY2Ljc4LDQwLjMxLDE4NS42NiwyNS4wOCwyMTJhOCw4LDAsMSwwLDEzLjg0LDhjMTguODQtMzIuNTYsNTIuMTQtNTIsODkuMDgtNTJzNzAuMjQsMTkuNDQsODkuMDgsNTJhOCw4LDAsMSwwLDEzLjg0LThaIj48L3BhdGg+PC9zdmc+"
    ASSISTANT_AVATAR = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgZmlsbD0iI2YwZjBmMCIgdmlld0JveD0iMCAwIDI1NiAyNTYiPjxwYXRoIGQ9Ik0yMDgsMzJINDhBMTYsMTYsMCwwLDAsMzIsNDhWMTc2YTE2LDE2LDAsMCwwLDE2LDE2SDY0djI0YTgsOCwwLDAsMCwxNiwwVjE5Mmg5NnYyNGE4LDgsMCwwLDAsMTYsMFYxOTJoMTZhMTYsMTYsMCwwLDAsMTYtMTZWNDhBMTYsMTYsMCwwLDAsMjA4LDMyWk05NiwxNDRhMTYsMTYsMCwxLDEsMTYtMTZBMTYsMTYsMCwwLDEsOTYsMTQ0Wm02NCwwYTE2LDE2LDAsMSwxLDE2LTE2QTE2LDE2LDAsMCwxLDE2MCwxNDRaIj48L3BhdGg+PC9zdmc+"

    # --- Model Initialization ---
    try:
        model = ChatGoogleGenerativeAI(model='models/gemini-1.5-flash', stream=True)
    except Exception as e:
        st.error(f"Failed to initialize the Gemini model. Please check your API key.")
        st.error(f"Error details: {e}")
        return

    # --- Session State for Chat History ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # --- UI LAYOUT ---
    # Apply a wrapper div to control the main layout with flexbox
    st.markdown('<div class="main-content-wrapper">', unsafe_allow_html=True)

    # Use a container for the chat history to enable scrolling
    chat_container = st.container()

    with chat_container:
        # Show the initial centered greeting if there are no messages
        if not st.session_state.messages:
            st.markdown("""
                <div class="initial-view-container">
                    <p class="hello-text">Hello there!</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Display the entire chat history from session state
            for message in st.session_state.messages:
                avatar = USER_AVATAR if message["role"] == "user" else ASSISTANT_AVATAR
                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])

    # --- UNIFIED CHAT INPUT AND RESPONSE LOGIC ---
    if prompt := st.chat_input("Ask Gemini", key="main_chat_input"):
        # Add user message to session state and display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display the new user message inside the chat container
        with chat_container:
            with st.chat_message("user", avatar=USER_AVATAR):
                st.markdown(prompt)

        # Generate and stream AI response
        with chat_container:
            with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
                try:
                    history = st.session_state.messages[-10:]
                    langchain_messages = [
                        HumanMessage(content=msg["content"]) if msg["role"] == "user" 
                        else AIMessage(content=msg["content"]) 
                        for msg in history
                    ]
                    config = {"generation_config": {"response_mime_type": "text/plain"}}
                    
                    def stream_response():
                        for chunk in model.stream(langchain_messages, config=config):
                            yield chunk.content
                    
                    full_response = st.write_stream(stream_response)
                    
                    # Add the complete AI response to session state for history
                    st.session_state.messages.append({"role": "assistant", "content": full_response})

                except Exception as e:
                    st.error(f"An error occurred while getting the response: {e}")
        
        # Rerun to clear the "Hello there!" and display the full chat
        st.rerun()

    # Close the wrapper div
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    if os.getenv("GOOGLE_API_KEY") is None:
        st.error("GOOGLE_API_KEY environment variable not found.")
        st.info("Please create a `.env` file and add your key: `GOOGLE_API_KEY='your-api-key-here'`")
    else:
        main()
