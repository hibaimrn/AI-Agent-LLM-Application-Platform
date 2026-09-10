"""
Shared CSS styles for the LLM Bootcamp Project.
Call the appropriate apply_*_css() function once at the top of each page,
right after st.set_page_config().

Design system note: every color/spacing/radius value used anywhere in the
app is defined ONCE in _TOKENS_CSS below as a CSS custom property (e.g.
var(--accent)). All three apply_*_css() functions load _TOKENS_CSS first,
then their own page-specific rules on top. To retheme the whole app, change
a value in _TOKENS_CSS — nothing else needs to move. This is a pure CSS/
visual layer: it doesn't touch page logic, session state, or control flow,
so it can be explained separately from (and skipped when walking through)
how each page actually works.

Theme: "modern SaaS" — vibrant indigo/violet accent, rounded cards, soft
colored shadows, and a subtle gradient used sparingly on primary actions,
chat avatars, and card accents (Linear/Notion/Vercel-style polish).
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Design tokens + resets shared by every page (Home + pages 1-5)
# ---------------------------------------------------------------------------

_TOKENS_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #ffffff;
        --bg-secondary: #f8f8fc;
        --bg-tertiary: #f1f1f8;
        --border: #e5e7eb;
        --border-subtle: #eef0f4;
        --text: #111827;
        --text-secondary: #6b7280;
        --text-tertiary: #9ca3af;
        --accent: #6366f1;
        --accent-hover: #4f46e5;
        --accent-2: #8b5cf6;
        --accent-gradient: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        --accent-soft-bg: #eef0ff;
        --accent-soft-border: #d7dafc;
        --success-bg: #ecfdf3;
        --success-border: #b7ebc6;
        --success-text: #12805c;
        --warn-bg: #fffaeb;
        --warn-border: #fde68a;
        --warn-text: #92640a;
        --danger-bg: #fef2f2;
        --danger-border: #fecaca;
        --danger-text: #b42318;
        --radius: 12px;
        --radius-sm: 8px;
        --radius-lg: 16px;
        --shadow-sm: 0 1px 2px rgba(17, 24, 39, 0.04), 0 1px 3px rgba(17, 24, 39, 0.03);
        --shadow-md: 0 8px 20px rgba(99, 102, 241, 0.12), 0 2px 6px rgba(17, 24, 39, 0.05);
        --shadow-glow: 0 4px 14px rgba(99, 102, 241, 0.32);
    }

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    #MainMenu, footer { visibility: hidden; }
    /* keep the header transparent so the sidebar collapse arrow stays reachable */
    [data-testid="stHeader"] { background: transparent !important; box-shadow: none !important; }
    [data-testid="stAppDeployButton"] { display: none !important; }
    /* keep the sidebar expand control reachable even with the header hidden */
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] { visibility: visible !important; }

    .stApp { background-color: var(--bg); }
    [data-testid="stSidebar"] { background-color: var(--bg-secondary); border-right: 1px solid var(--border-subtle); }

    /* Page-nav links in the sidebar get a rounded hover/active highlight,
       matching the rest of the rounded, colorful UI. */
    [data-testid="stSidebarNav"] a, [data-testid="stSidebarNavLink"] {
        border-radius: var(--radius-sm) !important;
        transition: background 120ms ease, color 120ms ease;
    }
    [data-testid="stSidebarNav"] a:hover { background: var(--accent-soft-bg) !important; }
    [data-testid="stSidebarNav"] a[aria-current="page"],
    [data-testid="stSidebarNav"] a[aria-selected="true"] {
        background: var(--accent-soft-bg) !important;
        color: var(--accent-hover) !important;
        font-weight: 700 !important;
    }

    a { color: var(--accent); font-weight: 600; }

    /* Chat avatars — a gradient assistant avatar with a soft glow, neutral
       user avatar — consistent across all chat pages. */
    [data-testid="stChatMessageAvatarAssistant"] {
        background: var(--accent-gradient) !important;
        box-shadow: var(--shadow-glow);
    }
    [data-testid="stChatMessageAvatarAssistant"] svg { fill: #fff !important; }
    [data-testid="stChatMessageAvatarUser"],
    [data-testid="stChatMessageAvatarUser"] svg { background-color: var(--text-secondary) !important; fill: #fff !important; }

    /* Buttons — one consistent ghost style everywhere by default, rounded
       with a gentle lift-and-glow on hover */
    .stButton > button, .stDownloadButton > button {
        border-radius: var(--radius) !important;
        border: 1px solid var(--border) !important;
        background: var(--bg) !important;
        color: var(--text) !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
        box-shadow: var(--shadow-sm) !important;
        transition: border-color 150ms ease, color 150ms ease, background 150ms ease,
                    box-shadow 150ms ease, transform 150ms ease;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        border-color: var(--accent) !important;
        color: var(--accent-hover) !important;
        background: var(--accent-soft-bg) !important;
        box-shadow: var(--shadow-md) !important;
        transform: translateY(-1px);
    }
    /* Primary call-to-action buttons opt in by wrapping with
       st.container(key="cta_..."), which stamps a stable "st-key-cta_..."
       class on the wrapping div (same technique used for the Home page's
       module cards) — used for "Save API Keys", "Connect to MCP Server",
       "Apply personality", etc. */
    div[class*="st-key-cta_"] .stButton > button {
        background: var(--accent-gradient) !important;
        color: #ffffff !important;
        border: 1px solid transparent !important;
        font-weight: 700 !important;
        width: 100% !important;
        box-shadow: var(--shadow-glow) !important;
    }
    div[class*="st-key-cta_"] .stButton > button:hover {
        filter: brightness(1.07);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.45) !important;
        transform: translateY(-1px);
        color: #ffffff !important;
    }

    .stTextInput input, .stTextArea textarea {
        border-radius: var(--radius-sm) !important;
        border-color: var(--border) !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px var(--accent-soft-bg) !important;
    }

    div[data-testid="stExpander"] {
        border-radius: var(--radius) !important;
        border-color: var(--border-subtle) !important;
        box-shadow: var(--shadow-sm);
    }
    div[data-testid="stFileUploaderDropzone"] {
        border-radius: var(--radius) !important;
        background: var(--bg-secondary) !important;
        border: 1.5px dashed var(--border) !important;
    }

    /* Conversation-starter chips (utils/starters.py render_starters()) —
       targets the st.container(key="starters_...") wrapper by its stable
       "st-key-starters_*" class. */
    .starters-label {
        font-size: 0.7rem;
        font-weight: 700;
        color: var(--text-tertiary);
        margin: 0.25rem 0 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    div[class*="st-key-starters_"] { margin-bottom: 1rem; }
    div[class*="st-key-starters_"] .stButton > button {
        background: var(--accent-soft-bg) !important;
        border: 1px solid var(--accent-soft-border) !important;
        color: var(--accent-hover) !important;
        text-align: left !important;
        font-weight: 500 !important;
        font-size: 0.8rem !important;
        padding: 0.6rem 0.9rem !important;
        white-space: normal !important;
        height: auto !important;
        line-height: 1.4 !important;
        box-shadow: none !important;
    }
    div[class*="st-key-starters_"] .stButton > button:hover {
        background: var(--accent-gradient) !important;
        border-color: transparent !important;
        color: #ffffff !important;
        box-shadow: var(--shadow-glow) !important;
        transform: translateY(-1px);
    }
</style>
"""

