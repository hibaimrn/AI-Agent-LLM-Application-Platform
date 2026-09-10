"""
Chatbot Agent - AI agent with live web search via Tavily.
"""

# =============================================================================
# IMPORTS
# =============================================================================

import streamlit as st
import os
from datetime import datetime

from utils.styles import apply_base_css
from utils.formatting import render_assistant_text as _render_assistant_text
from utils.starters import render_starters
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain.agents import create_agent


# =============================================================================
# PAGE SETUP
# =============================================================================

st.set_page_config(
    page_title="Chatbot Agent",
    page_icon=None,
    layout="centered"
)

apply_base_css()

st.markdown('<div class="page-title">Search-Enabled Chat</div>', unsafe_allow_html=True)
st.markdown('<div class="page-caption">AI agent with live web search capabilities via Tavily.</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)


# =============================================================================
# SESSION STATE
# =============================================================================

if "agent" not in st.session_state:
    st.session_state.agent = None

if "agent_messages" not in st.session_state:
    st.session_state.agent_messages = []


# =============================================================================
# CHECK API KEYS FROM HOME PAGE
# =============================================================================

openai_key = st.session_state.get("openai_key", "")
tavily_key = st.session_state.get("tavily_key", "")

missing = []
if not openai_key:
    missing.append("OpenAI")
if not tavily_key:
    missing.append("Tavily")

if missing:
    st.markdown(f"""
    <div class="warn-banner">
        Missing API keys: <strong>{", ".join(missing)}</strong>.
        Please go back to the Home page and save your keys first.
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Home"):
        st.switch_page("Home.py")
    st.stop()
else:
    st.markdown("""
    <div class="info-banner">OpenAI and Tavily keys loaded — ready to search and chat.</div>
    """, unsafe_allow_html=True)


# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:
    st.markdown("**Search-Enabled Chat**")
    st.caption("AI agent with live web search via Tavily.")
    st.divider()
    if st.button("Clear chat"):
        st.session_state.agent_messages = []
        st.session_state.agent = None
        st.rerun()
    if st.button("Home"):
        st.switch_page("Home.py")


# =============================================================================
# CREATE AGENT
# =============================================================================

if not st.session_state.agent:
    os.environ["OPENAI_API_KEY"] = openai_key
    os.environ["TAVILY_API_KEY"] = tavily_key

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    search_tool = TavilySearch(
        max_results=5,
        description=(
            "Search the live web for up-to-date information, "
            "latest figures, prices, releases, sports scores, or anything that may have "
            "changed after the model's knowledge cutoff. Input should always be a search query string."
        ),
    )

    # Without an explicit system prompt the model falls back on its own training
    # data for anything date/time-related (e.g. confidently answering "today's
    # date" with a stale date from training) instead of using the search tool,
    # which is why real-time / current-date questions were coming back wrong.
    # Grounding it with the actual current date + an explicit "always search"
    # instruction fixes that.
    today_str = datetime.now().strftime("%A, %B %d, %Y")
    system_prompt = (
        f"You are a helpful assistant with access to a live web search tool. "
        f"Today's date is {today_str}. You do NOT reliably know the current date, "
        f"recent events, or any real-time information (prices, scores, news, "
        f"releases, etc.) from your training data — for ANY question that depends "
        f"on current or time-sensitive information, you MUST call the search tool "
        f"rather than answering from memory, even if you think you already know "
        f"the answer. Base your final answer on the actual search results returned, "
        f"and mention the date/source when it's relevant to the answer."
    )

    st.session_state.agent = create_agent(llm, tools=[search_tool], system_prompt=system_prompt)


# =============================================================================
# GREETING
# =============================================================================

if not st.session_state.agent_messages:
    greeting = "Hi! My name is Assistant. I can search the web for up-to-date information. What would you like to know today?"
    st.session_state.agent_messages.append({"role": "assistant", "content": greeting})

# =============================================================================
# CHAT HISTORY
# =============================================================================

for message in st.session_state.agent_messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            _render_assistant_text(message["content"])
        else:
            st.write(message["content"])

# Conversation starters — only while the chat is still just the greeting.
starter_clicked = None
if len(st.session_state.agent_messages) == 1:
    starter_clicked = render_starters([
        "What's today's date?",
        "What's the latest news in tech?",
        "What's the current weather in New York?",
        "Summarize today's top headlines",
    ], key="search_chat")


# =============================================================================
# USER INPUT
# =============================================================================

user_input = st.chat_input("Ask me anything...") or starter_clicked

if user_input:
    st.session_state.agent_messages.append({"role": "user", "content": user_input})
    st.rerun()


# =============================================================================
# GENERATE A REPLY WHEN THE LAST MESSAGE IS FROM THE USER
# =============================================================================

if st.session_state.agent_messages and st.session_state.agent_messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Searching and thinking..."):
            response = st.session_state.agent.invoke({
                "messages": st.session_state.agent_messages
            })
            response_text = response["messages"][-1].content

    st.session_state.agent_messages.append({
        "role": "assistant",
        "content": response_text
    })
    st.rerun()