import os
import time
import uuid
import streamlit as st

from utils.api import chat_with_ai, stream_text
from utils.storage import (
    get_chat_files,
    create_chat,
    load_chat,
    save_chat,
    delete_chat,
    rename_chat,
)

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="HyperGPT",
    page_icon="🤖",
    layout="wide",
)

# -----------------------------
# Load CSS
# -----------------------------
css_file = "assets/style.css"

if os.path.exists(css_file):
    with open(css_file, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -----------------------------
# Session State
# -----------------------------
if "current_chat" not in st.session_state:
    st.session_state.current_chat = create_chat()

if "messages" not in st.session_state:
    st.session_state.messages = load_chat(st.session_state.current_chat)

if "last_response_time" not in st.session_state:
    st.session_state.last_response_time = 0

if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.title("⚡ HyperGPT")
    st.markdown("---")

    AVAILABLE_MODELS = {
        "Llama 3.3 70B (Groq)": "llama-3.3-70b-versatile",
        "Llama 3.1 8B Instant (Groq)": "llama-3.1-8b-instant",
    }

    selected_model = st.selectbox(
        "Choose AI Model",
        list(AVAILABLE_MODELS.keys())
    )

    model = AVAILABLE_MODELS[selected_model]

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
    )

    st.markdown("---")

    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.current_chat = create_chat()
        st.session_state.messages = []
        st.rerun()

    st.subheader("💬 Chat History")

    chats = get_chat_files()

    if chats:
        for chat in chats:
            col1, col2 = st.columns([5, 1])

            with col1:
                if st.button(
                    chat.replace(".json", ""),
                    key=f"chat_{chat}",
                    use_container_width=True,
                ):
                    st.session_state.current_chat = chat
                    st.session_state.messages = load_chat(chat)
                    st.rerun()

            with col2:
                if st.button("❌", key=f"del_{chat}"):
                    delete_chat(chat)
                    st.rerun()
    else:
        st.info("No chats found.")

    st.markdown("---")

    if st.button("🧹 Clear Messages", use_container_width=True):
        st.session_state.messages = []
        save_chat(st.session_state.current_chat, [])
        st.rerun()

    st.markdown("---")

    new_name = st.text_input(
        "Rename Current Chat",
        placeholder="My AI Project",
    )

    if st.button("✏ Rename Chat", use_container_width=True):
        if new_name.strip():
            st.session_state.current_chat = rename_chat(
                st.session_state.current_chat,
                new_name.strip(),
            )
            st.rerun()

    if st.button("🗑 Delete Current Chat", use_container_width=True):

        delete_chat(st.session_state.current_chat)

        chats = get_chat_files()

        if chats:
            st.session_state.current_chat = chats[0]
            st.session_state.messages = load_chat(chats[0])
        else:
            st.session_state.current_chat = create_chat()
            st.session_state.messages = []

        st.rerun()

    st.markdown("---")

    st.success("🟢 AI Online")

    st.metric(
        "Current Chat",
        st.session_state.current_chat.replace(".json", ""),
    )

    st.metric(
        "Messages",
        len(st.session_state.messages),
    )

    st.metric(
        "Model",
        model,
    )

    st.metric(
        "Temperature",
        temperature,
    )

    st.metric(
        "Last Response",
        f"{st.session_state.last_response_time}s",
    )

# -----------------------------
# Main Page
# -----------------------------
st.title("🤖 HyperGPT")

st.markdown(
    """
### Your Intelligent AI Workspace

Ask questions, generate ideas, write code, and chat with your AI assistant.
"""
)

st.divider()

# -----------------------------
# Display Messages
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Chat Input
# -----------------------------
prompt = st.chat_input("💬 Ask HyperGPT anything...")

if prompt:

    st.session_state.last_prompt = prompt

    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    save_chat(
        st.session_state.current_chat,
        st.session_state.messages,
    )

    with st.chat_message("assistant"):

        start_time = time.time()

        with st.spinner("Thinking..."):

            response = chat_with_ai(
                message=prompt,
                chat_id=st.session_state.current_chat.replace(".json", ""),
                model=model,
            )

        response_time = round(time.time() - start_time, 2)

        st.session_state.last_response_time = response_time

        placeholder = st.empty()
        streamed = ""

        for chunk in stream_text(response):
            streamed += chunk
            placeholder.markdown(streamed)

        st.caption(
            f"⚡ Response generated in {response_time} seconds"
        )

        with st.expander("View Raw Response"):
            st.code(response, language="text")

        if st.button("🔄 Regenerate Response"):

            new_response = chat_with_ai(
                message=st.session_state.last_prompt,
                chat_id=st.session_state.current_chat.replace(".json", ""),
                model=model,
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": new_response,
                }
            )

            save_chat(
                st.session_state.current_chat,
                st.session_state.messages,
            )

            st.rerun()

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )

    save_chat(
        st.session_state.current_chat,
        st.session_state.messages,
    )

    st.rerun()