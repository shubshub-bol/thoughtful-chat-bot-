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
        overflow: hidden;
        color: #e0e0e0;
        font-family: 'Poppins', sans-serif; /* Apply Poppins to the whole app */
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
        filter: blur(80px); /* Increased blur for a softer look */
        z-index: 0;
    }}
    
    /* Ensure content is above the background animation */
    [data-testid="stVerticalBlock"] {{
        z-index: 1;
        position: relative;
    }}
    
    /* Hide the default Streamlit header */
    [data-testid="stHeader"] {{
        background-color: rgba(0, 0, 0, 0);
    }}

    /* --- DEFINITIVE FIX FOR BLACK BAR --- */
    div[data-testid="stBottom"] {{
        background-color: transparent !important;
        border: none !important;
        padding-bottom: 20px !important; /* Lifts the input box */
    }}
    /* --- END FIX --- */

    /* --- INPUT STYLES START --- */
    
    /* Style the main chat input box (at the bottom) */
    [data-testid="stChatInput"] {{
        background-color: rgba(0, 0, 0, 0.2); /* More transparent */
        backdrop-filter: blur(12px);
        border-radius: 50px; /* Pill shape */
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }}

    /* Add a glow effect when the chat input is focused */
    [data-testid="stChatInput"]:focus-within {{
        border-color: rgba(173, 216, 230, 0.7); /* Light blue glow */
        box-shadow: 0 0 10px rgba(173, 216, 230, 0.3);
    }}
    
    /* Styling for the placeholder text in the main chat input */
    [data-testid="stChatInput"] textarea::placeholder {{
        color: rgba(255, 255, 255, 0.6);
        font-family: 'Poppins', sans-serif;
    }}

    /* --- NEW SEND BUTTON STYLES --- */
    [data-testid="stChatInput"] button {{
        background-color: #333;
        border: none;
        border-radius: 50%;
        width: 36px;
        height: 36px;
        display: flex;
        justify-content: center;
        align-items: center;
        transition: background-color 0.3s ease;
        margin: 5px;
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
        transform: rotate(0deg);
        line-height: 1;
    }}
    
    /* --- INPUT STYLES END --- */


    /* Style the chat messages with animation */
    [data-testid="stChatMessage"] {{
        background-color: rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        animation: fadeIn 0.5s ease-out; /* Apply the fade-in animation */
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2); /* Add a subtle shadow for depth */
    }}

    /* Centered container for the initial 'Hello' message */
    .initial-view-container {{
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 80vh; /* Make it take up more vertical space */
    }}
    
    /* --- UPDATED HELLO TEXT STYLE --- */
    .hello-text {{
        font-family: 'Poppins', sans-serif !important;
        font-size: 4.0em !important; /* Reduced size */
        font-weight: 600 !important; /* Bolder */
        color: #f0f0f0 !important;
        padding-bottom: 20px !important;
        letter-spacing: -2px !important; /* Tighter spacing */
    }}
    
    </style>
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
        model = ChatGoogleGenerativeAI(model='models/gemini-2.5-flash', stream=True)
    except Exception as e:
        st.error(f"Failed to initialize the Gemini model. Please check your API key.")
        st.error(f"Error details: {e}")
        return

    # --- Session State for Chat History ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

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
    if prompt := st.chat_input("Ask Gemini", key="main_chat_input"):
        # Add user message to session state and display it immediately
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(prompt)

        # Generate and stream AI response
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


if __name__ == "__main__":
    if os.getenv("GOOGLE_API_KEY") is None:
        st.error("GOOGLE_API_KEY environment variable not found.")
        st.info("Please create a `.env` file and add your key: `GOOGLE_API_KEY='your-api-key-here'`")
    else:
        main()

