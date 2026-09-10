"""
Basic Chatbot with LangGraph
"""

# =============================================================================
# IMPORTS
# =============================================================================

import streamlit as st
from langchain_openai import ChatOpenAI
from utils.styles import apply_base_css
from utils.formatting import render_assistant_text
from utils.starters import render_starters
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict


# =============================================================================
# PAGE SETUP
# =============================================================================

st.set_page_config(
    page_title="Basic Chatbot",
    page_icon=None,
    layout="centered"
)

apply_base_css()

st.markdown('<div class="page-title">Basic AI Chat</div>', unsafe_allow_html=True)
st.markdown('<div class="page-caption">A friendly AI assistant that chats with you.</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)


# =============================================================================
# SESSION STATE
# =============================================================================

if "llm" not in st.session_state:
    st.session_state.llm = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chatbot" not in st.session_state:
    st.session_state.chatbot = None

if "basic_persona" not in st.session_state:
    st.session_state.basic_persona = ""


# =============================================================================
# CHECK API KEY FROM HOME PAGE
# =============================================================================

openai_key = st.session_state.get("openai_key", "")

if not openai_key:
    st.markdown("""
    <div class="warn-banner">
        No API key found. Please go back to the Home page and save your OpenAI API key first.
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Home"):
        st.switch_page("Home.py")
    st.stop()
else:
    st.markdown("""
    <div class="info-banner">OpenAI key loaded from Home — ready to chat.</div>
    """, unsafe_allow_html=True)


# =============================================================================
# CUSTOM PERSONALITY
# =============================================================================
# Lets the user set how the assistant should act (e.g. "act like a witty
# stand-up comedian") instead of the fixed default. Same text-input-plus-
# button pattern as the "Save API Keys" control on the Home page — applying
# it becomes the system prompt chatbot_node() uses below, and starts a fresh
# conversation under the new personality.

st.markdown('<div class="sec-label">Assistant personality (optional)</div>', unsafe_allow_html=True)
persona_col, apply_col = st.columns([4, 1])
with persona_col:
    persona_input = st.text_input(
        "Tell the assistant how to act",
        value=st.session_state.basic_persona,
        placeholder="e.g. Act like a witty stand-up comedian who jokes around",
        label_visibility="collapsed",
    )
with apply_col:
    with st.container(key="cta_apply_persona"):
        apply_persona = st.button("Apply", use_container_width=True)

if apply_persona:
    st.session_state.basic_persona = persona_input.strip()
    st.session_state.messages = []
    st.rerun()

if st.session_state.basic_persona:
    cap_col, reset_col = st.columns([5, 1])
    with cap_col:
        st.caption(f"Currently acting as: “{st.session_state.basic_persona}”")
    with reset_col:
        if st.button("Reset", key="reset_persona"):
            st.session_state.basic_persona = ""
            st.session_state.messages = []
            st.rerun()

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:
    st.markdown("**Basic AI Chat**")
    st.caption("Simple LLM conversation with no tools or retrieval.")
    st.divider()
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.session_state.chatbot = None
        st.session_state.llm = None
        st.rerun()
    if st.button("Home"):
        st.switch_page("Home.py")


# =============================================================================
# INITIALIZE AI
# =============================================================================

if not st.session_state.llm:
    st.session_state.llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=openai_key
    )


# =============================================================================
# BUILD CHATBOT GRAPH
# =============================================================================

if st.session_state.llm and not st.session_state.chatbot:

    class State(TypedDict):
        messages: Annotated[list, add_messages]

    def chatbot_node(state: State):
        persona = st.session_state.get("basic_persona", "").strip()
        if persona:
            prompt = (
                f"You are an AI assistant. Behave exactly as instructed here, "
                f"and stay in this style for the whole conversation: {persona}"
            )
        else:
            prompt = "You are a helpful and friendly AI assistant. Have natural conversations with users."
        system_msg = SystemMessage(content=prompt)
        messages = [system_msg] + state["messages"]
        response = st.session_state.llm.invoke(messages)
        return {"messages": [response]}

    workflow = StateGraph(State)
    workflow.add_node("chatbot", chatbot_node)
    workflow.add_edge(START, "chatbot")
    workflow.add_edge("chatbot", END)
    st.session_state.chatbot = workflow.compile()


# =============================================================================
# GREETING
# =============================================================================

if not st.session_state.messages:
    if st.session_state.basic_persona:
        greeting = "Hi! I'm set up with the personality you described. What can I do for you today?"
    else:
        greeting = "Hi! My name is Assistant. What can I do for you today?"
    st.session_state.messages.append({"role": "assistant", "content": greeting})

# =============================================================================
# CHAT HISTORY
# =============================================================================
# The loop below is the ONLY place a message is ever drawn to the screen. New
# messages are appended to session_state and then st.rerun() is called so the
# very next script run redraws everything through this same loop — never a
# separate one-off render followed later by a second render of the same
# content (that dual code path is what caused responses to briefly appear
# twice, with a faded duplicate, when a new message was submitted).

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            render_assistant_text(message["content"])
        else:
            st.write(message["content"])

# Conversation starters — only while the chat is still just the greeting.
starter_clicked = None
if len(st.session_state.messages) == 1:
    starter_clicked = render_starters([
        "Tell me an interesting fact I probably don't know",
        "Help me brainstorm a birthday gift idea",
        "Explain machine learning like I'm new to it",
        "Tell me a joke",
    ], key="basic_chat")


# =============================================================================
# USER INPUT
# =============================================================================

user_input = st.chat_input("Type your message...") or starter_clicked

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()


# =============================================================================
# GENERATE A REPLY WHEN THE LAST MESSAGE IS FROM THE USER
# =============================================================================

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            messages = []
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                else:
                    messages.append(AIMessage(content=msg["content"]))

            result = st.session_state.chatbot.invoke({"messages": messages})
            response = result["messages"][-1].content

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()