# ---------------------------------------------------------------------------
# Shared base — used by pages 1-4 (Basic Chatbot, Chatbot Agent, RAG, MCP)
# ---------------------------------------------------------------------------

_BASE_CSS = """
<style>
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
        max-width: 860px !important;
    }
    .page-title {
        font-size: 1.4rem;
        font-weight: 800;
        color: var(--text);
        margin-bottom: 0.2rem;
        letter-spacing: -0.02em;
        display: flex;
        align-items: center;
        gap: 0.55rem;
    }
    .page-title::before {
        content: "";
        display: inline-block;
        width: 11px;
        height: 11px;
        border-radius: 4px;
        background: var(--accent-gradient);
        flex-shrink: 0;
    }
    .page-caption {
        font-size: 0.85rem;
        color: var(--text-secondary);
        margin-bottom: 1.25rem;
    }
    .divider {
        border: none;
        border-top: 1px solid var(--border-subtle);
        margin: 0 0 1.25rem;
    }
    .info-banner {
        background: var(--accent-soft-bg);
        border: 1px solid var(--accent-soft-border);
        border-left: 3px solid var(--accent);
        border-radius: var(--radius-sm);
        padding: 0.65rem 1rem;
        font-size: 0.82rem;
        color: var(--text);
        margin-bottom: 1.25rem;
    }
    .info-banner a { font-weight: 600; }
    .warn-banner {
        background: var(--warn-bg);
        border: 1px solid var(--warn-border);
        border-left: 3px solid var(--warn-text);
        border-radius: var(--radius-sm);
        padding: 0.65rem 1rem;
        font-size: 0.82rem;
        color: var(--warn-text);
        margin-bottom: 1.25rem;
    }
    /* Section labels — small uppercase eyebrow text used across pages
       (sidebars, "Customize this assistant", etc.) */
    .sec-label {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--text-tertiary);
        margin-bottom: 0.5rem;
    }
</style>
"""

