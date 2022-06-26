"""Adaptation of Token.java"""
from __future__ import annotations


class Token:
    """Simple token object"""

    def __init__(
        self, type_: str, lexeme: str, literal: str, line: int, column: int = -1
    ) -> None:
        # Added column information, which is not included in the book.
        self.type_ = type_
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
        self.column = column

    def __str__(self) -> str:
        return f"{self.type_} {self.lexeme} {self.literal}"
