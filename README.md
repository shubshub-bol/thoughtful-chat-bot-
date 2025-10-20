#  Thoughtful Chat Bot

A sleek, minimal Streamlit-based chatbot UI inspired by Google's Gemini aesthetic. This project demonstrates how to design a **modern, rounded chat interface** with a transparent search box and smooth dark gradient background.

---

##  Features

- Elegant dark gradient background(by default system theme)
- Frosted-glass style chat input box
- Rounded corners with smooth shadows
- Fully responsive on desktop and mobile(probabily not responsive)
- Minimalist layout using native Streamlit elements
- Compatible with Streamlit's chat input system

---

##  Live Demo

Try it live here \
🔗 [**Thoughtful Chat BOT - Live App**](https://thoughfulchat.streamlit.app/)


---

##  Tech Stack

- **Python 3.10+**
- **Streamlit** for UI
- **Custom HTML & CSS** for design styling

---

##  Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/shubshub-bol/thoughtful-chat-bot.git
   cd thoughtful-chat-bot
   ```

2. Install dependencies:

   ```bash
   pip install streamlit
   ```

3. Run the app:

   ```bash
   streamlit run app.py
   ```

4. Open your browser and visit:

   ```
   http://localhost:8501
   ```

---

##  Preview

| Desktop View | Mobile View |
| ------------ | ----------- |
|              |             |

---

##  File Structure

```
📦 gemini-chat-ui
 ┣ 📜 app.py              # Main Streamlit application
 ┣ 📜 requirements.txt    # Dependencies
 ┣ 📜 README.md           # Project documentation
 ┗ 📂 assets              # Screenshots & visuals
```

---

##  Customization

You can easily modify the chat box design:

- Change the gradient color in the CSS section.
- Adjust `border-radius` for different shapes.
- Modify text or placeholder styling as per your theme.

---

##  Integration with Gemini API

To integrate your UI with an actual **Gemini LLM backend**, follow these steps:

1. Install the required SDK:

   ```bash
   pip install google-generativeai
   ```

2. Add this to your code after importing Streamlit:

   ```python
   import google.generativeai as genai
   genai.configure(api_key="YOUR_API_KEY")
   model = genai.GenerativeModel("gemini-1.5-flash")

   user_query = st.chat_input("Ask Gemini")
   if user_query:
       response = model.generate_content(user_query)
       st.write(response.text)
   ```

3. Replace `YOUR_API_KEY` with your Gemini API key.

---

##  Author

**Shubham Yadav**\
[LinkedIn](https://www.linkedin.com/in/shubham-yadav-ds/)  •  [GitHub](https://github.com/shubshub-bol)

---

##  License

This project is licensed under the **MIT License** — feel free to use and modify it as you wish.

