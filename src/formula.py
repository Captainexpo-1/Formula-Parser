from lexer import Token, TokenType, lex
from parse import ASTNode, Parser

class Formula:
    def __init__(self, code: str, print_ast=False, print_tokens=False):
        self.code = code
        self.parser = Parser()
        self.print_tokens = print_tokens
        self.ast: ASTNode|None = self.parse() 
        if print_ast and self.ast is not None:
            self.ast.output()
    
    def parse(self) -> ASTNode|None:
        try: 
            tokens = lex(self.code)
            if self.print_tokens:
                print(tokens)
            parsed = self.parser.parse(tokens)
        except Exception as e: 
            print(f"Failed to parse {self.code}: {e}")
            return None
        return parsed