# ---------------------------------------------------------------------------
# Home page — extends base with module grid, API section, and button overrides
# ---------------------------------------------------------------------------

_HOME_CSS = """
<style>
    .block-container {
        padding-top: 2.25rem !important;
        padding-bottom: 1rem !important;
        max-width: 900px !important;
    }

    .page-title {
        font-size: 1.75rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 0.35rem;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        display: inline-block;
    }
    .page-sub {
        font-size: 0.88rem;
        color: var(--text-secondary);
        max-width: 560px;
        margin: 0 0 1.5rem;
        line-height: 1.6;
    }

    .info-banner {
        background: var(--accent-soft-bg);
        border: 1px solid var(--accent-soft-border);
        border-left: 3px solid var(--accent);
        border-radius: var(--radius-sm);
        padding: 0.7rem 1rem;
        font-size: 0.82rem;
        color: var(--text);
        margin-bottom: 1.75rem;
    }

    .divider {
        border: none;
        border-top: 1px solid var(--border-subtle);
        margin: 0 0 1.5rem;
    }

    .sec-label {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--text-tertiary);
        margin-bottom: 1rem;
    }

    /* Module cards use st.container(border=True, key="module_card_...") —
       Streamlit stamps the container's own wrapper with a stable
       "st-key-<key>" class, which is what this targets. A slim gradient
       bar across the top plus a lift-and-glow on hover give the grid a
       modern, tactile feel. */
    div[class*="st-key-module_card_"] {
        position: relative;
        overflow: hidden;
        border: 1px solid var(--border-subtle) !important;
        border-radius: var(--radius-lg) !important;
        box-shadow: var(--shadow-sm) !important;
        transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
    }
    div[class*="st-key-module_card_"]::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        background: var(--accent-gradient);
    }
    div[class*="st-key-module_card_"]:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-md) !important;
        border-color: var(--accent-soft-border) !important;
    }

    .module-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
        background: var(--accent-soft-bg);
        border-radius: var(--radius-sm);
        font-size: 0.7rem;
        font-weight: 800;
        color: var(--accent-hover);
    }

    .module-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: var(--text);
        margin: 0;
    }

    .module-desc {
        font-size: 0.8rem;
        color: var(--text-secondary);
        line-height: 1.55;
        flex: 1;
    }

    /* API section */
    .api-label {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--text-tertiary);
        margin-bottom: 0.75rem;
    }

    .footer-note {
        text-align: center;
        font-size: 0.7rem;
        color: var(--text-tertiary);
        padding-top: 0.75rem;
        border-top: 1px solid var(--border-subtle);
        margin-top: 0.5rem;
    }
</style>
"""

