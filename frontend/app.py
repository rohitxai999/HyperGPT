import os
import time
import streamlit as st

from utils.api import (
    chat_with_ai,
    stream_text,
    register_user,
    login_user,
    get_current_user,
    logout_user,
)

from utils.storage import (
    get_chat_files,
    create_chat,
    load_chat,
    save_chat,
    delete_chat,
    rename_chat,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="HyperGPT",
    page_icon="🤖",
    layout="wide",
)


# ============================================================
# LOAD CSS
# ============================================================

css_file = "assets/style.css"

if os.path.exists(css_file):
    with open(css_file, "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )


# ============================================================
# SESSION STATE
# ============================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "access_token" not in st.session_state:
    st.session_state.access_token = None

if "user" not in st.session_state:
    st.session_state.user = None

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_response_time" not in st.session_state:
    st.session_state.last_response_time = 0

if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""


# ============================================================
# AUTHENTICATION PAGE
# ============================================================

if not st.session_state.authenticated:

    st.title("🤖 HyperGPT")

    st.subheader("Your Intelligent AI Workspace")

    st.write(
        "Sign in to access your personalized HyperGPT workspace."
    )

    st.divider()

    login_tab, register_tab = st.tabs(
        ["🔐 Login", "📝 Register"]
    )

    # --------------------------------------------------------
    # LOGIN
    # --------------------------------------------------------

    with login_tab:

        st.header("Welcome Back")

        login_email = st.text_input(
            "Email",
            key="login_email",
            placeholder="you@example.com",
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password",
            placeholder="Enter your password",
        )

        if st.button(
            "🔐 Login",
            use_container_width=True,
            type="primary",
        ):

            if not login_email.strip():
                st.error("Please enter your email.")

            elif not login_password:
                st.error("Please enter your password.")

            else:

                with st.spinner("Signing you in..."):

                    result = login_user(
                        email=login_email.strip(),
                        password=login_password,
                    )

                if result["success"]:

                    token = result["access_token"]

                    user_result = get_current_user(
                        token
                    )

                    if user_result["success"]:

                        st.session_state.access_token = token

                        st.session_state.user = (
                            user_result["data"]
                        )

                        st.session_state.authenticated = True

                        st.session_state.current_chat = (
                            create_chat()
                        )

                        st.session_state.messages = []

                        st.success(
                            "Login successful!"
                        )

                        st.rerun()

                    else:

                        st.error(
                            user_result["error"]
                        )

                else:

                    st.error(
                        result["error"]
                    )

    # --------------------------------------------------------
    # REGISTER
    # --------------------------------------------------------

    with register_tab:

        st.header("Create Your HyperGPT Account")

        register_email = st.text_input(
            "Email",
            key="register_email",
            placeholder="you@example.com",
        )

        register_username = st.text_input(
            "Username",
            key="register_username",
            placeholder="Choose a username",
        )

        register_password = st.text_input(
            "Password",
            type="password",
            key="register_password",
            placeholder="Create a strong password",
        )

        register_confirm = st.text_input(
            "Confirm Password",
            type="password",
            key="register_confirm",
            placeholder="Re-enter your password",
        )

        if st.button(
            "📝 Create Account",
            use_container_width=True,
            type="primary",
        ):

            if not register_email.strip():

                st.error(
                    "Please enter your email."
                )

            elif not register_username.strip():

                st.error(
                    "Please enter a username."
                )

            elif not register_password:

                st.error(
                    "Please enter a password."
                )

            elif register_password != register_confirm:

                st.error(
                    "Passwords do not match."
                )

            else:

                with st.spinner(
                    "Creating your account..."
                ):

                    result = register_user(
                        email=register_email.strip(),
                        username=register_username.strip(),
                        password=register_password,
                    )

                if result["success"]:

                    st.success(
                        "Account created successfully! "
                        "You can now login."
                    )

                else:

                    st.error(
                        result["error"]
                    )

    st.stop()


# ============================================================
# AUTHENTICATED USER
# ============================================================

user = st.session_state.user

if user is None:

    st.session_state.authenticated = False

    st.rerun()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("⚡ HyperGPT")

    st.markdown("---")

    st.success("🟢 AI Online")

    st.markdown(
        f"### 👤 {user.get('username', 'User')}"
    )

    st.caption(
        user.get(
            "email",
            "",
        )
    )

    st.markdown("---")

    AVAILABLE_MODELS = {
        "Llama 3.3 70B (Groq)": (
            "llama-3.3-70b-versatile"
        ),
        "Llama 3.1 8B Instant (Groq)": (
            "llama-3.1-8b-instant"
        ),
    }

    selected_model = st.selectbox(
        "Choose AI Model",
        list(AVAILABLE_MODELS.keys()),
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

    # --------------------------------------------------------
    # NEW CHAT
    # --------------------------------------------------------

    if st.button(
        "➕ New Chat",
        use_container_width=True,
    ):

        st.session_state.current_chat = (
            create_chat()
        )

        st.session_state.messages = []

        st.rerun()

    # --------------------------------------------------------
    # CHAT HISTORY
    # --------------------------------------------------------

    st.subheader("💬 Chat History")

    chats = get_chat_files()

    if chats:

        for chat in chats:

            col1, col2 = st.columns(
                [5, 1]
            )

            with col1:

                if st.button(
                    chat.replace(".json", ""),
                    key=f"chat_{chat}",
                    use_container_width=True,
                ):

                    st.session_state.current_chat = chat

                    st.session_state.messages = (
                        load_chat(chat)
                    )

                    st.rerun()

            with col2:

                if st.button(
                    "❌",
                    key=f"del_{chat}",
                ):

                    delete_chat(chat)

                    if (
                        st.session_state.current_chat
                        == chat
                    ):

                        st.session_state.current_chat = (
                            None
                        )

                        st.session_state.messages = []

                    st.rerun()

    else:

        st.info("No chats found.")

    # --------------------------------------------------------
    # CLEAR MESSAGES
    # --------------------------------------------------------

    st.markdown("---")

    if st.button(
        "🧹 Clear Messages",
        use_container_width=True,
    ):

        st.session_state.messages = []

        if st.session_state.current_chat:

            save_chat(
                st.session_state.current_chat,
                [],
            )

        st.rerun()

    # --------------------------------------------------------
    # RENAME CHAT
    # --------------------------------------------------------

    st.markdown("---")

    new_name = st.text_input(
        "Rename Current Chat",
        placeholder="My AI Project",
    )

    if st.button(
        "✏ Rename Chat",
        use_container_width=True,
    ):

        if (
            new_name.strip()
            and st.session_state.current_chat
        ):

            st.session_state.current_chat = (
                rename_chat(
                    st.session_state.current_chat,
                    new_name.strip(),
                )
            )

            st.rerun()

    # --------------------------------------------------------
    # DELETE CURRENT CHAT
    # --------------------------------------------------------

    if st.button(
        "🗑 Delete Current Chat",
        use_container_width=True,
    ):

        if st.session_state.current_chat:

            delete_chat(
                st.session_state.current_chat
            )

        chats = get_chat_files()

        if chats:

            st.session_state.current_chat = (
                chats[0]
            )

            st.session_state.messages = (
                load_chat(chats[0])
            )

        else:

            st.session_state.current_chat = (
                create_chat()
            )

            st.session_state.messages = []

        st.rerun()

    # --------------------------------------------------------
    # USER INFO
    # --------------------------------------------------------

    st.markdown("---")

    st.metric(
        "Messages",
        len(
            st.session_state.messages
        ),
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

    # --------------------------------------------------------
    # LOGOUT
    # --------------------------------------------------------

    st.markdown("---")

    if st.button(
        "🚪 Logout",
        use_container_width=True,
    ):

        token = (
            st.session_state.access_token
        )

        if token:

            logout_user(token)

        st.session_state.authenticated = False

        st.session_state.access_token = None

        st.session_state.user = None

        st.session_state.current_chat = None

        st.session_state.messages = []

        st.session_state.last_prompt = ""

        st.rerun()


# ============================================================
# CREATE CHAT IF NEEDED
# ============================================================

if st.session_state.current_chat is None:

    st.session_state.current_chat = (
        create_chat()
    )

    st.session_state.messages = (
        load_chat(
            st.session_state.current_chat
        )
    )


# ============================================================
# MAIN PAGE
# ============================================================

st.title("🤖 HyperGPT")

st.markdown(
    f"""
### Your Intelligent AI Workspace

Welcome back, **{user.get('username', 'User')}**.

Ask questions, generate ideas, write code,
and chat with your AI assistant.
"""
)

st.divider()


# ============================================================
# DISPLAY MESSAGES
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

prompt = st.chat_input(
    "💬 Ask HyperGPT anything..."
)


if prompt:

    st.session_state.last_prompt = prompt

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # AI RESPONSE
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        start_time = time.time()

        with st.spinner(
            "Thinking..."
        ):

            response = chat_with_ai(
                message=prompt,
                chat_id=(
                    st.session_state.current_chat
                    .replace(".json", "")
                ),
                model=model,
                token=(
                    st.session_state.access_token
                ),
            )

        response_time = round(
            time.time() - start_time,
            2,
        )

        st.session_state.last_response_time = (
            response_time
        )

        # ----------------------------------------------------
        # STREAM RESPONSE
        # ----------------------------------------------------

        placeholder = st.empty()

        streamed = ""

        for chunk in stream_text(
            response
        ):

            streamed += chunk

            placeholder.markdown(
                streamed
            )

        st.caption(
            f"⚡ Response generated in "
            f"{response_time} seconds"
        )

        # ----------------------------------------------------
        # RAW RESPONSE
        # ----------------------------------------------------

        with st.expander(
            "View Raw Response"
        ):

            st.code(
                response,
                language="text",
            )

    # --------------------------------------------------------
    # SAVE AI MESSAGE
    # --------------------------------------------------------

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