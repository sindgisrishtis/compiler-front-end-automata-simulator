"""
lexer.py
========
Lexical analysis engine.
Tokenises C-style source code using regular expressions (which are
the theoretical equivalent of DFA-recognised regular languages).
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
    type: str       # e.g. KEYWORD, IDENTIFIER, NUMBER …
    value: str      # raw lexeme
    line: int
    column: int


# ─────────────────────────────────────────────
# LEXER
# ─────────────────────────────────────────────

KEYWORDS = {
    "int", "float", "char", "void", "if", "else",
    "for", "while", "do", "return", "break", "continue",
    "switch", "case", "default", "struct", "typedef", "double",
    "long", "short", "unsigned", "signed", "const", "static"
}

# Token patterns — order matters (more specific before general)
TOKEN_PATTERNS = [
    ("COMMENT",    r'//[^\n]*|/\*[\s\S]*?\*/'),
    ("FLOAT",      r'\b\d+\.\d+\b'),
    ("NUMBER",     r'\b\d+\b'),
    ("STRING",     r'"[^"\n]*"'),
    ("CHAR_LIT",   r"'[^'\n]'"),
    ("OPERATOR",   r'==|!=|<=|>=|&&|\|\||[+\-*/%=<>!&|^~]|\+\+|--|[+\-*/%]?='),
    ("SYMBOL",     r'[(){}\[\];,.]'),
    ("IDENTIFIER", r'\b[A-Za-z_][A-Za-z0-9_]*\b'),
    ("WHITESPACE", r'[ \t\r]+'),
    ("NEWLINE",    r'\n'),
    ("UNKNOWN",    r'.'),
]

MASTER_PATTERN = re.compile(
    '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_PATTERNS)
)


class Lexer:
    """
    Tokenises source code.
    Each token maps to a DFA-recognisable regular language.
    """

    def tokenise(self, source: str) -> List[Token]:
        """
        Run lexical analysis on source code.
        Returns a list of Token objects (whitespace and comments excluded).
        """
        tokens: List[Token] = []
        line = 1
        line_start = 0

        for match in MASTER_PATTERN.finditer(source):
            kind = match.lastgroup
            value = match.group()
            col = match.start() - line_start + 1

            if kind == "NEWLINE":
                line += 1
                line_start = match.end()
                continue

            if kind in ("WHITESPACE", "COMMENT"):
                # Count newlines inside block comments
                if kind == "COMMENT":
                    line += value.count('\n')
                continue

            # Resolve IDENTIFIER → KEYWORD if applicable
            if kind == "IDENTIFIER" and value in KEYWORDS:
                kind = "KEYWORD"

            tokens.append(Token(type=kind, value=value, line=line, column=col))

        return tokens

    def get_statistics(self, tokens: List[Token]) -> dict:
        """Return a summary of token type counts."""
        stats: dict = {}
        for tok in tokens:
            stats[tok.type] = stats.get(tok.type, 0) + 1
        return stats

    def has_errors(self, tokens: List[Token]) -> bool:
        """Check whether any UNKNOWN tokens were produced."""
        return any(t.type == "UNKNOWN" for t in tokens)