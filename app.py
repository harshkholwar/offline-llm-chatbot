import streamlit as st
from datetime import datetime
from callollama import CALLOLLAMA

# Page config
st.set_page_config(page_title="Offline LLM Chatbot", layout="wide")

# Default Dark Mode
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True  # default ON

# Model Selection
model_options = ["phi3", "llama3", "mistral"]
if "model" not in st.session_state:
    st.session_state.model = model_options[0]  # default phi3

# Sidebar
st.sidebar.title("📦 Build Info")

# Theme Toggle
st.sidebar.markdown("### 🌙 Theme")
st.session_state.dark_mode = st.sidebar.toggle("Enable Dark Mode", value=st.session_state.dark_mode)

# Model Selector
st.sidebar.markdown("### 🤖 Choose Model")
st.session_state.model = st.sidebar.selectbox("Available Models", model_options, index=model_options.index(st.session_state.model))
#Show short description of each model
model_descriptions = {
    "phi3": "Small, fast & efficient. Best for Q&A.",
    "llama3": "Powerful general-purpose model.",
    "mistral": "Compact and strong at reasoning tasks."
}
st.sidebar.markdown(f"🧠 Model Info: {model_descriptions[st.session_state.model]}")

# ℹ️ App Info
st.sidebar.markdown(f"""
**Version:** 1.0.5  
**Model:** `{st.session_state.model}`  
**Developer:** Harsh Kholwar  

---

📍 Ask anything in the chat  
📥 Download your conversation  
🧽 Clear session anytime  
""")

# Theme Colors
if st.session_state.dark_mode:
    bg_color = "#121212"
    text_color = "#FAFAFA"
    user_bg = "#2E8B57"
    bot_bg = "#333333"
    button_color = "#00C851"
else:
    bg_color = "#f7f7f7"
    text_color = "#111111"
    user_bg = "#D1FFC6"
    bot_bg = "#F0F0F0"
    button_color = "#388E3C"

# CSS
st.markdown(f"""
    <style>
    html, body, .block-container {{
        background-color: {bg_color};
        color: {text_color};
        font-family: 'Segoe UI', sans-serif;
    }}
    .title {{
        font-size: 2.6em;
        font-weight: bold;
        color: {button_color};
        text-align: center;
        margin-top: 20px;
        margin-bottom: 0.2rem;
    }}
    .sub {{
        font-size: 1.1em;
        text-align: center;
        color: #aaa;
        margin-bottom: 25px;
    }}
    .chat-box {{
        border-radius: 10px;
        padding: 12px 18px;
        margin: 12px 0;
        max-width: 90%;
        word-wrap: break-word;
    }}
    .user-msg {{
        background-color: {user_bg};
        margin-left: auto;
        text-align: right;
    }}
    .bot-msg {{
        background-color: {bot_bg};
        margin-right: auto;
        text-align: left;
    }}
    .timestamp {{
        font-size: 0.75em;
        color: #888;
        text-align: right;
        margin-top: 4px;
    }}
    .typing {{
        font-style: italic;
        color: #888;
        animation: pulse 1s infinite;
        padding: 8px;
    }}
    @keyframes pulse {{
        0% {{opacity: 0.3;}}
        50% {{opacity: 1;}}
        100% {{opacity: 0.3;}}
    }}
    button[kind="primary"] {{
        background-color: {button_color} !important;
        color: white !important;
        border-radius: 6px !important;
        padding: 0.4rem 1.2rem !important;
        border: none !important;
    }}
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #222;
        color: white;
        text-align: center;
        padding: 10px 0;
        font-size: 0.9rem;
        z-index: 9999;
    }}
    a {{
        color: {button_color};
        text-decoration: none;
    }}
    </style>
""", unsafe_allow_html=True)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hi, I'm Harsh's chatbot. Ask me anything!",
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }]
if "is_typing" not in st.session_state:
    st.session_state.is_typing = False

# Header
st.markdown('<div class="title">🤖 Offline LLM Chatbot</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub">Model: <b>{st.session_state.model}</b> | Private & Local | Powered by Ollama</div>', unsafe_allow_html=True)

# Chat display
for msg in st.session_state.messages:
    role_class = "user-msg" if msg["role"] == "user" else "bot-msg"
    st.markdown(
        f'<div class="chat-box {role_class}">{msg["content"]}<div class="timestamp">{msg["timestamp"]}</div></div>',
        unsafe_allow_html=True
    )

# Typing status
if st.session_state.is_typing:
    st.markdown('<div class="typing">Bot is typing...</div>', unsafe_allow_html=True)

# Input form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", placeholder="Type your message here...")
    send_button = st.form_submit_button("🚀 Send")

# Buttons
col1, col2 = st.columns([1, 1])
with col1:
    clear_button = st.button("🗑️ Clear Chat")
with col2:
    download_button = st.download_button(
        label="⬇️ Download Chat",
        data="\n".join([f"{m['role'].upper()} ({m['timestamp']}): {m['content']}" for m in st.session_state.messages]),
        file_name="chat_history.txt",
        mime="text/plain"
    )

# Send logic
if send_button and user_input.strip():
    st.session_state.messages.append({
        "role": "user",
        "content": user_input.strip(),
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    st.session_state.is_typing = True
    st.rerun()

# Bot response
if st.session_state.is_typing:
    user_message = st.session_state.messages[-1]["content"]
    model = st.session_state.model
    bot_reply = CALLOLLAMA(user_message, model=model, history=st.session_state.messages)
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    st.session_state.is_typing = False
    st.rerun()

# Clear chat
if clear_button:
    st.session_state.messages = []
    st.rerun()

# Footer
st.markdown("""
    <div class="footer">
        🚀 Built by Harsh Kholwar |
        <a href="https://www.instagram.com/_harsh_k_1012_/" target="_blank">Instagram</a> |
        <a href="https://www.linkedin.com/in/harsh-kholwar-b369b2332/" target="_blank">LinkedIn</a> |
        <a href="https://api.whatsapp.com/send/?phone=7976283610" target="_blank">WhatsApp</a> |
        2025 &copy;
    </div>
""", unsafe_allow_html=True)
