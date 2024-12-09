<<<<<<< HEAD
from lexer import Token, TokenType, lex
from parse import ASTNode, Parser
from eval import evaluate

class Formula:
    def __init__(self, code: str, print_ast=False):
        self.code = code
        self.parser = Parser()
        self.ast: ASTNode = self.parse()
        if print_ast:
            self.ast.output()
    
    def parse(self) -> Exception|ASTNode:
        try: 
            tokens = lex(self.code)
            parsed = self.parser.parse(tokens)
        except: 
            return None
        return parsed
    
    def evaluate(self, row: dict[str, any]) -> any:
        try:        
            return evaluate(self.ast, row)
        except:
            return None
=======
from lexer import Token, TokenType, lex
from parse import ASTNode, Parser
from eval import evaluate

class Formula:
    def __init__(self, code: str):
        self.code = code
        self.parser = Parser()
        self.ast: ASTNode = self.parse()
    
    def parse(self):
        tokens = lex(self.code)
        print(tokens)
        return self.parser.parse(tokens)
    
    def evaluate(self, row: dict[str, any]) -> any:
        return evaluate(self.ast, row)
>>>>>>> c0e54d49ad7f0c763749c1f9c7a386b9415be23a
