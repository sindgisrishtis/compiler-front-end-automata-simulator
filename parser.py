"""
parser.py
=========
Syntax validation engine.
Uses PDA-based bracket matching plus basic statement structure checks.
Maps to Context-Free Grammar (CFG) concepts from Theory of Computation.
"""

from dataclasses import dataclass, field
from typing import List, Tuple
from lexer import Token


# ─────────────────────────────────────────────
# DATA CLASSES
# ─────────────────────────────────────────────

@dataclass
class SyntaxError_:
    """A detected syntax error with location and description."""
    message: str
    line: int
    column: int
    severity: str = "ERROR"


@dataclass
class ParseResult:
    """Outcome of syntax analysis."""
    accepted: bool
    errors: List[SyntaxError_] = field(default_factory=list)
    warnings: List[SyntaxError_] = field(default_factory=list)
    statements_found: int = 0
    bracket_depth: int = 0


# ─────────────────────────────────────────────
# PDA BRACKET DEFINITIONS
# ─────────────────────────────────────────────

OPEN_BRACKETS  = {'(': ')', '{': '}', '[': ']'}
CLOSE_BRACKETS = {')': '(', '}': '{', ']': '['}


# ─────────────────────────────────────────────
# PARSER
# ─────────────────────────────────────────────

class Parser:
    """
    Context-Free Grammar-level syntax validator.

    Validates:
    1. Bracket balance (PDA stack simulation)
    2. Declaration syntax
    3. Missing semicolons
    4. Invalid identifiers
    5. Incomplete statements
    """

    def parse(self, tokens: List[Token]) -> ParseResult:

        errors: List[SyntaxError_] = []
        warnings: List[SyntaxError_] = []

        # ─────────────────────────────────────
        # Empty input
        # ─────────────────────────────────────

        if not tokens:
            errors.append(
                SyntaxError_(
                    "Empty source code",
                    1,
                    1
                )
            )

            return ParseResult(
                accepted=False,
                errors=errors,
                warnings=warnings,
                statements_found=0,
                bracket_depth=0
            )

        # ─────────────────────────────────────
        # 1. PDA BRACKET MATCHING
        # ─────────────────────────────────────

        stack: List[Tuple[str, int, int]] = []

        for tok in tokens:

            if tok.value in OPEN_BRACKETS:
                stack.append((tok.value, tok.line, tok.column))

            elif tok.value in CLOSE_BRACKETS:

                expected_open = CLOSE_BRACKETS[tok.value]

                if not stack:

                    errors.append(
                        SyntaxError_(
                            f"Unexpected closing '{tok.value}'",
                            tok.line,
                            tok.column
                        )
                    )

                elif stack[-1][0] != expected_open:

                    open_br, ol, oc = stack[-1]

                    errors.append(
                        SyntaxError_(
                            f"Bracket mismatch: '{open_br}' closed by '{tok.value}'",
                            tok.line,
                            tok.column
                        )
                    )

                    stack.pop()

                else:
                    stack.pop()

        # Unclosed brackets

        for (br, line, col) in stack:

            errors.append(
                SyntaxError_(
                    f"Unclosed bracket '{br}'",
                    line,
                    col
                )
            )

        # ─────────────────────────────────────
        # 2. INVALID TOKENS
        # ─────────────────────────────────────

        for tok in tokens:

            if tok.type == "UNKNOWN":

                errors.append(
                    SyntaxError_(
                        f"Unrecognised token '{tok.value}'",
                        tok.line,
                        tok.column
                    )
                )

        # ─────────────────────────────────────
        # 3. INCOMPLETE STATEMENTS
        # ─────────────────────────────────────

        if len(tokens) == 1:

            single = tokens[0]

            if single.type in ("IDENTIFIER", "NUMBER", "FLOAT"):

                errors.append(
                    SyntaxError_(
                        "Incomplete statement",
                        single.line,
                        single.column
                    )
                )

        # ─────────────────────────────────────
        # 4. MISSING SEMICOLON CHECK
        # ─────────────────────────────────────

        self._check_missing_semicolons(tokens, errors)

        # ─────────────────────────────────────
        # 5. STATEMENT COUNT
        # ─────────────────────────────────────

        stmts = sum(1 for t in tokens if t.value == ';')

        # ─────────────────────────────────────
        # FINAL RESULT
        # ─────────────────────────────────────

        return ParseResult(
            accepted=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            statements_found=stmts,
            bracket_depth=len(stack)
        )

    # ─────────────────────────────────────────
    # SEMICOLON VALIDATION
    # ─────────────────────────────────────────

    def _check_missing_semicolons(
        self,
        tokens: List[Token],
        errors: List[SyntaxError_]
    ) -> None:

        if not tokens:
            return

        TYPE_KEYWORDS = {
            "int",
            "float",
            "char",
            "double",
            "long",
            "short",
            "return"
        }

        has_braces = any(t.value in ["{", "}"] for t in tokens)

        ends_correctly = tokens[-1].value in [";", "}"]

        starts_statement = (
            tokens[0].type == "KEYWORD"
            or tokens[0].type == "IDENTIFIER"
        )

        # Reject:
        # int a = 10
        # return a
        # a = a + 1

        if starts_statement and not has_braces and not ends_correctly:

            last = tokens[-1]

            errors.append(
                SyntaxError_(
                    "Missing semicolon ';'",
                    last.line,
                    last.column
                )
            )