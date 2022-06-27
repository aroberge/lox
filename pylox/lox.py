"""Adaptation of Lox.java


This is done mostly as a simple translation from Java to Python,
using OOP even though the code might be simpler if
functions were used instead of methods.
"""
from __future__ import annotations

import sys

from .errors import LoxSyntaxError
from .lexer.scanner import Scanner


class Lox:
    """The class used as a starting point"""

    def __init__(self) -> None:
        """Entrypoint for the program"""
        self.had_error: bool = False

    def run_file(self, filename: str) -> None:
        """Runs code from a file"""
        with open(filename) as f:
            src = f.read()
        self.run(src)
        if self.had_error:
            sys.exit(65)

    def run_prompt(self) -> None:
        """Simple REPL"""
        print("pylox REPL\n")
        # use >> for prompt to distinguish from my terminal prompt
        prompt = ">> "
        while True:
            line = input(prompt)
            if not line:
                break
            try:
                self.run(line)
            except LoxSyntaxError as exc:
                print(" " * (exc.column + len(prompt)) + "^-- LoxSyntaxError.")
                print(f"{exc.message}\n")
                self.had_error = True
            else:
                self.had_error = False

    def run(self, source: str) -> None:
        """Runs code from a string"""
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        for token in tokens:
            print(token)
