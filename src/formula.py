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
