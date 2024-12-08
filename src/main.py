from parse import *
from lexer import lex
from formula import Formula
def main():
    v = input("Enter k:v, k:v, ... pairs for vars\n")
    vars = {}
    if v != "":
        for pair in v.split(","):
            k,v = pair.split(":")
            k,v = k.strip(), v.strip()
            if all(i.isdigit() for i in v):
                v = float(v)
            if v == "True":
                v = True
            if v == "False":
                v = False
            if v == "None" or v == "NULL":
                v = None
            vars[k] = v
        print(vars)

    while True:
        code = input(">> ")
        if code == "exit":
            break
        formula = Formula(code)
        print(formula.ast)
        #result = formula.evaluate(vars)
        #print("RESULT:", result)        


if __name__ == "__main__":
    main()