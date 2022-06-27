"""Simple adaptation of Scanner.java"""

from ..errors import LoxSyntaxError
from .token import Token
from .token_type import TokenType as TT  # noqa


class Scanner:
    """Scans the source one character at a time, identifying tokens"""

    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens: list[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1
        self.column: int = -1

    def is_at_end(self) -> bool:
        """Determine if we have found the last character"""
        return self.current >= len(self.source)

    def scan_tokens(self) -> list[Token]:
        """Scans the source one character at a time, converting the source
        into a list of tokens.
        """
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TT.EOF, "", "\0", self.line))
        return self.tokens

    def scan_token(self) -> None:
        """Scan the source, with the goal of identifying a single Token."""
        add_token = self.add_token
        match char := self.advance():
            case "(":
                add_token(TT.LEFT_PAREN)
            case ")":
                add_token(TT.RIGHT_PAREN)
            case "{":
                add_token(TT.LEFT_BRACE)
            case "}":
                add_token(TT.RIGHT_BRACE)
            case ",":
                add_token(TT.COMMA)
            case ".":
                add_token(TT.DOT)
            case "-":
                add_token(TT.MINUS)
            case "+":
                add_token(TT.PLUS)
            case ";":
                add_token(TT.SEMICOLON)
            case "*":
                add_token(TT.STAR)
            case "!":
                add_token(TT.BANG_EQUAL) if self.match("=") else add_token(TT.BANG)
            case "=":
                add_token(TT.EQUAL_EQUAL) if self.match("=") else add_token(TT.EQUAL)
            case "<":
                add_token(TT.LESS_EQUAL) if self.match("=") else add_token(TT.LESS)
            case ">":
                add_token(TT.GREATER_EQUAL) if self.match("=") else add_token(
                    TT.GREATER
                )
            case "/":
                if self.match("/"):
                    # This is a comment; ignore until the end of line.
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    add_token(TT.SLASH)
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1
                self.column = -1
            case '"':
                self.string()
            case _:
                if char.isdigit():
                    self.number()
                else:
                    raise LoxSyntaxError(
                        self.line, self.column, f"Unknown token {char}"
                    )

    def advance(self) -> str:
        """Finds the next character and increment the location."""
        # Consider using try/finally here
        char = self.source[self.current]
        self.current += 1
        self.column += 1
        return char

    def match(self, expected: str) -> bool:
        """Return True and advance stream if current token equals the expected one."""
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self) -> str:
        """Looks at the next character, without actually advancing the scanner."""
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def add_token(self, type_: TT, literal: str = "") -> None:
        """Appends a single token"""
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type_, text, literal, self.line))

    def string(self) -> None:
        """Finds the text inside a string. Supports multiline strings."""
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
                self.column = -1
            self.advance()

        if self.is_at_end():
            raise LoxSyntaxError(self.line, self.column, "Unterminated string.")

        # get the closing "
        self.advance()

        string_content = self.source[self.start + 1 : self.current - 1]
        self.add_token(TT.STRING, string_content)

    def number(self) -> None:
        """Get a number"""
        while self.peek().isdigit():
            self.advance()
        # Look for the fractional part
        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()
        self.add_token(TT.NUMBER, self.source[self.start : self.current])

    def peek_next(self) -> str:
        """Looks at the second next character, without actually advancing the scanner."""
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]
