"""
Shared assistant-response rendering for the LLM Bootcamp Project.

Why this exists (Day 5 retro fix — "answer/response formatting issues seen
during the final project"):

Model responses sometimes contain Markdown links, e.g. `[label](https://...)`,
especially from the search agent (Tavily) and MCP tools. `st.write()` renders
plain strings through Streamlit's Markdown pipeline, but it also HTML-escapes
raw angle brackets and can leave link syntax looking broken or, worse, let
literal HTML from a tool result leak into the page unescaped. This mirrored
what participants hit during the final project: URLs and bold/italic markup
in agent answers either printed literally (`[Docs](https://example.com)`
instead of a clickable link) or broke the layout.

`render_assistant_text()` fixes this once, consistently: it escapes all text
by default (safe against stray HTML from tool output), converts well-formed
Markdown (links, **bold**, *italics*, "- "/"* " bullet lists) into real HTML
itself, and lays the result out with HTML we control (no leftover blank
lines). Every page that displays a model-generated answer should call this
instead of `st.write(...)` for the assistant role.

Why NOT just pass the escaped text straight to st.markdown(): Streamlit's
st.markdown() ALWAYS runs its argument through a Markdown parser, even with
unsafe_allow_html=True (that flag only permits raw tags through — it doesn't
turn parsing off). Wrapping escaped text in a single `<div>` and relying on
`white-space: pre-wrap` to preserve blank lines used to leave literal blank
lines inside that div. Per CommonMark, an HTML block like `<div>` ends at the
first blank line, so everything BEFORE the first blank line stayed raw/
literal (e.g. `**bold**` printed literally) while everything AFTER a blank
line got reparsed as ordinary Markdown (e.g. "- [text](url)" turned into a
real bulleted `<li>` with the browser's default margins) — an inconsistent
mix, plus each blank line adding its own paragraph gap on top of that. That
combination is what produced the "weird gap" / half-formatted look. Building
the HTML ourselves (no stray blank lines, spacing set by our own CSS) avoids
the whole class of issue instead of just patching one symptom of it.
"""

import html
import re

import streamlit as st

_MD_LINK = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")
_MD_BOLD = re.compile(r"\*\*([^\n*]+)\*\*")
_MD_ITALIC = re.compile(r"(?<!\*)\*([^\n*]+)\*(?!\*)")
_BULLET_LINE = re.compile(r"^\s*[-*]\s+(.*)$")


def _inline_html(segment: str) -> str:
    """Escape a run of plain text and convert inline Markdown (links, bold,
    italics) into real HTML. `segment` has no newlines in it."""
    parts: list[str] = []
    last = 0
    for m in _MD_LINK.finditer(segment):
        parts.append(html.escape(segment[last: m.start()]))
        label, raw_url = m.group(1), m.group(2).strip()
        if raw_url.startswith(("http://", "https://")):
            href = html.escape(raw_url, quote=True)
            parts.append(
                f'<a href="{href}" target="_blank" rel="noopener noreferrer">'
                f"{html.escape(label)}</a>"
            )
        else:
            parts.append(html.escape(m.group(0)))
        last = m.end()
    parts.append(html.escape(segment[last:]))
    out = "".join(parts)
    out = _MD_BOLD.sub(lambda m: f"<strong>{m.group(1)}</strong>", out)
    out = _MD_ITALIC.sub(lambda m: f"<em>{m.group(1)}</em>", out)
    return out


def render_assistant_text(text: str) -> None:
    """Render model/agent output safely: escapes plain text, turns Markdown
    links/bold/italics into real HTML, and renders "- "/"* " lines as an
    actual bulleted list — laid out with our own spacing so there's never a
    leftover blank line for Streamlit's Markdown parser to reinterpret. Use
    this for ASSISTANT messages; plain user input can still use st.write()."""
    text = (text or "").strip("\n")

    # Blank-line-separated blocks; a block is either a run of consecutive
    # bullet lines (-> one <ul>) or a paragraph (-> one <p>, internal single
    # newlines become <br>).
    blocks_html: list[str] = []
    for block in re.split(r"\n\s*\n", text):
        lines = [ln for ln in block.split("\n") if ln.strip()]
        if not lines:
            continue
        bullet_matches = [_BULLET_LINE.match(ln) for ln in lines]
        if all(bullet_matches):
            items = "".join(f"<li>{_inline_html(m.group(1))}</li>" for m in bullet_matches)
            blocks_html.append(f'<ul style="margin:0.3rem 0 0.3rem 1.1rem; padding:0;">{items}</ul>')
        else:
            para = "<br>".join(_inline_html(ln) for ln in lines)
            blocks_html.append(f'<p style="margin:0 0 0.6rem;">{para}</p>')

    if blocks_html:
        blocks_html[-1] = blocks_html[-1].replace('margin:0 0 0.6rem', 'margin:0', 1)

    st.markdown(
        f'<div>{"".join(blocks_html)}</div>',
        unsafe_allow_html=True,
    )
