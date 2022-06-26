"""Adaptation of TokenType.java

Rather than using enum.Enum to emulate the java class used in the
book, we use simple module constants. This enables to simplify
referring to token types in the code, similarly to what is done
with the *-import on page 46."""
from __future__ import annotations

# Single character tokens
LEFT_PAREN: str = "("
RIGHT_PAREN: str = ")"
LEFT_BRACE: str = "{"
RIGHT_BRACE: str = "}"
COMMA: str = ","
DOT: str = "."
MINUS: str = "-"
PLUS: str = "+"
SEMICOLON: str = ";"
SLASH: str = "/"
STAR: str = "*"

# One or two character tokens
BANG: str = "!"
BANG_EQUAL: str = "!="
EQUAL: str = "="
EQUAL_EQUAL: str = "=="
GREATER: str = ">"
GREATER_EQUAL: str = ">="
LESS: str = "<"
LESS_EQUAL: str = "<="

# Identifiers
IDENTIFIER: str = "IDENTIFIER"
STRING: str = "STRING"
NUMBER: str = "NUMBER"

# Keywords
AND: str = "AND"
CLASS: str = "CLASS"
ELSE: str = "ELSE"
FALSE: str = "FALSE"
FUN: str = "FUN"
FOR: str = "FOR"
IF: str = "IF"
NIL: str = "NIL"
OR: str = "OR"
PRINT: str = "PRINT"
RETURN: str = "RETURN"
SUPER: str = "SUPER"
THIS: str = "THIS"
TRUE: str = "TRUE"
VAR: str = "VAR"
WHILE: str = "WHILE"

EOF: str = "EOF"
