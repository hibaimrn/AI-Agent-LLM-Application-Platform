"""
MCP Agent - AI agent with Model Context Protocol server integration.
"""

# =============================================================================
# IMPORTS
# =============================================================================

import streamlit as st
import asyncio
import os
import nest_asyncio

from utils.styles import apply_base_css
from utils.formatting import render_assistant_text
from utils.starters import render_starters

nest_asyncio.apply()

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI


# =============================================================================
# PAGE SETUP
# =============================================================================

st.set_page_config(
    page_title="MCP Agent",
    page_icon=None,
    layout="centered"
)

apply_base_css()

st.markdown('<div class="page-title">MCP Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="page-caption">AI agent connected to external tools via the Model Context Protocol.</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)


# =============================================================================
# SESSION STATE
# =============================================================================

if "mcp_server_url" not in st.session_state:
    st.session_state.mcp_server_url = ""

if "mcp_api_key" not in st.session_state:
    st.session_state.mcp_api_key = ""

if "mcp_agent" not in st.session_state:
    st.session_state.mcp_agent = None

if "mcp_messages" not in st.session_state:
    st.session_state.mcp_messages = []

if "mcp_tool_names" not in st.session_state:
    st.session_state.mcp_tool_names = []


# =============================================================================
# CHECK OPENAI KEY FROM HOME PAGE
# =============================================================================

openai_key = st.session_state.get("openai_key", "")

if not openai_key:
    st.markdown("""
    <div class="warn-banner">
        No OpenAI API key found. Please go back to the Home page and save your key first.
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Home"):
        st.switch_page("Home.py")
    st.stop()


# =============================================================================
# MCP SERVER CONFIGURATION
# =============================================================================

# MCP server URL is specific to this page — ask for it here if not set
if not st.session_state.mcp_server_url:
    st.markdown("""
    <div class="info-banner">
        Enter your MCP server URL to connect. Use an API key for servers that
        require Authorization headers (e.g. Zapier MCP).
    </div>
    """, unsafe_allow_html=True)

    st.markdown('[Follow this Zapier MCP guide to get your MCP Server URL and API key](https://academy.datasciencedojo.com/pages/how-to-set-up-zapier-for-mcp-integration)', unsafe_allow_html=True)
    server_url = st.text_input("Server URL", placeholder="https://your-mcp-server.com")
    mcp_api_key = st.text_input("Token", type="password")

    with st.container(key="cta_connect_mcp"):
        connect_clicked = st.button("Connect to MCP Server")
    if connect_clicked:
        if server_url and (server_url.startswith("http://") or server_url.startswith("https://")):
            st.session_state.mcp_server_url = server_url
            st.session_state.mcp_api_key = mcp_api_key
            st.rerun()
        else:
            st.error("Please enter a valid URL starting with http:// or https://")
    st.stop()
else:
    st.markdown(f"""
    <div class="info-banner">
        OpenAI key loaded · MCP server connected: <strong>{st.session_state.mcp_server_url[:50]}...</strong>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:
    st.markdown("**MCP Chatbot**")
    st.caption("Connected to an external MCP tool server.")
    st.divider()
    if st.session_state.mcp_server_url:
        st.caption(f"Server: `{st.session_state.mcp_server_url[:30]}...`")
    if st.session_state.mcp_tool_names:
        with st.expander(f"Available tools ({len(st.session_state.mcp_tool_names)})"):
            st.caption(
                "If a Notion/other action isn't listed here, it isn't exposed by "
                "your Zapier MCP server yet — add it in Zapier, then reconnect."
            )
            for t in st.session_state.mcp_tool_names:
                st.caption(t)
    if st.button("Clear chat"):
        st.session_state.mcp_messages = []
        st.rerun()
    if st.button("Change MCP Server"):
        st.session_state.mcp_server_url = ""
        st.session_state.mcp_api_key = ""
        st.session_state.mcp_agent = None
        st.session_state.mcp_messages = []
        st.rerun()
    if st.button("Home"):
        st.switch_page("Home.py")


# =============================================================================
# INITIALIZE MCP AGENT
# =============================================================================

MCP_SYSTEM_PROMPT = (
    "You are an assistant with access to tools exposed by an external MCP server "
    "(for example, actions for Notion, Google Sheets, Slack, etc. via Zapier). "
    "Follow these rules when using them:\n"
    "1. Before doing anything else, check the tools you actually have available and "
    "pick the one whose name/description most closely matches the request. Never "
    "guess a tool exists — only call tools that were given to you.\n"
    "2. If the user asks you to find, retrieve, read, look up, or 'give me' something "
    "(e.g. a page, a document, a record), prefer a SEARCH / FIND / LIST style tool over "
    "a CREATE / WRITE / UPDATE style tool. Only use a create/write tool when the user "
    "explicitly asks to create, add, or update something.\n"
    "3. Never invent a required argument (e.g. a title, ID, or property value) that the "
    "user didn't give you. If a tool call fails because of a missing or invalid required "
    "argument, first try a broader search/list tool to discover the correct value (e.g. "
    "the exact title or ID) instead of guessing again.\n"
    "4. If a lookup by exact name/title returns nothing, retry with a partial or "
    "case-insensitive match before telling the user it doesn't exist.\n"
    "5. If a tool call still fails after that, tell the user plainly what failed and why "
    "(from the tool's error message), and mention that the item may need to be shared "
    "with the connected integration."
)


if not st.session_state.mcp_agent:
    with st.spinner("Initializing MCP agent..."):
        os.environ["OPENAI_API_KEY"] = openai_key

        async def init_agent():
            server_cfg = {
                "url": st.session_state.mcp_server_url,
                "transport": "streamable_http",
            }
            if st.session_state.mcp_api_key:
                server_cfg["headers"] = {
                    "Authorization": f"Bearer {st.session_state.mcp_api_key}"
                }
            client = MultiServerMCPClient({"server": server_cfg})
            tools = await client.get_tools()
            llm = ChatOpenAI(model="gpt-4o", temperature=0)
            return tools, create_agent(llm, tools=tools, system_prompt=MCP_SYSTEM_PROMPT)

        try:
            tools, agent = asyncio.get_event_loop().run_until_complete(init_agent())
            st.session_state.mcp_agent = agent
            # Kept only so the sidebar can show which tools/actions the connected
            # MCP server actually exposes — handy for diagnosing "it can't find my
            # Notion page" issues that turn out to be a missing/misconfigured
            # Zapier action rather than a bug in this app.
            st.session_state.mcp_tool_names = [
                f"{t.name} — {(t.description or '').strip().splitlines()[0][:80]}"
                for t in tools
            ]
        except ExceptionGroup as eg:
            for exc in eg.exceptions:
                st.error(f"MCP sub-error: {type(exc).__name__}: {exc}")
            st.session_state.mcp_server_url = ""
            st.session_state.mcp_agent = None
            st.stop()
        except Exception as e:
            st.error(f"Failed to initialize MCP agent: {type(e).__name__}: {e}")
            st.session_state.mcp_server_url = ""
            st.session_state.mcp_agent = None
            st.stop()


# =============================================================================
# GREETING
# =============================================================================

if not st.session_state.mcp_messages:
    greeting = "Hi! My name is Assistant. I'm connected to an MCP server and ready to use external tools. What can I help you with today?"
    st.session_state.mcp_messages.append({"role": "assistant", "content": greeting})

# =============================================================================
# CHAT HISTORY
# =============================================================================

for message in st.session_state.mcp_messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            render_assistant_text(message["content"])
        else:
            st.write(message["content"])

# Conversation starters — only while the chat is still just the greeting.
starter_clicked = None
if len(st.session_state.mcp_messages) == 1:
    starter_clicked = render_starters([
        "What tools do you have access to?",
        "Search for a page in my workspace",
        "What can you help me with here?",
        "Show me an example of what you can do",
    ], key="mcp_chat")


# =============================================================================
# USER INPUT
# =============================================================================

user_input = st.chat_input("Ask me anything...") or starter_clicked

if user_input:
    st.session_state.mcp_messages.append({"role": "user", "content": user_input})
    st.rerun()


# =============================================================================
# GENERATE A REPLY WHEN THE LAST MESSAGE IS FROM THE USER
# =============================================================================

if st.session_state.mcp_messages and st.session_state.mcp_messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Processing with MCP tools..."):
            async def run_agent():
                return await st.session_state.mcp_agent.ainvoke({
                    "messages": st.session_state.mcp_messages
                })

            try:
                response = asyncio.get_event_loop().run_until_complete(run_agent())
                response_text = response["messages"][-1].content
            except Exception as e:
                response_text = (
                    f"Error: {str(e)}\n\n"
                    "This usually means either the target item (e.g. a Notion page) "
                    "hasn't been shared with your Zapier/MCP integration, or the "
                    "connected action doesn't support what was asked. Check the "
                    "'Available tools' list in the sidebar and your Zapier MCP setup."
                )

    st.session_state.mcp_messages.append({
        "role": "assistant",
        "content": response_text
    })
    st.rerun()