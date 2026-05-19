"""
app.py
======
Smart Compiler Automata Simulation System
Design and Analysis of DFA and PDA for Lexical and Syntax Validation

Run:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from simulator import Simulator, SimulationReport
from automata import DFAEngine, PDAEngine
from lexer import Lexer
from utils import highlight_source, render_stack_html, token_badge, TOKEN_COLOURS
from diagrams import build_dfa_diagram, build_pda_diagram, build_architecture_diagram

try:
    import graphviz as gv
    HAS_GRAPHVIZ = True
except Exception:
    HAS_GRAPHVIZ = False


# ═══════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════

st.set_page_config(
    page_title="TOC Automata Simulator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ═══════════════════════════════════════════════
# GLOBAL CSS
# ═══════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600&display=swap');

/* ── Root theme ── */
:root {
    --bg-deep:    #0a0e1a;
    --bg-card:    #111827;
    --bg-panel:   #1a2236;
    --accent:     #00d4ff;
    --accent2:    #7c3aed;
    --success:    #10b981;
    --danger:     #ef4444;
    --text:       #e2e8f0;
    --muted:      #64748b;
    --border:     rgba(0,212,255,0.2);
}

/* ── Main background ── */
.stApp { background: var(--bg-deep); }
.main .block-container { max-width: 1400px; padding: 1.5rem 2rem; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0e1a 0%, #111827 100%);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { font-family: 'Share Tech Mono', monospace; }

/* ── Headings ── */
h1 { font-family: 'Orbitron', monospace !important; color: var(--accent) !important; letter-spacing: 2px; }
h2 { font-family: 'Orbitron', monospace !important; color: var(--text) !important; font-size: 1.1rem !important; }
h3 { font-family: 'Exo 2', sans-serif !important; color: var(--accent) !important; }

/* ── Cards ── */
.toc-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
}
.toc-card-accent {
    background: linear-gradient(135deg, #111827 0%, #1a2236 100%);
    border: 1px solid var(--accent);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 0 20px rgba(0,212,255,0.08);
}

/* ── Metric tiles ── */
.metric-tile {
    background: var(--bg-panel);
    border-radius: 10px;
    padding: 16px;
    text-align: center;
    border: 1px solid var(--border);
}
.metric-value {
    font-family: 'Orbitron', monospace;
    font-size: 2rem;
    color: var(--accent);
    line-height: 1;
}
.metric-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ── State chips ── */
.state-chip {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px;
    margin: 2px;
}

/* ── Verdict banners ── */
.verdict-accept {
    background: linear-gradient(90deg, rgba(16,185,129,0.15), transparent);
    border-left: 4px solid #10b981;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    font-family: 'Orbitron', monospace;
    color: #10b981;
    font-size: 1rem;
    letter-spacing: 1px;
}
.verdict-reject {
    background: linear-gradient(90deg, rgba(239,68,68,0.15), transparent);
    border-left: 4px solid #ef4444;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    font-family: 'Orbitron', monospace;
    color: #ef4444;
    font-size: 1rem;
    letter-spacing: 1px;
}

/* ── Transition table ── */
.trans-table { width: 100%; border-collapse: collapse; font-family: 'Share Tech Mono', monospace; font-size: 12px; }
.trans-table th { background: #1e3a5f; color: var(--accent); padding: 8px 12px; text-align: left; border-bottom: 2px solid var(--border); }
.trans-table td { padding: 6px 12px; border-bottom: 1px solid rgba(255,255,255,0.05); color: var(--text); }
.trans-table tr:hover td { background: rgba(0,212,255,0.05); }

/* ── Stack cell ── */
.stack-item {
    background: #0f3460;
    border: 1px solid var(--accent);
    border-radius: 4px;
    padding: 6px 16px;
    margin: 2px auto;
    text-align: center;
    font-family: 'Share Tech Mono', monospace;
    color: white;
    width: fit-content;
    min-width: 60px;
}
.stack-top { background: #7c3aed !important; border-color: #7c3aed !important; }

/* ── Info boxes ── */
.info-box {
    background: rgba(0,212,255,0.06);
    border: 1px solid rgba(0,212,255,0.3);
    border-radius: 8px;
    padding: 14px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px;
    color: var(--text);
    margin: 8px 0;
}

/* ── Sidebar nav button ── */
div[data-testid="stButton"] button {
    font-family: 'Share Tech Mono', monospace !important;
    letter-spacing: 1px;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab"] {
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px;
    color: var(--muted);
}
.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom-color: var(--accent) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════

if "report" not in st.session_state:
    st.session_state.report = None
if "source" not in st.session_state:
    st.session_state.source = ""


# ═══════════════════════════════════════════════
# SIDEBAR NAVIGATION
# ═══════════════════════════════════════════════

PAGES = {
    "🚀 Compiler Front-End":      "compiler",
    "🤖 TOC Automata Simulator":  "automata",
    "📘 Theory Reference":        "theory",
    "📊 Analysis Dashboard":      "dashboard",
}

with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:16px 0 24px;">
      <div style="font-family:'Orbitron',monospace;font-size:1.1rem;color:#00d4ff;letter-spacing:2px;">
        ◈ TOC SIM
      </div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:#64748b;margin-top:4px;">
        AUTOMATA SIMULATION SYSTEM
      </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("Navigation", list(PAGES.keys()), label_visibility="collapsed")
    active = PAGES[page]

    st.markdown("---")
    st.markdown("""
    <div style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:#64748b;padding:8px;">
    DFA · PDA · CFG · Regular Expressions<br>
    Lexical Analysis · Syntax Validation<br><br>
    <span style="color:#00d4ff;">Theory of Computation</span><br>
    Compiler Front-End Simulation
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.report:
        r: SimulationReport = st.session_state.report
        st.markdown("---")
        st.markdown("""<div style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:#64748b;">
        LAST RUN SUMMARY</div>""", unsafe_allow_html=True)
        lex_col = "#10b981" if r.lexically_valid else "#ef4444"
        syn_col = "#10b981" if r.syntactically_valid else "#ef4444"
        st.markdown(f"""
        <div style="font-family:'Share Tech Mono',monospace;font-size:0.7rem;padding:4px;">
        Tokens: <span style="color:#00d4ff;">{len(r.tokens)}</span><br>
        DFA Trans: <span style="color:#00d4ff;">{r.total_dfa_transitions}</span><br>
        PDA Ops: <span style="color:#00d4ff;">{len(r.pda_result.transitions)}</span><br>
        Lexical: <span style="color:{lex_col};">{'✓ OK' if r.lexically_valid else '✗ FAIL'}</span><br>
        Syntax: <span style="color:{syn_col};">{'✓ OK' if r.syntactically_valid else '✗ FAIL'}</span>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# HELPER: SAMPLE PROGRAMS
# ═══════════════════════════════════════════════

SAMPLES = {
    "✅ Valid: Variable & if": """\
int a = 10;

if(a > 5){
    a = a + 1;
}
""",
    "✅ Valid: For Loop": """\
int sum = 0;
for(int i = 0; i < 5; i = i + 1){
    sum = sum + i;
}
return sum;
""",
    "✅ Valid: Float & Return": """\
float pi = 3.14;
float area = pi * 5 * 5;
return area;
""",
    "❌ Invalid: Bad Identifier": """\
int 1abc = 10;
""",
    "❌ Invalid: Unclosed Paren": """\
if(a > 5{
    a = a + 1;
}
""",
    "❌ Invalid: Bracket Mismatch": """\
int a = (10 + 5];
""",
}


# ═══════════════════════════════════════════════
# PAGE 1: COMPILER FRONT-END
# ═══════════════════════════════════════════════

def page_compiler():

    st.markdown("""
    <h1>🚀 Compiler Front-End</h1>
    <p style="font-family:'Share Tech Mono',monospace;color:#64748b;font-size:0.8rem;">
    Lexical Analysis & Syntax Validation — Practical Mode
    </p>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2], gap="large")

    # ─────────────────────────────────────────────
    # LEFT PANEL
    # ─────────────────────────────────────────────

    with col_left:

        st.markdown("### 📝 Source Code Editor")

        # Sample selector
        sample_options = ["(write your own)"] + list(SAMPLES.keys())

        selected_sample = st.selectbox(
            "Load sample program:",
            sample_options
        )

        # Load selected sample automatically
        if selected_sample == "(write your own)":

            default_code = st.session_state.get(
                "source",
                "int a = 10;\n\nif(a > 5){\n    a = a + 1;\n}"
            )

        else:
            default_code = SAMPLES[selected_sample]

        # Editor
        source = st.text_area(
            "",
            value=default_code,
            height=240,
            key=f"editor_{selected_sample}"
        )

        # Analyse button
        run_col, _ = st.columns([1, 3])

        with run_col:
            run = st.button(
                "⚡ ANALYSE",
                use_container_width=True,
                type="primary"
            )

        # Run simulator
        if run and source.strip():

            sim = Simulator()

            report = sim.run(source)

            st.session_state.report = report
            st.session_state.source = source

    # ─────────────────────────────────────────────
    # RESULTS
    # ─────────────────────────────────────────────

    if st.session_state.get("report"):

        r: SimulationReport = st.session_state.report

        with col_right:

            # Verdict
            if r.lexically_valid and r.syntactically_valid:

                st.markdown(
                    '''
                    <div class="verdict-accept">
                    ✅ ACCEPTED — Lexically & Syntactically Valid
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    '''
                    <div class="verdict-reject">
                    ❌ REJECTED — Errors Detected
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

            st.write("")

            # Metrics
            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(
                    f'''
                    <div class="metric-tile">
                        <div class="metric-value">{len(r.tokens)}</div>
                        <div class="metric-label">Tokens</div>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

            with c2:

                err_count = len(r.parse_result.errors)

                st.markdown(
                    f'''
                    <div class="metric-tile">
                        <div class="metric-value" style="color:{"#ef4444" if err_count else "#10b981"}">
                            {err_count}
                        </div>
                        <div class="metric-label">Errors</div>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

            with c3:

                st.markdown(
                    f'''
                    <div class="metric-tile">
                        <div class="metric-value">{r.parse_result.statements_found}</div>
                        <div class="metric-label">Statements</div>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

            st.write("")

            # Errors
            if r.parse_result.errors:

                st.markdown("### 🔴 Syntax Errors")

                for e in r.parse_result.errors:

                    st.markdown(
                        f'''
                        <div style="
                            background:rgba(239,68,68,0.1);
                            border-left:3px solid #ef4444;
                            padding:8px 12px;
                            margin:4px 0;
                            border-radius:0 4px 4px 0;
                            font-family:Share Tech Mono,monospace;
                            font-size:12px;
                            color:#fca5a5;
                        ">
                        Line {e.line}: {e.message}
                        </div>
                        ''',
                        unsafe_allow_html=True
                    )

        # ─────────────────────────────────────────────
        # BOTTOM PANELS
        # ─────────────────────────────────────────────

        st.write("")

        tab1, tab2 = st.tabs([
            "🏷 Token Stream",
            "📊 Token Statistics"
        ])

        # TOKEN STREAM
        with tab1:

            badge_html = ""

            for tok in r.tokens:
                badge_html += token_badge(tok.type, tok.value) + " "

            st.markdown(
                f'<div style="line-height:2.2;">{badge_html}</div>',
                unsafe_allow_html=True
            )

            df = pd.DataFrame([
                {
                    "#": i + 1,
                    "Type": t.type,
                    "Value": t.value,
                    "Line": t.line,
                    "Column": t.column
                }
                for i, t in enumerate(r.tokens)
            ])

            st.dataframe(
                df,
                use_container_width=True,
                height=300,
                hide_index=True
            )

        # TOKEN STATISTICS
        with tab2:

            stats = r.token_stats

            if stats:

                df_stats = pd.DataFrame([
                    {
                        "Token Type": k,
                        "Count": v,
                        "Percentage": f"{100*v/max(sum(stats.values()),1):.1f}%"
                    }
                    for k, v in sorted(stats.items(), key=lambda x: -x[1])
                ])

                st.dataframe(
                    df_stats,
                    use_container_width=True,
                    hide_index=True
                )

                st.bar_chart(pd.Series(stats))

# ═══════════════════════════════════════════════
# PAGE 2: TOC AUTOMATA SIMULATOR
# ═══════════════════════════════════════════════

def page_automata():
    st.markdown("""
    <h1>🤖 TOC Automata Simulator</h1>
    <p style="font-family:'Share Tech Mono',monospace;color:#64748b;font-size:0.8rem;">
    DFA · PDA · State Transitions · Stack Operations — Theory Mode
    </p>
    """, unsafe_allow_html=True)

    if not st.session_state.report:
        st.markdown("""
        <div class="info-box">
        ⚠ No analysis run yet.<br>
        Go to <b>🚀 Compiler Front-End</b>, enter code and press ANALYSE first.
        </div>
        """, unsafe_allow_html=True)
        return

    r: SimulationReport = st.session_state.report

    dfa_tab, pda_tab = st.tabs(["⚙ DFA Simulation", "📦 PDA Simulation"])

    # ─────────────────────────────────────────────────
    # DFA TAB
    # ─────────────────────────────────────────────────
    with dfa_tab:
        st.markdown("### Deterministic Finite Automaton — Token-Level Simulation")

        col_sel, col_info = st.columns([2, 3], gap="large")

        with col_sel:
            token_labels = [f"[{i+1}] {dr.token_type}: {dr.token}" for i, dr in enumerate(r.dfa_results)]
            sel_idx = st.selectbox("Select token to inspect:", range(len(token_labels)),
                                    format_func=lambda i: token_labels[i])

        dr = r.dfa_results[sel_idx]

        with col_info:
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(f'<div class="metric-tile"><div class="metric-value" style="font-size:1.4rem">{dr.token}</div><div class="metric-label">Token</div></div>', unsafe_allow_html=True)
            with c2:
                col = TOKEN_COLOURS.get(dr.token_type, "#888")
                st.markdown(f'<div class="metric-tile"><div class="metric-value" style="font-size:1.1rem;color:{col}">{dr.token_type}</div><div class="metric-label">Type</div></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="metric-tile"><div class="metric-value" style="font-size:1.4rem">{len(dr.transitions)}</div><div class="metric-label">Transitions</div></div>', unsafe_allow_html=True)
            with c4:
                v_col = "#10b981" if dr.accepted else "#ef4444"
                v_txt = "ACCEPT" if dr.accepted else "REJECT"
                st.markdown(f'<div class="metric-tile"><div class="metric-value" style="font-size:1rem;color:{v_col}">{v_txt}</div><div class="metric-label">Final State</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        d1, d2 = st.columns([3, 2], gap="large")

        with d1:
            st.markdown("#### 📋 DFA Transition Trace")
            #st.markdown('<div class="toc-card">', unsafe_allow_html=True)

            # Execution trace text
            trace_html = '<div style="font-family:Share Tech Mono,monospace;font-size:12px;line-height:2;">'
            for t in dr.transitions:
                arrow = "──→"
                sym_html = f'<span style="color:#ffd700;">{t.symbol}</span>'
                from_col = "#1e90ff"
                to_col = "#10b981" if "accept" in t.to_state else ("#ef4444" if "reject" in t.to_state or "error" in t.to_state else "#9cdcfe")
                trace_html += (
                    f'<span style="color:{from_col}">{t.from_state}</span> '
                    f'<span style="color:#64748b">{arrow}</span> '
                    f'[{sym_html}] '
                    f'<span style="color:#64748b">{arrow}</span> '
                    f'<span style="color:{to_col}">{t.to_state}</span><br>'
                )
            trace_html += '</div>'
            st.markdown(trace_html, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Transition table
            st.markdown("#### 📊 DFA Transition Table")
            rows = [{"Step": t.step, "From State": t.from_state, "Input Symbol": t.symbol, "To State": t.to_state}
                    for t in dr.transitions]
            df_dfa = pd.DataFrame(rows)
            st.dataframe(df_dfa, use_container_width=True, hide_index=True)

        with d2:
            st.markdown("#### 🗺 State Diagram")
            if HAS_GRAPHVIZ:
                diagram = build_dfa_diagram(dr)
                if diagram:
                    try:
                        st.graphviz_chart(diagram.source, use_container_width=True)
                    except Exception:
                        st.info("Diagram rendering unavailable.")
            else:
                # Text-based state diagram fallback
                st.markdown('<div class="toc-card">', unsafe_allow_html=True)
                states = dr.states_visited
                for i, s in enumerate(states):
                    col_s = "#10b981" if "accept" in s else ("#ef4444" if "reject" in s or "error" in s else ("#ffd700" if s == "q0" else "#9cdcfe"))
                    st.markdown(f'<div style="font-family:Share Tech Mono,monospace;color:{col_s};padding:4px 0;">'
                                f'{"→ " if i == 0 else "↓  "}<b>{s}</b></div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # State path
            st.markdown("#### 🧭 State Path")
            path_html = ""
            for i, s in enumerate(dr.states_visited):
                if "accept" in s:
                    colour = "#10b981"
                elif "reject" in s or "error" in s:
                    colour = "#ef4444"
                elif s == "q0":
                    colour = "#ffd700"
                else:
                    colour = "#9cdcfe"
                path_html += f'<span class="state-chip" style="background:{colour}22;color:{colour};border:1px solid {colour}55;">{s}</span>'
                if i < len(dr.states_visited) - 1:
                    path_html += '<span style="color:#64748b;font-size:10px;"> → </span>'
            st.markdown(f'<div style="line-height:2.5;">{path_html}</div>', unsafe_allow_html=True)

        # All tokens DFA summary
        #st.markdown("<br>")
        st.markdown("#### 📋 All Tokens — DFA Summary")
        all_rows = []
        for dr_ in r.dfa_results:
            all_rows.append({
                "Token": dr_.token,
                "Type": dr_.token_type,
                "States": len(dr_.states_visited),
                "Transitions": len(dr_.transitions),
                "Final State": dr_.final_state,
                "Accepted": "✅" if dr_.accepted else "❌",
            })
        st.dataframe(pd.DataFrame(all_rows), use_container_width=True, hide_index=True)

    # ─────────────────────────────────────────────────
    # PDA TAB
    # ─────────────────────────────────────────────────
    with pda_tab:
        pda = r.pda_result
        st.markdown("### Pushdown Automaton — Bracket/Delimiter Stack Simulation")

        # Summary metrics
        c1, c2, c3, c4, c5 = st.columns(5)
        metrics = [
            (len(pda.transitions), "PDA Steps", "#00d4ff"),
            (pda.total_pushes, "PUSH Ops", "#7c3aed"),
            (pda.total_pops, "POP Ops", "#10b981"),
            (pda.max_stack_depth, "Max Stack Depth", "#f59e0b"),
            ("ACCEPT" if pda.accepted else "REJECT", "Verdict", "#10b981" if pda.accepted else "#ef4444"),
        ]
        for col, (val, lbl, clr) in zip([c1, c2, c3, c4, c5], metrics):
            with col:
                st.markdown(f'<div class="metric-tile"><div class="metric-value" style="color:{clr};font-size:1.4rem">{val}</div><div class="metric-label">{lbl}</div></div>', unsafe_allow_html=True)

        if pda.accepted:
            st.markdown('<div class="verdict-accept" style="margin-top:12px;">✅ PDA ACCEPTED — All brackets balanced</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="verdict-reject" style="margin-top:12px;">❌ PDA REJECTED — Bracket imbalance detected</div>', unsafe_allow_html=True)

        #st.markdown("<br>")
        p1, p2, p3 = st.columns([3, 2, 2], gap="large")

        with p1:
            st.markdown("#### 📋 PDA Execution Trace")
            rows_pda = []
            for t in pda.transitions:
                stack_str = " ".join(t.stack_after) if t.stack_after else "∅"
                rows_pda.append({
                    "Step": t.step,
                    "Symbol": t.symbol,
                    "Action": t.action,
                    "Stack After": stack_str,
                    "State": t.state,
                })
            df_pda = pd.DataFrame(rows_pda)
            st.dataframe(df_pda, use_container_width=True, hide_index=True, height=380)

        with p2:
            st.markdown("#### 🗺 PDA Diagram")
            if HAS_GRAPHVIZ:
                pda_diag = build_pda_diagram(pda)
                if pda_diag:
                    try:
                        st.graphviz_chart(pda_diag.source, use_container_width=True)
                    except Exception:
                        st.info("Diagram unavailable")
            else:
                st.markdown("""
                <div class="toc-card" style="font-family:Share Tech Mono,monospace;font-size:12px;line-height:2;">
                <span style="color:#ffd700">q₀ START</span><br>
                ↓ open bracket<br>
                <span style="color:#00d4ff">q₁ PUSH</span><br>
                ↓ close bracket<br>
                <span style="color:#10b981">q₂ POP</span><br>
                ↓ EOF & stack empty<br>
                <span style="color:#10b981">qₐ ACCEPT</span><br>
                ↓ stack not empty<br>
                <span style="color:#ef4444">q_r REJECT</span>
                </div>
                """, unsafe_allow_html=True)

        with p3:
            st.markdown("#### 📦 Final Stack State")
            if pda.final_stack:
                for i, item in enumerate(reversed(pda.final_stack)):
                    cls = "stack-top" if i == 0 else ""
                    st.markdown(f'<div class="stack-item {cls}">{item}{"  ← TOP" if i == 0 else ""}</div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align:center;font-family:Share Tech Mono,monospace;color:#64748b;font-size:11px;margin-top:6px;">⊥ BOTTOM OF STACK</div>', unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="text-align:center;padding:32px;color:#10b981;font-family:Share Tech Mono,monospace;font-size:13px;">
                ∅<br>Stack Empty<br><span style="font-size:10px;color:#64748b;">⊥ Bottom of Stack</span>
                </div>
                """, unsafe_allow_html=True)

            #st.markdown("<br>")
            st.markdown("#### 📊 PDA Transition Table")
            pda_tbl = []
            for t in pda.transitions:
                pda_tbl.append({
                    "State": t.state,
                    "Input": t.symbol,
                    "Stack Top": t.stack_before[-1] if t.stack_before else "∅",
                    "Action": t.action[:40] + "…" if len(t.action) > 40 else t.action,
                    "New Stack Top": t.stack_after[-1] if t.stack_after else "∅",
                })
            st.dataframe(pd.DataFrame(pda_tbl), use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════
# PAGE 3: THEORY REFERENCE
# ═══════════════════════════════════════════════

def page_theory():
    st.markdown("""
    <h1>📘 Theory Reference</h1>
    <p style="font-family:'Share Tech Mono',monospace;color:#64748b;font-size:0.8rem;">
    Formal Language Theory · Automata · Compiler Architecture
    </p>
    """, unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs(["DFA", "PDA", "Regular Expr & CFG", "Compiler Architecture"])

    # ── DFA ───────────────────────────────────────────
    with t1:
        c_l, c_r = st.columns(2, gap="large")
        with c_l:
            st.markdown("""
            <div class="toc-card-accent">
            <h3>Deterministic Finite Automaton (DFA)</h3>
            <p style="font-family:'Share Tech Mono',monospace;font-size:12px;color:#94a3b8;line-height:1.8;">
            A DFA is a 5-tuple M = (Q, Σ, δ, q₀, F) where:<br><br>
            &nbsp;• <b style="color:#00d4ff;">Q</b> — finite set of states<br>
            &nbsp;• <b style="color:#00d4ff;">Σ</b> — finite input alphabet<br>
            &nbsp;• <b style="color:#00d4ff;">δ: Q × Σ → Q</b> — transition function<br>
            &nbsp;• <b style="color:#00d4ff;">q₀ ∈ Q</b> — start state<br>
            &nbsp;• <b style="color:#00d4ff;">F ⊆ Q</b> — set of accepting states<br><br>
            A string w is accepted if δ*(q₀, w) ∈ F
            </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="toc-card">
            <h3>DFA in Lexical Analysis</h3>
            <p style="font-family:'Share Tech Mono',monospace;font-size:12px;color:#94a3b8;line-height:1.8;">
            The lexer (scanner) in a compiler is essentially a DFA.<br><br>
            &nbsp;• Each token type corresponds to a regular language<br>
            &nbsp;• The DFA transitions character-by-character<br>
            &nbsp;• On reaching an accept state → token recognised<br>
            &nbsp;• On reaching a dead/reject state → lexical error<br><br>
            <b style="color:#00d4ff;">Kleene's Theorem</b> guarantees that every regular<br>
            language can be recognised by a finite automaton.
            </p>
            </div>
            """, unsafe_allow_html=True)

        with c_r:
            st.markdown("""
            <div class="toc-card">
            <h3>DFA Token Recognition Examples</h3>
            </div>
            """, unsafe_allow_html=True)

            dfa_engine = DFAEngine()
            for tok_val in ["int", "sum", "3.14", "123", "==", "+"]:
                dr = dfa_engine.simulate(tok_val)
                trace = " → ".join([t.from_state for t in dr.transitions[:3]])
                if dr.transitions:
                    trace += f" → {dr.transitions[-1].to_state}"
                col_t = TOKEN_COLOURS.get(dr.token_type, "#888")
                acc_icon = "✅" if dr.accepted else "❌"
                st.markdown(f"""
                <div style="background:#111827;border:1px solid rgba(0,212,255,0.15);border-radius:8px;padding:10px 14px;margin-bottom:8px;">
                  <span style="font-family:Share Tech Mono,monospace;font-size:13px;">
                    <b style="color:#ffd700;">TOKEN:</b> <span style="color:white;">{tok_val}</span>
                    &nbsp;&nbsp;<span style="background:{col_t}22;color:{col_t};border:1px solid {col_t}55;border-radius:4px;padding:1px 8px;font-size:11px;">{dr.token_type}</span>
                    &nbsp;{acc_icon}<br>
                    <span style="color:#64748b;font-size:11px;">Path: {trace}</span>
                  </span>
                </div>
                """, unsafe_allow_html=True)

    # ── PDA ───────────────────────────────────────────
    with t2:
        c_l, c_r = st.columns(2, gap="large")
        with c_l:
            st.markdown("""
            <div class="toc-card-accent">
            <h3>Pushdown Automaton (PDA)</h3>
            <p style="font-family:'Share Tech Mono',monospace;font-size:12px;color:#94a3b8;line-height:1.8;">
            A PDA is a 7-tuple M = (Q, Σ, Γ, δ, q₀, Z₀, F) where:<br><br>
            &nbsp;• <b style="color:#00d4ff;">Q</b> — finite set of states<br>
            &nbsp;• <b style="color:#00d4ff;">Σ</b> — input alphabet<br>
            &nbsp;• <b style="color:#00d4ff;">Γ</b> — stack alphabet<br>
            &nbsp;• <b style="color:#00d4ff;">δ: Q × (Σ∪{ε}) × Γ → P(Q × Γ*)</b><br>
            &nbsp;• <b style="color:#00d4ff;">q₀</b> — start state<br>
            &nbsp;• <b style="color:#00d4ff;">Z₀</b> — initial stack symbol<br>
            &nbsp;• <b style="color:#00d4ff;">F</b> — accepting states<br><br>
            Power: recognises <b style="color:#7c3aed;">Context-Free Languages</b>
            </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="toc-card">
            <h3>PDA in Syntax Validation</h3>
            <p style="font-family:'Share Tech Mono',monospace;font-size:12px;color:#94a3b8;line-height:1.8;">
            The syntax analyser (parser) in a compiler uses<br>
            a PDA to recognise context-free languages.<br><br>
            &nbsp;• Opening brackets are PUSHed onto the stack<br>
            &nbsp;• Closing brackets cause a POP + match check<br>
            &nbsp;• On empty stack at EOF → balanced → ACCEPT<br>
            &nbsp;• Non-empty stack or mismatch → REJECT<br><br>
            <b style="color:#00d4ff;">Chomsky's Hierarchy:</b><br>
            Regular (DFA) ⊂ Context-Free (PDA) ⊂ Context-Sensitive ⊂ Recursively Enumerable
            </p>
            </div>
            """, unsafe_allow_html=True)

        with c_r:
            st.markdown("""
            <div class="toc-card">
            <h3>PDA Stack Simulation Example</h3>
            <p style="font-family:'Share Tech Mono',monospace;font-size:12px;color:#94a3b8;">Input: if(a > 5){ a = a + 1; }</p>
            </div>
            """, unsafe_allow_html=True)

            pda_engine = PDAEngine()
            ex_pda = pda_engine.simulate("if(a > 5){ a = a + 1; }")
            for step in ex_pda.transitions:
                state_col = "#10b981" if "accept" in step.state else ("#ef4444" if "error" in step.state or "reject" in step.state else ("#7c3aed" if "push" in step.state else "#00d4ff"))
                stack_vis = " ".join(step.stack_after) if step.stack_after else "∅"
                st.markdown(f"""
                <div style="background:#111827;border-left:3px solid {state_col};padding:8px 12px;margin-bottom:6px;border-radius:0 6px 6px 0;">
                  <span style="font-family:Share Tech Mono,monospace;font-size:11px;">
                    <b style="color:#ffd700;">READ:</b> <span style="color:white;">'{step.symbol}'</span>
                    &nbsp;&nbsp;<span style="color:{state_col}">{step.state}</span><br>
                    <span style="color:#64748b;">{step.action}</span><br>
                    <b style="color:#64748b;">Stack:</b> <span style="color:#9cdcfe;">[{stack_vis}]</span>
                  </span>
                </div>
                """, unsafe_allow_html=True)

    # ── Regular Expr & CFG ────────────────────────────
    with t3:
        c_l, c_r = st.columns(2, gap="large")
        with c_l:
            st.markdown("""
            <div class="toc-card-accent">
            <h3>Regular Expressions</h3>
            <p style="font-family:'Share Tech Mono',monospace;font-size:12px;color:#94a3b8;line-height:2;">
            Regular expressions define <b style="color:#00d4ff;">regular languages</b> —<br>
            the class of languages recognised by DFAs.<br><br>
            Token patterns used in this system:<br><br>
            </p>
            </div>
            """, unsafe_allow_html=True)

            regex_table = pd.DataFrame([
                {"Token Type": "KEYWORD",    "Pattern": r"\b(int|float|if|...)\b",   "Example": "int, if, return"},
                {"Token Type": "IDENTIFIER", "Pattern": r"[A-Za-z_][A-Za-z0-9_]*",  "Example": "sum, myVar, _x"},
                {"Token Type": "INTEGER",    "Pattern": r"\b\d+\b",                  "Example": "0, 42, 100"},
                {"Token Type": "FLOAT",      "Pattern": r"\b\d+\.\d+\b",             "Example": "3.14, 2.0"},
                {"Token Type": "STRING",     "Pattern": r'"[^"\n]*"',               "Example": '"hello"'},
                {"Token Type": "OPERATOR",   "Pattern": r"==|!=|<=|>=|[+\-*/=<>!]", "Example": "+, ==, >="},
                {"Token Type": "SYMBOL",     "Pattern": r"[(){}\[\];,]",             "Example": "(, {, ;"},
            ])
            st.dataframe(regex_table, use_container_width=True, hide_index=True)

        with c_r:
            st.markdown("""
            <div class="toc-card-accent">
            <h3>Context-Free Grammar (CFG)</h3>
            <p style="font-family:'Share Tech Mono',monospace;font-size:12px;color:#94a3b8;line-height:2;">
            A CFG is a 4-tuple G = (V, T, P, S) where:<br>
            &nbsp;• <b style="color:#00d4ff;">V</b> = non-terminals (variables)<br>
            &nbsp;• <b style="color:#00d4ff;">T</b> = terminals (tokens)<br>
            &nbsp;• <b style="color:#00d4ff;">P</b> = production rules<br>
            &nbsp;• <b style="color:#00d4ff;">S</b> = start symbol<br><br>
            Sample grammar for this system:
            </p>
            </div>
            """, unsafe_allow_html=True)

            st.code("""
Program    → Statement*
Statement  → Declaration | IfStmt | ForStmt | ReturnStmt
Declaration→ Type Identifier '=' Expr ';'
IfStmt     → 'if' '(' Expr ')' Block
ForStmt    → 'for' '(' Stmt Expr ';' Stmt ')' Block
Block      → '{' Statement* '}'
Expr       → Expr Op Expr | Identifier | Number
Type       → 'int' | 'float' | 'char' | 'void'
            """, language="text")

    # ── Compiler Architecture ─────────────────────────
    with t4:
        st.markdown("""
        <div class="toc-card-accent">
        <h3>Compiler Front-End Architecture</h3>
        <p style="font-family:'Share Tech Mono',monospace;font-size:12px;color:#94a3b8;">
        Mapping of Theory of Computation to compiler implementation:
        </p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2, gap="large")
        with c1:
            if HAS_GRAPHVIZ:
                arch = build_architecture_diagram()
                if arch:
                    try:
                        st.graphviz_chart(arch.source, use_container_width=True)
                    except Exception:
                        pass
            st.markdown("""
            <div class="toc-card">
            <p style="font-family:'Share Tech Mono',monospace;font-size:12px;color:#94a3b8;line-height:2;">
            <b style="color:#00d4ff;">Stage 1 — Lexical Analysis (DFA):</b><br>
            &nbsp;Reads characters, groups into tokens using DFA.<br>
            &nbsp;Regular expressions define token patterns.<br><br>
            <b style="color:#7c3aed;">Stage 2 — Syntax Analysis (PDA):</b><br>
            &nbsp;Validates token stream against CFG.<br>
            &nbsp;PDA stack manages nested structure.<br><br>
            <b style="color:#10b981;">Stage 3 — Semantic Analysis:</b><br>
            &nbsp;Type checking, scope resolution (beyond TOC scope).
            </p>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown("""
            <div class="toc-card">
            <h3>Chomsky Hierarchy</h3>
            <table style="width:100%;font-family:Share Tech Mono,monospace;font-size:11px;border-collapse:collapse;">
            <tr style="border-bottom:1px solid rgba(0,212,255,0.2);">
              <th style="color:#00d4ff;padding:6px;">Type</th>
              <th style="color:#00d4ff;padding:6px;">Grammar</th>
              <th style="color:#00d4ff;padding:6px;">Automaton</th>
              <th style="color:#00d4ff;padding:6px;">Compiler Use</th>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
              <td style="color:#94a3b8;padding:6px;">Type 3</td>
              <td style="color:#94a3b8;padding:6px;">Regular</td>
              <td style="color:#9cdcfe;padding:6px;">DFA / NFA</td>
              <td style="color:#94a3b8;padding:6px;">Lexer (Tokens)</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
              <td style="color:#94a3b8;padding:6px;">Type 2</td>
              <td style="color:#94a3b8;padding:6px;">Context-Free</td>
              <td style="color:#7c3aed;padding:6px;">PDA</td>
              <td style="color:#94a3b8;padding:6px;">Parser (Syntax)</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
              <td style="color:#94a3b8;padding:6px;">Type 1</td>
              <td style="color:#94a3b8;padding:6px;">Context-Sensitive</td>
              <td style="color:#f59e0b;padding:6px;">LBA</td>
              <td style="color:#94a3b8;padding:6px;">Semantics</td>
            </tr>
            <tr>
              <td style="color:#94a3b8;padding:6px;">Type 0</td>
              <td style="color:#94a3b8;padding:6px;">Unrestricted</td>
              <td style="color:#ef4444;padding:6px;">Turing Machine</td>
              <td style="color:#94a3b8;padding:6px;">General Computation</td>
            </tr>
            </table>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PAGE 4: ANALYSIS DASHBOARD
# ═══════════════════════════════════════════════

def page_dashboard():
    st.markdown("""
    <h1>📊 Analysis Dashboard</h1>
    <p style="font-family:'Share Tech Mono',monospace;color:#64748b;font-size:0.8rem;">
    Aggregate Metrics · Charts · Automata Performance
    </p>
    """, unsafe_allow_html=True)

    if not st.session_state.report:
        st.markdown("""
        <div class="info-box">
        ⚠ No analysis run yet — go to 🚀 Compiler Front-End and run an analysis first.
        </div>
        """, unsafe_allow_html=True)
        return

    r: SimulationReport = st.session_state.report

    # ── Top KPIs ───────────────────────────────────────
    cols = st.columns(8)
    kpis = [
        ("Total Tokens",     len(r.tokens),                       "#00d4ff"),
        ("Keywords",         r.token_stats.get("KEYWORD", 0),     "#569cd6"),
        ("Identifiers",      r.token_stats.get("IDENTIFIER", 0),  "#9cdcfe"),
        ("Numbers",          r.token_stats.get("NUMBER", 0) + r.token_stats.get("FLOAT", 0), "#b5cea8"),
        ("Operators",        r.token_stats.get("OPERATOR", 0),    "#d4d4d4"),
        ("Syntax Errors",    len(r.parse_result.errors),          "#ef4444" if r.parse_result.errors else "#10b981"),
        ("DFA Transitions",  r.total_dfa_transitions,             "#7c3aed"),
        ("PDA Operations",   len(r.pda_result.transitions),       "#f59e0b"),
    ]
    for col, (label, value, colour) in zip(cols, kpis):
        with col:
            st.markdown(
                f'<div class="metric-tile"><div class="metric-value" style="color:{colour};font-size:1.5rem">{value}</div>'
                f'<div class="metric-label">{label}</div></div>',
                unsafe_allow_html=True
            )

    #st.markdown("<br>")

    # ── Charts ─────────────────────────────────────────
    c1, c2, c3 = st.columns(3, gap="large")

    with c1:
        st.markdown("#### Token Distribution")
        if r.token_stats:
            df_tok = pd.DataFrame.from_dict(r.token_stats, orient='index', columns=['Count'])
            df_tok = df_tok.sort_values('Count', ascending=False)
            st.bar_chart(df_tok)

    with c2:
        st.markdown("#### DFA — Transitions Per Token")
        dfa_counts = {dr.token: len(dr.transitions) for dr in r.dfa_results}
        # Show top 15 tokens by transition count
        top15 = dict(sorted(dfa_counts.items(), key=lambda x: -x[1])[:15])
        df_dfa_c = pd.DataFrame.from_dict(top15, orient='index', columns=['Transitions'])
        st.bar_chart(df_dfa_c)

    with c3:
        st.markdown("#### PDA — Stack Depth Over Time")
        depths = []
        d = 0
        for t in r.pda_result.transitions:
            d = len(t.stack_after)
            depths.append(d)
        if depths:
            df_depth = pd.DataFrame({"Stack Depth": depths})
            st.line_chart(df_depth)

    #st.markdown("<br>")
    c4, c5 = st.columns(2, gap="large")

    with c4:
        st.markdown("#### DFA Token Type Acceptance")
        accepted = sum(1 for dr in r.dfa_results if dr.accepted)
        rejected = len(r.dfa_results) - accepted
        df_acc = pd.DataFrame({"Status": ["Accepted", "Rejected"], "Count": [accepted, rejected]})
        st.dataframe(df_acc, hide_index=True, use_container_width=True)

        #st.markdown("<br>")
        st.markdown("#### Automata Complexity Summary")
        complexity = pd.DataFrame([
            {"Metric": "Unique DFA States Visited",     "Value": r.total_dfa_states},
            {"Metric": "Total DFA Transitions",         "Value": r.total_dfa_transitions},
            {"Metric": "PDA Total Push Operations",     "Value": r.pda_result.total_pushes},
            {"Metric": "PDA Total Pop Operations",      "Value": r.pda_result.total_pops},
            {"Metric": "PDA Max Stack Depth",           "Value": r.pda_result.max_stack_depth},
            {"Metric": "Total PDA Steps",               "Value": len(r.pda_result.transitions)},
            {"Metric": "Syntax Errors",                 "Value": len(r.parse_result.errors)},
            {"Metric": "Warnings",                      "Value": len(r.parse_result.warnings)},
        ])
        st.dataframe(complexity, hide_index=True, use_container_width=True)

    with c5:
        st.markdown("#### Token Type Breakdown (Full Table)")
        rows = []
        for dr in r.dfa_results:
            rows.append({
                "Token": dr.token,
                "Type": dr.token_type,
                "DFA States": len(dr.states_visited),
                "Transitions": len(dr.transitions),
                "Accepted": "✅" if dr.accepted else "❌",
            })
        df_full = pd.DataFrame(rows)
        st.dataframe(df_full, hide_index=True, use_container_width=True, height=400)


# ═══════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════

if active == "compiler":
    page_compiler()
elif active == "automata":
    page_automata()
elif active == "theory":
    page_theory()
elif active == "dashboard":
    page_dashboard()