# ---------------------------------------------------------------------------
# Deep Agent page — same base chrome as pages 1-4 (font, title/caption,
# divider, banners, background, top/bottom spacing), plus ONLY the extra
# rules the two-column chat + side-panel layout genuinely needs: a wider
# block-container, and styles for the file/plan/skills panel itself. Keeping
# this layered on top of _BASE_CSS (instead of a separate parallel
# stylesheet) is what guarantees the two stay visually identical instead of
# slowly drifting apart.
# ---------------------------------------------------------------------------

_DEEP_AGENT_EXTRA_CSS = """
<style>
    /* Wider than the other pages so the chat + side panel fit comfortably —
       the one deliberate layout difference, needed for the panel. */
    .block-container {
        max-width: 1150px !important;
    }
    .da-status {
        display:inline-flex; align-items:center; gap:0.45rem;
        background: var(--success-bg); border: 1px solid var(--success-border); color: var(--success-text);
        border-radius: var(--radius-sm); padding:0.25rem 0.75rem; font-size:0.74rem; font-weight:700;
        margin-bottom: 1.25rem; box-shadow: var(--shadow-sm);
    }
    .da-dot { width:6px; height:6px; border-radius:50%; background: var(--success-text); }
    /* Panel */
    .panel-label {
        font-size:0.68rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase;
        color: var(--text-tertiary); margin:0 0 0.6rem 0; display:flex; align-items:center;
        justify-content:space-between;
    }
    .panel-label span {
        background: var(--accent-soft-bg); color: var(--accent-hover); border-radius: var(--radius-sm);
        padding:0.02rem 0.5rem; font-size:0.66rem; font-weight:700;
    }
    .file-meta { color: var(--text-tertiary); font-size:0.72rem; }
    .badge-new {
        background: var(--success-bg); color: var(--success-text); font-size:0.6rem; font-weight:700;
        padding:0.08rem 0.42rem; border-radius: var(--radius-sm); margin-left:0.45rem;
        letter-spacing:0.03em;
    }
    .todo-row { font-size:0.82rem; color: var(--text); padding:0.18rem 0; line-height:1.5; }
    .todo-row.done { color: var(--text-tertiary); text-decoration:line-through; }
    .dot { display:inline-block; width:8px; height:8px; border-radius:50%; margin-right:0.55rem; }
    .d-done { background: var(--success-text); } .d-prog { background:#b5790f; } .d-todo { background: var(--border); }
    .empty { color: var(--text-tertiary); font-size:0.8rem; }
    .stPopover > div > button {
        border-radius: var(--radius) !important; border:1px solid var(--border) !important;
        background: var(--bg) !important; font-size:0.82rem !important; font-weight:600 !important;
        text-align:left !important; color: var(--text) !important; box-shadow: var(--shadow-sm) !important;
    }
    .stPopover > div > button:hover {
        border-color: var(--accent) !important; background: var(--accent-soft-bg) !important;
        color: var(--accent-hover) !important;
    }
    [data-testid="stContainer"] { border-radius: var(--radius) !important; box-shadow: var(--shadow-sm); }
</style>
"""


def apply_base_css():
    """Apply shared styles for pages 1–4."""
    st.markdown(_TOKENS_CSS, unsafe_allow_html=True)
    st.markdown(_BASE_CSS, unsafe_allow_html=True)


def apply_home_css():
    """Apply styles for the Home page."""
    st.markdown(_TOKENS_CSS, unsafe_allow_html=True)
    st.markdown(_HOME_CSS, unsafe_allow_html=True)


def apply_deep_agent_css():
    """Apply styles for the Deep Agent Skill Architecture page: the same
    shared base as pages 1-4, plus the panel-only additions above."""
    st.markdown(_TOKENS_CSS, unsafe_allow_html=True)
    st.markdown(_BASE_CSS, unsafe_allow_html=True)
    st.markdown(_DEEP_AGENT_EXTRA_CSS, unsafe_allow_html=True)
