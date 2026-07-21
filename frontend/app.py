import streamlit as st
from utils import chat_with_ai

st.set_page_config(
    page_title="HyperGPT",
    page_icon="🤖",
    layout="wide"
)

# --------------------------
# Sidebar
# --------------------------
with st.sidebar:
    st.title("⚡ HyperGPT")

    st.markdown("---")

    model = st.selectbox(
        "Choose Model",
        [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant"
        ]
    )

    temperature = st.slider(
        "Temperature",
        0.0,
        1.0,
        0.7,
        0.1
    )

    st.markdown("---")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.info(
        """
        HyperGPT

        AI Playground
        """
    )

# --------------------------
# Main Title
# --------------------------

st.title("🤖 HyperGPT")
st.caption("Your AI Assistant")

# --------------------------
# Chat History
# --------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------------
# Chat Input
# --------------------------

prompt = st.chat_input("Ask anything...")

if prompt:

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response from FastAPI
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_with_ai(prompt)
            st.markdown(response)

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )