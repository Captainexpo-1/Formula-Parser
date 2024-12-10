from parse import *
from lexer import lex
from formula import Formula
from transpiler import Transpiler
import sys

def main():
    args = sys.argv
    transpiler = Transpiler()
    do_transpile = args.count("-t") > 0
    do_print_parse = args.count("--ast") > 0
    do_print_tokens = args.count("--tokens") > 0
    do_use_file = args.count("-f") > 0
    f = None if not do_use_file else args[args.index("-f") + 1]
    if do_use_file:
        inp: str = open(f, "r").read()
        formula = Formula(inp, print_ast=do_print_parse, print_tokens=do_print_tokens)
        if do_transpile: print(transpiler.transpile(formula.ast, "my_table", "result"))
        return
    while True:
        try:
            code = input(">> ")
            formula = Formula(code, print_ast=do_print_parse, print_tokens=do_print_tokens)
            if do_transpile: print(transpiler.transpile(formula.ast, "my_table", "result"))
        except KeyboardInterrupt:
            exit(0)

if __name__ == "__main__":
    main()