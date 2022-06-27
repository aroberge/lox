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
                add_token(TT.BANG_EQUAL) if self.is_next("=") else add_token(TT.BANG)
            case "=":
                add_token(TT.EQUAL_EQUAL) if self.is_next("=") else add_token(TT.EQUAL)
            case "<":
                add_token(TT.LESS_EQUAL) if self.is_next("=") else add_token(TT.LESS)
            case ">":
                add_token(TT.GREATER_EQUAL) if self.is_next("=") else add_token(
                    TT.GREATER
                )
            case "/":
                if self.is_next("/"):
                    # This is a comment; ignore until the end of line.
                    while True:
                        next_ = self.peek()
                        if next_ != "\n" and not self.is_at_end():
                            self.advance()
                        else:
                            break
                else:
                    add_token(TT.SLASH)
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1
                self.column = -1
            case '"':
                self.string_()
            case _:
                raise LoxSyntaxError(self.line, self.column, f"Unknown token {char}")

    def advance(self) -> str:
        """Finds the next character and increment the location."""
        # Consider using try/finally here
        char = self.source[self.current]
        self.current += 1
        self.column += 1
        return char

    def is_next(self, expected: str) -> bool:
        """Return True and advance stream if current token equals the expected one."""
        # This method is called 'match' in the book
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

    def string_(self) -> None:
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
