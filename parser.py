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
    severity: str = "ERROR"   # ERROR | WARNING


@dataclass
class ParseResult:
    """Outcome of syntax analysis."""
    accepted: bool
    errors: List[SyntaxError_] = field(default_factory=list)
    warnings: List[SyntaxError_] = field(default_factory=list)
    statements_found: int = 0
    bracket_depth: int = 0


# ─────────────────────────────────────────────
# PARSER / SYNTAX VALIDATOR
# ─────────────────────────────────────────────

OPEN_BRACKETS  = {'(': ')', '{': '}', '[': ']'}
CLOSE_BRACKETS = {')': '(', '}': '{', ']': '['}


class Parser:
    """
    Context-Free Grammar-level syntax validator.
    
    Validates:
    1. Bracket balance (PDA stack simulation)
    2. Declaration syntax  → `type identifier = expr ;`
    3. Statement termination (semicolons)
    4. Mismatched bracket types
    5. Invalid identifier names (starting with digit)
    """

    def parse(self, tokens: List[Token]) -> ParseResult:
        errors: List[SyntaxError_] = []
        warnings: List[SyntaxError_] = []

        # ── 1. Bracket balance check ───────────────────────
        stack: List[Tuple[str, int, int]] = []   # (bracket, line, col)
        for tok in tokens:
            if tok.value in OPEN_BRACKETS:
                stack.append((tok.value, tok.line, tok.column))
            elif tok.value in CLOSE_BRACKETS:
                expected_open = CLOSE_BRACKETS[tok.value]
                if not stack:
                    errors.append(SyntaxError_(
                        f"Unexpected closing '{tok.value}' — no matching opening bracket",
                        tok.line, tok.column
                    ))
                elif stack[-1][0] != expected_open:
                    open_br, ol, oc = stack[-1]
                    errors.append(SyntaxError_(
                        f"Bracket mismatch: '{open_br}' at line {ol}:{oc} "
                        f"closed by '{tok.value}' at line {tok.line}:{tok.column}",
                        tok.line, tok.column
                    ))
                    stack.pop()
                else:
                    stack.pop()

        for (br, line, col) in stack:
            errors.append(SyntaxError_(
                f"Unclosed bracket '{br}' opened at line {line}:{col}",
                line, col
            ))

        # ── 2. Invalid identifiers (start with digit) ─────
        for tok in tokens:
            if tok.type == "UNKNOWN":
                errors.append(SyntaxError_(
                    f"Unrecognised token '{tok.value}'",
                    tok.line, tok.column
                ))

        # ── 3. Statement counting ──────────────────────────
        # Count top-level semicolons as statement terminators
        stmts = sum(1 for t in tokens if t.value == ';')

        # ── 4. Missing semicolons after declarations ───────
        # Simple heuristic: keyword ident ... no semicolon before next keyword or }
        self._check_missing_semicolons(tokens, errors, warnings)

        return ParseResult(
            accepted=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            statements_found=stmts,
            bracket_depth=0
        )

    def _check_missing_semicolons(
        self,
        tokens: List[Token],
        errors: List[SyntaxError_],
        warnings: List[SyntaxError_]
    ) -> None:
        """
        Warn when a declaration-like pattern (type ident =) 
        doesn't end with a semicolon before the next line-level keyword.
        """
        TYPE_KEYWORDS = {"int", "float", "char", "void", "double", "long", "short"}
        n = len(tokens)
        i = 0
        while i < n:
            tok = tokens[i]
            # pattern: TYPE IDENTIFIER = ... — look for semicolon before next statement
            if tok.type == "KEYWORD" and tok.value in TYPE_KEYWORDS:
                # scan forward for ';' or next keyword at same nesting
                j = i + 1
                found_semi = False
                depth = 0
                while j < n:
                    t = tokens[j]
                    if t.value in ('{', '(', '['):
                        depth += 1
                    elif t.value in ('}', ')', ']'):
                        depth -= 1
                        if depth < 0:
                            break
                    elif t.value == ';' and depth == 0:
                        found_semi = True
                        break
                    elif t.type == "KEYWORD" and t.value in TYPE_KEYWORDS and depth == 0 and j > i + 1:
                        break
                    j += 1
                if not found_semi:
                    warnings.append(SyntaxError_(
                        f"Possible missing ';' after declaration starting at line {tok.line}",
                        tok.line, tok.column,
                        severity="WARNING"
                    ))
            i += 1