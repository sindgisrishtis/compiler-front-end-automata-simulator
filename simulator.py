"""
simulator.py
============
Orchestrates full compilation pipeline:
  source code → tokens (Lexer) → DFA traces → PDA trace → parse result
"""

from dataclasses import dataclass, field
from typing import List, Dict

from lexer import Lexer, Token
from parser import Parser, ParseResult
from automata import DFAEngine, DFAResult, PDAEngine, PDAResult


@dataclass
class SimulationReport:
    """
    Aggregated result of a full simulation run.
    Consumed by the Streamlit frontend.
    """
    source: str
    tokens: List[Token]
    token_stats: Dict[str, int]

    # DFA
    dfa_results: List[DFAResult]
    total_dfa_states: int
    total_dfa_transitions: int

    # PDA
    pda_result: PDAResult

    # Parse
    parse_result: ParseResult

    # Overall verdict
    lexically_valid: bool
    syntactically_valid: bool


class Simulator:
    """
    High-level orchestrator that ties together:
    - Lexer  (regular language / DFA-level)
    - DFA engine (per-token state machine simulation)
    - PDA engine (bracket-level stack simulation)
    - Parser (CFG-level structural checks)
    """

    def __init__(self):
        self.lexer  = Lexer()
        self.parser = Parser()
        self.dfa    = DFAEngine()
        self.pda    = PDAEngine()

    def run(self, source: str) -> SimulationReport:
        """Execute the full simulation pipeline."""

        # ── Lexical analysis ───────────────────────────────
        tokens = self.lexer.tokenise(source)
        token_stats = self.lexer.get_statistics(tokens)
        lex_valid = not self.lexer.has_errors(tokens)

        # ── DFA simulation (per token) ─────────────────────
        dfa_results: List[DFAResult] = []
        total_transitions = 0
        state_set = set()

        for tok in tokens:
            result = self.dfa.simulate(tok.value)
            dfa_results.append(result)
            total_transitions += len(result.transitions)
            for s in result.states_visited:
                state_set.add(s)

        # ── PDA simulation (whole source for brackets) ─────
        pda_result = self.pda.simulate(source)

        # ── Syntax / parse check ───────────────────────────
        parse_result = self.parser.parse(tokens)

        return SimulationReport(
            source=source,
            tokens=tokens,
            token_stats=token_stats,
            dfa_results=dfa_results,
            total_dfa_states=len(state_set),
            total_dfa_transitions=total_transitions,
            pda_result=pda_result,
            parse_result=parse_result,
            lexically_valid=lex_valid,
            syntactically_valid=parse_result.accepted,
        )