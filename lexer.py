"""
lexer.py
========
Lexical analysis engine.
Tokenises C-style source code using regular expressions
(theoretical equivalent of DFA-recognised regular languages).
"""

import re
from dataclasses import dataclass
from typing import List


# ─────────────────────────────────────────────
# TOKEN DEFINITION
# ─────────────────────────────────────────────

@dataclass
class Token:
    """Represents a single lexical token."""
    type: str
    value: str
    line: int
    column: int


# ─────────────────────────────────────────────
# KEYWORDS
# ─────────────────────────────────────────────

KEYWORDS = {
    "int", "float", "char", "void", "if", "else",
    "for", "while", "do", "return", "break", "continue",
    "switch", "case", "default", "struct", "typedef",
    "double", "long", "short", "unsigned", "signed",
    "const", "static"
}


# ─────────────────────────────────────────────
# TOKEN PATTERNS
# ORDER MATTERS
# ─────────────────────────────────────────────

TOKEN_PATTERNS = [

    # Comments
    ("COMMENT",    r'//[^\n]*|/\*[\s\S]*?\*/'),

    # INVALID IDENTIFIERS
    # catches: 1abc, 123name, 99temp
    ("INVALID_IDENTIFIER", r'\b\d+[A-Za-z_][A-Za-z0-9_]*\b'),

    # Float
    ("FLOAT",      r'\b\d+\.\d+\b'),

    # Integer
    ("NUMBER",     r'\b\d+\b'),

    # String
    ("STRING",     r'"[^"\n]*"'),

    # Character literal
    ("CHAR_LIT",   r"'[^'\n]'"),

    # Operators
    ("OPERATOR",   r'==|!=|<=|>=|&&|\|\||\+\+|--|[+\-*/%=<>!&|^~]'),

    # Symbols
    ("SYMBOL",     r'[(){}\[\];,.]'),

    # Valid identifier
    ("IDENTIFIER", r'\b[A-Za-z_][A-Za-z0-9_]*\b'),

    # Spaces
    ("WHITESPACE", r'[ \t\r]+'),

    # Newline
    ("NEWLINE",    r'\n'),

    # Unknown character
    ("UNKNOWN",    r'.'),
]


MASTER_PATTERN = re.compile(
    '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_PATTERNS)
)


# ─────────────────────────────────────────────
# LEXER
# ─────────────────────────────────────────────

class Lexer:
    """
    Tokenises source code using DFA-style regular expressions.
    """

    def tokenise(self, source: str) -> List[Token]:

        tokens: List[Token] = []

        line = 1
        line_start = 0

        for match in MASTER_PATTERN.finditer(source):

            kind = match.lastgroup
            value = match.group()

            col = match.start() - line_start + 1

            # Handle newline
            if kind == "NEWLINE":
                line += 1
                line_start = match.end()
                continue

            # Ignore whitespace/comments
            if kind in ("WHITESPACE", "COMMENT"):

                if kind == "COMMENT":
                    line += value.count('\n')

                continue

            # Invalid identifiers → UNKNOWN
            if kind == "INVALID_IDENTIFIER":
                kind = "UNKNOWN"

            # Convert identifier → keyword
            elif kind == "IDENTIFIER" and value in KEYWORDS:
                kind = "KEYWORD"

            tokens.append(
                Token(
                    type=kind,
                    value=value,
                    line=line,
                    column=col
                )
            )

        return tokens


    # ─────────────────────────────────────────

    def get_statistics(self, tokens: List[Token]) -> dict:
        """Return token count statistics."""

        stats = {}

        for tok in tokens:
            stats[tok.type] = stats.get(tok.type, 0) + 1

        return stats


    # ─────────────────────────────────────────

    def has_errors(self, tokens: List[Token]) -> bool:
        """Check whether lexer produced invalid tokens."""

        return any(tok.type == "UNKNOWN" for tok in tokens)