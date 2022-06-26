"""Simple adaptation of Scanner.java"""

from .token import Token
from .token_type import *  # noqa


class Scanner:
    start = 0
    current = 0
    line = 1

    def __init__(self, source):
        self.source = source
        self.tokens = []

    def is_at_end(self):
        """Determine if we have found the last character"""
        return self.current >= len(self.source)

    def scan_token(self):
        add_token = self.add_token
        match char := self.advance():  # noqa
            case "(":
                add_token(LEFT_PAREN)
            case ")":
                add_token(RIGHT_PAREN)
            case "{":
                add_token(LEFT_BRACE)
            case "}":
                add_token(RIGHT_BRACE)
            case ",":
                add_token(COMMA)
            case ".":
                add_token(DOT)
            case "-":
                add_token(MINUS)
            case "+":
                add_token(PLUS)
            case ";":
                add_token(SEMICOLON)
            case "*":
                add_token(STAR)

    def advance(self):
        """Finds the next character and increment the location."""
        # Consider using try/finally here
        char = self.source[self.current]
        self.current += 1
        return char

    def add_token(self, type_, literal=None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type_, text, literal, self.line))
