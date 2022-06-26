"""Adaptation of Lox.java


This is done mostly as a simple translation from Java to Python,
using OOP even though the code might be simpler if
functions were used instead of methods.
"""
from __future__ import annotations

import sys

from .lexer.scanner import Scanner


class Lox:
    """The class used as a starting point"""

    had_error = False

    def __init__(self, args: list) -> None:
        """Entrypoint for the program"""
        if len(args) > 2:
            print("Usage: py -m lox [script]")
            sys.exit(64)
        elif len(args) == 2:
            self.run_file(args[1])
        else:
            self.run_prompt()

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
        while True:
            # use >> for prompt to distinguish from my terminal prompt
            line = input(">> ")
            if not line:
                break
            self.run(line)
            self.had_error = False

    def run(self, source: str):
        """Runs code from a string"""
        scanner = Scanner(source)
        tokens = scanner.scan_token()
        for token in tokens:
            print(token)

    def error(self, line: int, column: int, message: str) -> None:
        """Gathering error information for reporting.

        Added column information as suggested on page 42.
        """
        self.report(line, column, "", message)

    def report(self, line: int, column: int, where: str, message: str) -> None:
        """Reporting error"""
        sys.stderr.write(f"[line {line}] Error{where}: {message}\n")
        sys.stderr.write(" " * column + "^-- Here.\n")
        self.had_error = True
