"""
automata.py
===========
Core automata simulation engines for DFA and PDA.
Implements dynamic (non-hardcoded) state machine simulation.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Set


# ─────────────────────────────────────────────
# DATA CLASSES
# ─────────────────────────────────────────────

@dataclass
class DFATransition:
    """Represents a single DFA transition step."""
    from_state: str
    symbol: str
    to_state: str
    step: int


@dataclass
class DFAResult:
    """Result of running a token through the DFA."""
    token: str
    token_type: str
    transitions: List[DFATransition]
    final_state: str
    accepted: bool
    states_visited: List[str]


@dataclass
class PDATransition:
    """Represents a single PDA transition step."""
    step: int
    symbol: str
    action: str           # PUSH / POP / READ
    stack_before: List[str]
    stack_after: List[str]
    state: str


@dataclass
class PDAResult:
    """Result of running input through the PDA."""
    input_string: str
    transitions: List[PDATransition]
    final_stack: List[str]
    accepted: bool
    max_stack_depth: int
    total_pushes: int
    total_pops: int


# ─────────────────────────────────────────────
# DFA ENGINE
# ─────────────────────────────────────────────

class DFAEngine:
    """
    Dynamic DFA simulation engine.
    Recognises token categories by simulating character-level transitions.

    States:
        q0  → start
        q1  → reading letters / identifier-in-progress
        q2  → keyword candidate (after first letter)
        q3  → number (digit seen)
        q4  → float (dot after digit)
        q5  → float-fraction
        q6  → string (inside quotes)
        q7  → operator / symbol
        q_accept → accept
        q_reject → reject
    """

    KEYWORDS: Set[str] = {
        "int", "float", "char", "void", "if", "else",
        "for", "while", "do", "return", "break", "continue",
        "switch", "case", "default", "struct", "typedef"
    }

    OPERATORS: Set[str] = {
        "+", "-", "*", "/", "%", "=", "==", "!=",
        "<", ">", "<=", ">=", "&&", "||", "!", "++", "--",
        "+=", "-=", "*=", "/="
    }

    SYMBOLS: Set[str] = {
        "(", ")", "{", "}", "[", "]", ";", ",", ".", ":"
    }

    def simulate(self, token: str) -> DFAResult:
        """Simulate DFA on a single token and return full trace."""
        transitions: List[DFATransition] = []
        states_visited: List[str] = ["q0"]
        current_state = "q0"
        step = 0

        if not token:
            return DFAResult(token, "UNKNOWN", [], "q_reject", False, ["q0"])

        # ── Operators ──────────────────────────────────────
        if token in self.OPERATORS:
            for i, ch in enumerate(token):
                next_state = f"q_op{i+1}"
                transitions.append(DFATransition(current_state, ch, next_state, step))
                states_visited.append(next_state)
                current_state = next_state
                step += 1
            final = "q_accept"
            transitions.append(DFATransition(current_state, "ε", final, step))
            states_visited.append(final)
            return DFAResult(token, "OPERATOR", transitions, final, True, states_visited)

        # ── Symbols ────────────────────────────────────────
        if token in self.SYMBOLS:
            next_state = "q_sym1"
            transitions.append(DFATransition("q0", token, next_state, 0))
            states_visited.append(next_state)
            final = "q_accept"
            transitions.append(DFATransition(next_state, "ε", final, 1))
            states_visited.append(final)
            return DFAResult(token, "SYMBOL", transitions, final, True, states_visited)

        # ── String literal ─────────────────────────────────
        if len(token) >= 2 and token[0] == '"' and token[-1] == '"':
            current_state = "q0"
            for i, ch in enumerate(token):
                if i == 0:
                    ns = "q_str_open"
                elif i == len(token) - 1:
                    ns = "q_str_close"
                else:
                    ns = "q_str_body"
                transitions.append(DFATransition(current_state, ch, ns, i))
                states_visited.append(ns)
                current_state = ns
            final = "q_accept"
            transitions.append(DFATransition(current_state, "ε", final, len(token)))
            states_visited.append(final)
            return DFAResult(token, "STRING", transitions, final, True, states_visited)

        # ── Number / Float ─────────────────────────────────
        is_number = token.lstrip('-').isdigit()
        is_float = False
        try:
            float(token)
            if '.' in token:
                is_float = True
            elif not token.lstrip('-').isdigit():
                is_float = False
        except ValueError:
            pass

        if is_number or is_float:
            tok_type = "FLOAT" if is_float else "NUMBER"
            current_state = "q0"
            for i, ch in enumerate(token):
                if ch.isdigit():
                    ns = "q_num" if not is_float else ("q_frac" if '.' in token[:i] else "q_num")
                elif ch == '.':
                    ns = "q_dot"
                elif ch == '-' and i == 0:
                    ns = "q_sign"
                else:
                    ns = "q_reject"
                transitions.append(DFATransition(current_state, ch, ns, i))
                states_visited.append(ns)
                current_state = ns
            final = "q_accept" if current_state != "q_reject" else "q_reject"
            transitions.append(DFATransition(current_state, "ε", final, len(token)))
            states_visited.append(final)
            return DFAResult(token, tok_type, transitions, final, current_state != "q_reject", states_visited)

        # ── Identifier / Keyword ───────────────────────────
        if token[0].isalpha() or token[0] == '_':
            valid = all(c.isalnum() or c == '_' for c in token)
            current_state = "q0"
            for i, ch in enumerate(token):
                if i == 0:
                    ns = "q_id1"
                else:
                    ns = "q_id_cont"
                transitions.append(DFATransition(current_state, ch, ns, i))
                states_visited.append(ns)
                current_state = ns

            tok_type = "KEYWORD" if token in self.KEYWORDS else "IDENTIFIER"
            if valid:
                final = "q_accept"
                transitions.append(DFATransition(current_state, "ε", final, len(token)))
                states_visited.append(final)
                return DFAResult(token, tok_type, transitions, final, True, states_visited)
            else:
                final = "q_reject"
                transitions.append(DFATransition(current_state, "ε", final, len(token)))
                states_visited.append(final)
                return DFAResult(token, "UNKNOWN", transitions, final, False, states_visited)

        # ── Unknown ────────────────────────────────────────
        transitions.append(DFATransition("q0", token[0], "q_reject", 0))
        states_visited.append("q_reject")
        return DFAResult(token, "UNKNOWN", transitions, "q_reject", False, states_visited)

    def get_transition_table(self, token: str) -> Dict:
        """Return structured transition table for a token."""
        result = self.simulate(token)
        rows = []
        for t in result.transitions:
            rows.append({
                "Step": t.step,
                "From State": t.from_state,
                "Input Symbol": t.symbol,
                "To State": t.to_state
            })
        return {
            "token": token,
            "token_type": result.token_type,
            "accepted": result.accepted,
            "final_state": result.final_state,
            "rows": rows
        }


# ─────────────────────────────────────────────
# PDA ENGINE
# ─────────────────────────────────────────────

BRACKET_PAIRS: Dict[str, str] = {
    ')': '(',
    '}': '{',
    ']': '['
}

OPEN_BRACKETS: Set[str] = {'(', '{', '['}
CLOSE_BRACKETS: Set[str] = {')', '}', ']'}


class PDAEngine:
    """
    Pushdown Automata simulation engine.
    Validates bracket/delimiter balance using a stack.
    Simulates character-by-character with full stack trace.
    """

    def simulate(self, input_string: str) -> PDAResult:
        """Run PDA simulation on the entire input string."""
        stack: List[str] = []
        transitions: List[PDATransition] = []
        step = 0
        max_depth = 0
        pushes = 0
        pops = 0
        accepted = True

        # Extract only bracket characters for PDA (keep positional context)
        chars = list(input_string)

        for i, ch in enumerate(chars):
            if ch in OPEN_BRACKETS:
                stack_before = list(stack)
                stack.append(ch)
                pushes += 1
                max_depth = max(max_depth, len(stack))
                transitions.append(PDATransition(
                    step=step,
                    symbol=ch,
                    action=f"PUSH '{ch}' onto stack",
                    stack_before=stack_before,
                    stack_after=list(stack),
                    state="q_push"
                ))
                step += 1

            elif ch in CLOSE_BRACKETS:
                stack_before = list(stack)
                expected = BRACKET_PAIRS[ch]

                if not stack:
                    transitions.append(PDATransition(
                        step=step,
                        symbol=ch,
                        action=f"ERROR: Stack empty, unexpected '{ch}'",
                        stack_before=stack_before,
                        stack_after=[],
                        state="q_error"
                    ))
                    accepted = False
                    step += 1
                elif stack[-1] != expected:
                    transitions.append(PDATransition(
                        step=step,
                        symbol=ch,
                        action=f"ERROR: Mismatch — expected '{expected}', got '{stack[-1]}'",
                        stack_before=stack_before,
                        stack_after=list(stack),
                        state="q_error"
                    ))
                    accepted = False
                    step += 1
                else:
                    stack.pop()
                    pops += 1
                    transitions.append(PDATransition(
                        step=step,
                        symbol=ch,
                        action=f"POP '{expected}' — matched with '{ch}'",
                        stack_before=stack_before,
                        stack_after=list(stack),
                        state="q_pop"
                    ))
                    step += 1

        # If stack is not empty after processing, there are unmatched openers
        if stack:
            accepted = False
            transitions.append(PDATransition(
                step=step,
                symbol="EOF",
                action=f"ERROR: Unmatched bracket(s) remaining: {stack}",
                stack_before=list(stack),
                stack_after=list(stack),
                state="q_error"
            ))
        else:
            transitions.append(PDATransition(
                step=step,
                symbol="EOF",
                action="Stack empty — input accepted" if accepted else "Rejected due to earlier error",
                stack_before=list(stack),
                stack_after=[],
                state="q_accept" if accepted else "q_reject"
            ))

        return PDAResult(
            input_string=input_string,
            transitions=transitions,
            final_stack=stack,
            accepted=accepted,
            max_stack_depth=max_depth,
            total_pushes=pushes,
            total_pops=pops
        )