import streamlit as st

from agent import run_agent_turn

st.set_page_config(page_title="MilliAI", page_icon="💗")

st.markdown(
    """
    <style>
    /* Full-page cherry-blossom sky background */
    html, body, .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background: linear-gradient(180deg, #fff0f6 0%, #ffe3ef 55%, #ffd6e8 100%) !important;
        background-attachment: fixed !important;
    }
    /* Make Streamlit's top header transparent so the gradient is truly full-page */
    [data-testid="stHeader"] {
        background: transparent !important;
    }

    .milli-title {
        font-size: 6.5rem !important;
        line-height: 1.05 !important;
        font-weight: 900 !important;
        text-align: center;
        letter-spacing: -3px;
        background: linear-gradient(90deg, #ff4f97, #ff8fc4, #ff4f97);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.2rem 0 0.1rem 0;
        text-shadow: 0 2px 24px rgba(255, 120, 180, 0.25);
    }
    .milli-sub {
        text-align: center;
        color: #d1477a;
        font-size: 1.15rem;
        margin-top: 0;
        margin-bottom: 1.5rem;
    }

    /* Soften chat bubbles with a pink tint */
    [data-testid="stChatMessage"] {
        background: rgba(255, 238, 246, 0.85);
        border-radius: 16px;
    }

    /* Force dark text in questions + replies so it stays readable on pink,
       even if the visitor's browser/OS is in dark mode. */
    [data-testid="stChatMessage"],
    [data-testid="stChatMessage"] * {
        color: #2b2b2b !important;
    }
    /* Keep the input box text dark and readable too. */
    [data-testid="stChatInput"] textarea {
        color: #2b2b2b !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #9a6b80 !important;
    }

    /* Falling cherry-blossom petals: fall + sway + slow fade in/out */
    .petal {
        position: fixed;
        top: -8vh;
        z-index: 0;
        pointer-events: none;
        user-select: none;
        font-size: 1.6rem;
        animation-name: petal-fall, petal-sway, petal-fade;
        animation-timing-function: linear, ease-in-out, ease-in-out;
        animation-iteration-count: infinite, infinite, infinite;
    }
    @keyframes petal-fall {
        0%   { top: -8vh; }
        100% { top: 108vh; }
    }
    @keyframes petal-sway {
        0%   { transform: translateX(0) rotate(0deg); }
        50%  { transform: translateX(60px) rotate(180deg); }
        100% { transform: translateX(0) rotate(360deg); }
    }
    @keyframes petal-fade {
        0%, 100% { opacity: 0; }
        25%, 75% { opacity: 0.9; }
    }
    </style>

    <div class="petals">
        <span class="petal" style="left:5%;  animation-duration: 12s, 4s, 6s;  animation-delay: 0s,   0s,   0s;">🌸</span>
        <span class="petal" style="left:15%; animation-duration: 15s, 5s, 7s;  animation-delay: 1.5s, 0.5s, 1s;">🌸</span>
        <span class="petal" style="left:25%; animation-duration: 11s, 4.5s,5s; animation-delay: 3s,   1s,   2s;">🌸</span>
        <span class="petal" style="left:35%; animation-duration: 16s, 6s, 8s;  animation-delay: 0.5s, 0s,   0.5s;">🌸</span>
        <span class="petal" style="left:45%; animation-duration: 13s, 5s, 6s;  animation-delay: 2s,   1.5s, 1.5s;">🌸</span>
        <span class="petal" style="left:55%; animation-duration: 12s, 4s, 7s;  animation-delay: 4s,   0.5s, 0s;">🌸</span>
        <span class="petal" style="left:65%; animation-duration: 17s, 6s, 8s;  animation-delay: 1s,   1s,   2.5s;">🌸</span>
        <span class="petal" style="left:75%; animation-duration: 11.5s,4.5s,5s;animation-delay: 3.5s, 0s,   1s;">🌸</span>
        <span class="petal" style="left:85%; animation-duration: 14s, 5s, 7s;  animation-delay: 0s,   1.5s, 0.5s;">🌸</span>
        <span class="petal" style="left:95%; animation-duration: 13s, 5.5s,6s; animation-delay: 2.5s, 0.5s, 2s;">🌸</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="milli-title">MilliAI</div>', unsafe_allow_html=True)
st.markdown('<div class="milli-sub">your friendly AI assistant</div>', unsafe_allow_html=True)

# --- Two kinds of state ---
# engine_messages: the FULL history the LLM sees (user + assistant + tool msgs).
#                  This is the agent's memory across turns.
# display:         only what we render as chat bubbles (role, text).
if "engine_messages" not in st.session_state:
    st.session_state.engine_messages = []
if "display" not in st.session_state:
    st.session_state.display = []

# Re-draw the conversation so far.
for role, content in st.session_state.display:
    with st.chat_message(role):
        st.markdown(content)

# Input box pinned to the bottom (ChatGPT style).
prompt = st.chat_input("Ask something...")
if prompt:
    # Show + record the user's message.
    st.session_state.display.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.engine_messages.append({"role": "user", "content": prompt})

    # Run the agent and show its reply.
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer, tool_events = run_agent_turn(st.session_state.engine_messages)
        for name, args in tool_events:
            st.caption(f"🔧 {name}({args})")
        st.markdown(answer or "_(no answer)_")

    st.session_state.display.append(("assistant", answer or "_(no answer)_"))
