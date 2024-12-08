from parse import *
from lexer import lex
from formula import Formula
def main():
    while True:
        code = input(">> ")
        if code == "exit":
            break
        formula = Formula(code)
        print(formula.ast)


if __name__ == "__main__":
    main()