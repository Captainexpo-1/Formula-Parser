from parse import *
from lexer import lex
from formula import Formula
import sys

def main():
    args = sys.argv
    if len(args) > 2:
        if args[1] == "-f":
            inp: str = open(args[2], "r").read()
            formula = Formula(inp, print_ast=True)
            return
    while True:
        try:
            code = input(">> ")
            formula = Formula(code)
            print(formula.ast)
        except KeyboardInterrupt:
            exit(0)

if __name__ == "__main__":
    main()