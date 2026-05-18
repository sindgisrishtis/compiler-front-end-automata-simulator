"""
diagrams.py
===========
Generates Graphviz source for DFA and PDA state diagrams.
Returns graphviz.Digraph objects that Streamlit can render.
"""

try:
    import graphviz
    HAS_GRAPHVIZ = True
except ImportError:
    HAS_GRAPHVIZ = False

from automata import DFAResult, PDAResult
from typing import Optional


# ─────────────────────────────────────────────
# COLOUR PALETTE
# ─────────────────────────────────────────────

PALETTE = {
    "start":   "#1a1a2e",
    "normal":  "#16213e",
    "accept":  "#0f3460",
    "reject":  "#e94560",
    "edge":    "#00d4ff",
    "font":    "white",
    "bg":      "transparent",
}


def _base_graph(name: str) -> "graphviz.Digraph":
    g = graphviz.Digraph(name=name, format="png")
    g.attr(
        bgcolor="transparent",
        fontcolor=PALETTE["font"],
        rankdir="LR",
        pad="0.3",
    )
    g.attr("node",
        style="filled",
        fontcolor=PALETTE["font"],
        fontname="Courier New",
        fontsize="11",
    )
    g.attr("edge",
        color=PALETTE["edge"],
        fontcolor=PALETTE["edge"],
        fontname="Courier New",
        fontsize="9",
    )
    return g


def build_dfa_diagram(result: DFAResult) -> Optional["graphviz.Digraph"]:
    """
    Build a Graphviz diagram for a single DFA run result.
    States are sized and coloured by role.
    """
    if not HAS_GRAPHVIZ:
        return None

    g = _base_graph(f"DFA_{result.token}")

    # Collect unique states in order
    seen = {}
    ordered = []
    for t in result.transitions:
        for s in (t.from_state, t.to_state):
            if s not in seen:
                seen[s] = True
                ordered.append(s)

    # Render nodes
    for s in ordered:
        if s == "q0":
            g.node(s, s, shape="circle", fillcolor="#1e3a5f", peripheries="2")
        elif s in ("q_accept",):
            g.node(s, s, shape="doublecircle", fillcolor="#0d7c3d")
        elif s in ("q_reject", "q_error"):
            g.node(s, s, shape="circle", fillcolor=PALETTE["reject"])
        else:
            g.node(s, s, shape="circle", fillcolor=PALETTE["normal"])

    # Invisible start arrow
    g.node("__start__", "", shape="none", width="0")
    g.edge("__start__", "q0", arrowhead="vee")

    # Render edges (deduplicate parallel edges with combined labels)
    edge_labels: dict = {}
    for t in result.transitions:
        key = (t.from_state, t.to_state)
        edge_labels.setdefault(key, [])
        if t.symbol not in edge_labels[key]:
            edge_labels[key].append(t.symbol)

    for (src, dst), labels in edge_labels.items():
        g.edge(src, dst, label=",".join(labels))

    return g


def build_pda_diagram(result: PDAResult) -> Optional["graphviz.Digraph"]:
    """
    Build a Graphviz diagram showing PDA states.
    """
    if not HAS_GRAPHVIZ:
        return None

    g = _base_graph("PDA")

    states = ["q_start", "q_push", "q_pop", "q_accept", "q_reject", "q_error"]
    colours = {
        "q_start":  "#1e3a5f",
        "q_push":   "#0f3460",
        "q_pop":    "#2d6a4f",
        "q_accept": "#0d7c3d",
        "q_reject": PALETTE["reject"],
        "q_error":  PALETTE["reject"],
    }
    labels = {
        "q_start":  "q₀\nSTART",
        "q_push":   "q₁\nPUSH",
        "q_pop":    "q₂\nPOP",
        "q_accept": "qₐ\nACCEPT",
        "q_reject": "q_r\nREJECT",
        "q_error":  "q_e\nERROR",
    }

    for s in states:
        shape = "doublecircle" if s in ("q_accept", "q_reject") else "circle"
        g.node(s, labels[s], shape=shape, fillcolor=colours[s])

    g.node("__start__", "", shape="none", width="0")
    g.edge("__start__", "q_start", arrowhead="vee")

    g.edge("q_start", "q_push",   label="open bracket\n(PUSH)")
    g.edge("q_push",  "q_push",   label="open bracket\n(PUSH)")
    g.edge("q_push",  "q_pop",    label="close bracket\n(POP)")
    g.edge("q_pop",   "q_push",   label="open bracket\n(PUSH)")
    g.edge("q_pop",   "q_pop",    label="close bracket\n(POP)")
    g.edge("q_pop",   "q_accept", label="EOF &\nstack empty")
    g.edge("q_push",  "q_reject", label="EOF &\nstack not empty")
    g.edge("q_push",  "q_error",  label="mismatch")
    g.edge("q_pop",   "q_error",  label="empty stack pop")

    return g


def build_architecture_diagram() -> Optional["graphviz.Digraph"]:
    """
    Build a compiler front-end architecture diagram.
    """
    if not HAS_GRAPHVIZ:
        return None

    g = graphviz.Digraph("Architecture", format="png")
    g.attr(bgcolor="transparent", rankdir="TD", pad="0.5", nodesep="0.7")
    g.attr("node",
        style="filled",
        fontcolor="white",
        fontname="Courier New",
        fontsize="12",
        shape="box",
        rounded="true",
    )
    g.attr("edge", color="#00d4ff", fontcolor="#00d4ff", fontname="Courier New")

    stages = [
        ("src",   "#1a1a2e", "📄 Source Code"),
        ("lex",   "#0f3460", "🔍 Lexical Analyser\n(DFA)"),
        ("tok",   "#16213e", "🏷  Token Stream"),
        ("par",   "#0f3460", "🔧 Syntax Validator\n(PDA / CFG)"),
        ("ast",   "#16213e", "🌳 Parse Tree / AST"),
        ("out",   "#0d7c3d", "✅ Compiler Output"),
        ("err",   "#e94560", "❌ Error Reporter"),
    ]

    for nid, col, lbl in stages:
        g.node(nid, lbl, fillcolor=col)

    g.edge("src", "lex", label="raw text")
    g.edge("lex", "tok", label="tokens")
    g.edge("tok", "par", label="token stream")
    g.edge("par", "ast", label="valid structure")
    g.edge("ast", "out", label="accepted")
    g.edge("lex", "err", label="lex error")
    g.edge("par", "err", label="syntax error")

    return g