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
        return self.parser.parse(tokens)
    
    def evaluate(self, row: dict[str, any]) -> any:
        return evaluate(self.ast, row)
