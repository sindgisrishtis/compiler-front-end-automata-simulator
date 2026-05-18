"""
utils.py
========
Shared utility functions for formatting, highlighting, and display.
"""

import re
from typing import List
from lexer import Token


# ─────────────────────────────────────────────
# SYNTAX HIGHLIGHTING
# ─────────────────────────────────────────────

TOKEN_COLOURS = {
    "KEYWORD":    "#569cd6",   # blue
    "IDENTIFIER": "#9cdcfe",   # light blue
    "NUMBER":     "#b5cea8",   # green
    "FLOAT":      "#b5cea8",   # green
    "STRING":     "#ce9178",   # orange
    "CHAR_LIT":   "#ce9178",   # orange
    "OPERATOR":   "#d4d4d4",   # light grey
    "SYMBOL":     "#ffd700",   # gold
    "COMMENT":    "#6a9955",   # dark green
    "UNKNOWN":    "#e94560",   # red (error)
}


def highlight_source(source: str, tokens: List[Token]) -> str:
    """
    Return HTML with syntax-highlighted source code.
    Uses token positions to wrap spans.
    """
    if not tokens:
        return f'<pre style="color:#d4d4d4">{_escape(source)}</pre>'

    # Build char-level colour map
    colour_map = {}
    for tok in tokens:
        col = TOKEN_COLOURS.get(tok.type, "#d4d4d4")
        # Re-find in source (simple approach: match by value)

    # Simple line-by-line regex approach
    lines = source.split('\n')
    highlighted_lines = []

    KEYWORDS_SET = {
        "int","float","char","void","if","else","for","while","do",
        "return","break","continue","switch","case","default","struct",
        "typedef","double","long","short","unsigned","signed","const","static"
    }

    for line in lines:
        hl = _escape(line)
        # Strings first (to avoid re-highlighting)
        hl = re.sub(
            r'(&quot;[^&]*?&quot;|"[^"]*?")',
            lambda m: f'<span style="color:{TOKEN_COLOURS["STRING"]}">{m.group()}</span>',
            hl
        )
        # Comments
        hl = re.sub(
            r'(//.*?)$',
            lambda m: f'<span style="color:{TOKEN_COLOURS["COMMENT"]}">{m.group()}</span>',
            hl
        )
        # Keywords
        for kw in KEYWORDS_SET:
            hl = re.sub(
                rf'\b({kw})\b',
                f'<span style="color:{TOKEN_COLOURS["KEYWORD"]}">\\1</span>',
                hl
            )
        # Numbers
        hl = re.sub(
            r'\b(\d+\.\d+|\d+)\b',
            lambda m: f'<span style="color:{TOKEN_COLOURS["NUMBER"]}">{m.group()}</span>',
            hl
        )
        # Operators
        hl = re.sub(
            r'(==|!=|<=|>=|&&|\|\||[+\-*/%=<>!])',
            lambda m: f'<span style="color:{TOKEN_COLOURS["OPERATOR"]}">{m.group()}</span>',
            hl
        )
        # Symbols
        hl = re.sub(
            r'([(){}\[\];,])',
            lambda m: f'<span style="color:{TOKEN_COLOURS["SYMBOL"]}">{m.group()}</span>',
            hl
        )
        highlighted_lines.append(hl)

    body = '<br>'.join(highlighted_lines)
    return (
        f'<div style="background:#1e1e1e;padding:16px;border-radius:8px;'
        f'font-family:\'Courier New\',monospace;font-size:13px;'
        f'line-height:1.6;overflow-x:auto;">{body}</div>'
    )


def _escape(text: str) -> str:
    """HTML-escape special chars."""
    return (text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


# ─────────────────────────────────────────────
# STACK VISUALISER
# ─────────────────────────────────────────────

def render_stack_html(stack: List[str]) -> str:
    """Render the PDA stack as an HTML visual."""
    if not stack:
        return (
            '<div style="text-align:center;padding:24px;color:#6a9955;'
            'font-family:Courier New;font-size:14px;">'
            '⊥ Stack Empty (Bottom of Stack)</div>'
        )

    items_html = ""
    for i, item in enumerate(reversed(stack)):
        is_top = (i == 0)
        bg = "#0f3460" if not is_top else "#e94560"
        label = " ← TOP" if is_top else ""
        items_html += (
            f'<div style="background:{bg};border:1px solid #00d4ff;'
            f'margin:3px auto;width:120px;padding:8px;text-align:center;'
            f'border-radius:4px;font-family:Courier New;color:white;'
            f'font-size:14px;">{item}{label}</div>'
        )

    items_html += (
        '<div style="text-align:center;color:#6a9955;font-family:Courier New;'
        'font-size:11px;margin-top:4px;">⊥ BOTTOM</div>'
    )

    return f'<div style="display:flex;flex-direction:column;align-items:center;">{items_html}</div>'


# ─────────────────────────────────────────────
# TOKEN BADGE HELPER
# ─────────────────────────────────────────────

def token_badge(tok_type: str, value: str) -> str:
    """Return a coloured HTML badge for a token."""
    colour = TOKEN_COLOURS.get(tok_type, "#555")
    return (
        f'<span style="background:{colour}22;color:{colour};border:1px solid {colour}55;'
        f'border-radius:4px;padding:2px 8px;margin:2px;font-family:Courier New;'
        f'font-size:12px;display:inline-block;">'
        f'<b>{tok_type}</b> <span style="opacity:0.8">{_escape(value)}</span></span>'
    )