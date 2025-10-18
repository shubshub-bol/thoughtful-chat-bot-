import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
import base64

# Load environment variables from a.env file at the start
load_dotenv()

# Suppress the gRPC warning which is common in some environments
os.environ = 'NONE'

def set_ui_styles(is_initial_state):
    """
    Injects CSS into the Streamlit app.
    It conditionally applies styles for the initial centered view vs. the active chat view.
    """
    # LinkedIn logo SVG from Bootstrap Icons (MIT License)
    # Source: https://icons.getbootstrap.com/icons/linkedin/
    linkedin_svg_path = """
    M0 1.146C0.513.526 0 1.175 0h13.65C15.474 0 16.513 16 1.146v13.708c0.633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854zm4.943 12.248V6.169H2.542v7.225zm-1.2-8.212c.837 0 1.518-.681 1.518-1.518S4.58 3.65 3.743 3.65s-1.518.68-1.518 1.518.681 1.518 1.518 1.518zm1.2 8.212h3.553V9.25c0-.926.016-2.116 1.29-2.116 1.291 0 1.488 1.003 1.488 2.049v4.468h3.554V9.019c0-3.22-1.714-5.025-4.287-5.025-2.049 0-3.134 1.084-3.658 2.115h.055V6.169H4.943z
    """
    # To prevent issues with CSS parsing, it's safer to encode the SVG for use in an anchor tag
    # However, for direct embedding in HTML, it's fine. Here we will use a data URI for robustness in CSS if needed,
    # but for the HTML part, we'll embed it directly.
    
    # Base64 encode the SVG to create a data URI for the logo
    # This makes the app self-contained and avoids extra file requests.
    encoded_svg = base64.b64encode(linkedin_svg_path.encode("utf-8")).decode("utf-8")
    
    # Conditional CSS for the chat input position
    # If it's the initial state, we center the input box. Otherwise, it stays at the bottom.
    conditional_input_style = ""
    if is_initial_state:
        conditional_input_style = """
        /* Center the input box in the initial view */
        {
            position: absolute;
            bottom: 50%;
            left: 50%;
            transform: translate(-50%, 90%); /* Adjust vertical alignment */
            width: 80%!important;
            max-width: 740px!important;
        }
        """
    
    # The main CSS block for the application
    page_styles = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    /* --- KEYFRAMES FOR ANIMATIONS --- */
    @keyframes morph {{
        0% {{ border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; transform: rotate(0deg) scale(1.2); }}
        50% {{ border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%; transform: rotate(180deg) scale(1.1); }}
        100% {{ border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; transform: rotate(360deg) scale(1.2); }}
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(15px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* --- GLOBAL & LAYOUT STYLES --- */
    body {{
        font-family: 'Poppins', sans-serif;
    }}

    /* Main app container styling - Flexbox layout for scrolling */
    [data-testid="stAppViewContainer"] {{
        background-color: #111827;
        position: relative;
        overflow: hidden; /* Keep this for the blob effect, but manage children overflow */
        color: #e0e0e0;
        display: flex;
        flex-direction: column;
        height: 100vh;
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
    
    /* Ensure content is above the background animation */
   ,.main {{
        z-index: 1;
        position: relative;
    }}
    
    /* This targets the main content area and makes it scrollable */
    [data-testid="stAppViewContainer"] > section > div > div > div > div:nth-child(1) {{
        flex-grow: 1;
        overflow-y: auto; /* THIS IS THE KEY FIX FOR SCROLLING */
        padding-right: 15px; /* Add some padding to avoid scrollbar overlap */
    }}

    /* Hide the default Streamlit header */
    [data-testid="stHeader"] {{
        background-color: rgba(0, 0, 0, 0);
        z-index: 10;
    }}

    /* Style the bottom section containing the chat input */
    section {{
        background-color: transparent!important;
        border: none!important;
        padding-bottom: 15px!important;
        padding-top: 10px!important;
        z-index: 10;
        width: 100%;
    }}

    /* --- INITIAL VIEW STYLES (NO MESSAGES) --- */
   .initial-view-container {{
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 80vh;
        text-align: center;
    }}
    
   .hello-text {{
        font-family: 'Poppins', sans-serif!important;
        font-size: 4.0em!important;
        font-weight: 600!important;
        color: #f0f0f0!important;
        letter-spacing: -2px!important;
        animation: fadeIn 1s ease-out;
    }}

    /* --- CHAT INPUT STYLES --- */
    [data-testid="stChatInput"] {{
        background-color: rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(12px);
        border-radius: 9999px; /* Perfect pill shape */
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
        padding: 5px 5px 5px 15px;
    }}

    [data-testid="stChatInput"]:focus-within {{
        border-color: rgba(173, 216, 230, 0.7);
        box-shadow: 0 0 10px rgba(173, 216, 230, 0.3);
    }}
    
    [data-testid="stChatInput"] textarea {{
        background-color: transparent;
        color: #e0e0e0;
        font-family: 'Poppins', sans-serif;
    }}

    [data-testid="stChatInput"] textarea::placeholder {{
        color: rgba(255, 255, 255, 0.6);
        font-family: 'Poppins', sans-serif;
    }}

    [data-testid="stChatInput"] button {{
        background-color: #333;
        border: none;
        border-radius: 50%;
        width: 38px;
        height: 38px;
        display: flex;
        justify-content: center;
        align-items: center;
        transition: background-color 0.3s ease;
        margin: 0;
    }}

    [data-testid="stChatInput"] button:hover {{
        background-color: #444;
    }}

    [data-testid="stChatInput"] button svg {{
        display: none; /* Hide default SVG */
    }}

    [data-testid="stChatInput"] button::after {{
        content: '➤';
        font-size: 18px;
        color: white;
        line-height: 1;
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
        width: fit-content;
        max-width: 85%;
    }}

    /* --- HEADER MARK STYLES --- */
   .header-mark {{
        position: fixed;
        top: 20px;
        left: 25px;
        z-index: 100;
    }}

   .header-mark a {{
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.9em;
        font-weight: 400;
        color: rgba(255, 255, 255, 0.7);
        text-decoration: none;
        transition: color 0.3s ease;
    }}

   .header-mark a:hover {{
        color: rgba(255, 255, 255, 1.0);
    }}

   .header-mark svg {{
        width: 16px;
        height: 16px;
        fill: currentColor; /* The SVG color will match the text color */
    }}

    /* Apply the conditional style for the input box */
    {conditional_input_style}

    </style>
    """
    
    # HTML for the header mark
    header_html = f"""
    <div class="header-mark">
        <a href="https://www.linkedin.com/in/shubham-yadav-ds/" target="_blank" rel="noopener noreferrer">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-linkedin" viewBox="0 0 16 16">
                <path d="{linkedin_svg_path}"/>
            </svg>
            <span>Developed by Shubham Yadav</span>
        </a>
    </div>
    """
    
    st.markdown(page_styles, unsafe_allow_html=True)
    st.markdown(header_html, unsafe_allow_html=True)

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

    # --- Session State Initialization ---
    if "messages" not in st.session_state:
        st.session_state.messages =

    # --- UI Styling ---
    # The key change: pass the state to the styling function
    set_ui_styles(is_initial_state=(not st.session_state.messages))

    # --- AVATAR ICONS (using Base64 for self-containment) ---
    USER_AVATAR = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgZmlsbD0iI2YwZjBmMCIgdmlld0JveD0iMCAwIDI1NiAyNTYiPjxwYXRoIGQ9Ik0yMzAuOTIsMjEyYy0xNS4yMy0yNi4zMy0zOC43LTQ1LjIxLTY2LjA5LTU0LjE2YTcyLDcyLDAsMSwwLTczLjY2LDBDNjMuNzgsMTY2Ljc4LDQwLjMxLDE4NS42NiwyNS4wOCwyMTJhOCw4LDAsMSwwLDEzLjg0LDhjMTguODQtMzIuNTYsNTIuMTQtNTIsODkuMDgtNTJzNzAuMjQsMTkuNDQsODkuMDgsNTJhOCw4LDAsMSwwLDEzLjg0LThaIj48L3BhdGg+PC9zdmc+"
    ASSISTANT_AVATAR = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgZmlsbD0iI2YwZjBmMCIgdmlld0JveD0iMCAwIDI1NiAyNTYiPjxwYXRoIGQ9Ik0yMDgsMzJINDhBMTYsMTYsMCwwLDAsMzIsNDhWMTc2YTE2LDE2LDAsMCwwLDE2LDE2SDY0djI0YTgsOCwwLDAsMCwxNiwwVjE5Mmg5NnYyNGE4LDgsMCwwLDAsMTYsMFYxOTJoMTZhMTYsMTYsMCwwLDAsMTYtMTZWNDhBMTYsMTYsMCwwLDAsMjA4LDMyWk05NiwxNDRhMTYsMTYsMCwxLDEsMTYtMTZBMTYsMTYsMCwwLDEsOTYsMTQ0Wm02NCwwYTE2LDE2LDAsMSwxLDE2LTE2QTE2LDE2LDAsMCwxLDE2MCwxNDRaIj48L3BhdGg+PC9zdmc+"

    # --- Model Initialization ---
    try:
        model = ChatGoogleGenerativeAI(model='gemini-1.5-flash', stream=True)
    except Exception as e:
        st.error("Failed to initialize the Gemini model. Please check your API key.")
        st.error(f"Error details: {e}")
        return

    # --- UI Logic ---
    # Show the initial centered greeting if there are no messages
    if not st.session_state.messages:
        st.markdown("""
            <div class="initial-view-container">
                <p class="hello-text">Hello there!</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Display the entire chat history from session state
    for message in st.session_state.messages:
        avatar = USER_AVATAR if message["role"] == "user" else ASSISTANT_AVATAR
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # --- Unified Chat Input and Response Logic ---
    if prompt := st.chat_input("Ask Gemini...", key="main_chat_input"):
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Immediately re-run the script to update the UI.
        # This removes the initial view and moves the input to the bottom.
        st.rerun()

    # The logic to generate a response only runs if the last message was from the user
    # and we need to generate a new assistant response.
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
            try:
                # Prepare history for the model
                history = st.session_state.messages
                langchain_messages = [
                    HumanMessage(content=msg["content"]) if msg["role"] == "user" 
                    else AIMessage(content=msg["content"]) 
                    for msg in history
                ]
                
                def stream_response():
                    for chunk in model.stream(langchain_messages):
                        yield chunk.content
                
                full_response = st.write_stream(stream_response)
                
                # Add the complete AI response to session state for history
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                st.error(f"An error occurred while getting the response: {e}")

if __name__ == "__main__":
    if os.getenv("GOOGLE_API_KEY") is None:
        st.error("GOOGLE_API_KEY environment variable not found.")
        st.info("Please create a `.env` file and add your key: `GOOGLE_API_KEY='your-api-key-here'`")
    else:
        main()
