import sys

from pylox.lox import Lox


def main() -> None:
    args = sys.argv
    if len(args) > 2:
        print("Usage: py -m lox [script]")
        sys.exit(64)
    lox = Lox()
    if len(args) == 2:
        lox.run_file(args[1])
    else:
        try:
            lox.run_prompt()
        except KeyboardInterrupt:
            print("\n   Goodbye!")
            sys.exit(64)


main()
