"""
Conversation-starter chips for the LLM Bootcamp Project.

Shown only while a chat is still at its empty/greeting state, so a user can
tap a suggestion instead of typing one. This is a pure UI helper: it renders
buttons and hands back which one (if any) was clicked this run — the calling
page decides what to do with that, using the exact same "append the message
then st.rerun()" pattern it already uses for st.chat_input. Nothing here
touches session state, message history, or how a page talks to its model.
"""

import streamlit as st


def render_starters(prompts: list[str], key: str) -> str | None:
    """Render up to 4 starter chips (2 per row) inside a keyed container so
    utils/styles.py can style them consistently everywhere. `key` must be
    unique per call site. Returns the clicked prompt's text, or None."""
    prompts = list(prompts or [])[:4]
    if not prompts:
        return None

    clicked = None
    with st.container(key=f"starters_{key}"):
        st.markdown('<div class="starters-label">Or try one of these</div>', unsafe_allow_html=True)
        indexed = list(enumerate(prompts))
        for row_start in range(0, len(indexed), 2):
            row = indexed[row_start: row_start + 2]
            cols = st.columns(2)
            for col, (i, prompt) in zip(cols, row):
                with col:
                    if st.button(prompt, key=f"starter_{key}_{i}", use_container_width=True):
                        clicked = prompt
    return clicked
