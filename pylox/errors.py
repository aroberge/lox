"""Custom exceptions"""


class LoxSyntaxError(Exception):
    def __init__(self, line: int, column: int, message: str):
        self.line = line
        self.column = column
        self.message = message
