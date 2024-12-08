from lexer import Token, TokenType
from typing import List, Union, Optional

class ASTNode:
    def output(self, indent: int = 0) -> None:
        pass

class BinOp(ASTNode):
    def __init__(self, left: ASTNode, op: TokenType, right: ASTNode) -> None:
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self) -> str:
        return f'BinOp({self.left} {self.op} {self.right})'
    
    def output(self, indent: int = 0) -> None:
        print(' ' * indent + f'BinOp({self.op}')
        self.left.output(indent + 4)
        self.right.output(indent + 4)
        print(' ' * indent + ')')

class UnOp(ASTNode):
    def __init__(self, op: TokenType, right: ASTNode) -> None:
        self.op = op
        self.right = right

    def __repr__(self) -> str:
        return f'UnOp({self.op} {self.right})'
    
    def output(self, indent: int = 0) -> None:
        print(' ' * indent + f'UnOp({self.op}')
        self.right.output(indent + 4)
        print(' ' * indent + ')')

class Number(ASTNode):
    def __init__(self, value: Optional[float]) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"Number({self.value})"
    
    def output(self, indent: int = 0) -> None:
        print(' ' * indent + f"Number({self.value})")

class String(ASTNode):
    def __init__(self, value: str) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f'String("{self.value}")'
    
    def output(self, indent: int = 0) -> None:
        print(' ' * indent + f'String("{self.value}")')

class Variable(ASTNode):
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'Variable("{self.name}")'
    
    def output(self, indent: int = 0) -> None:
        print(' ' * indent + f'Variable("{self.name}")')

class FunctionCall(ASTNode):
    def __init__(self, name: str, args: List[ASTNode]) -> None:
        self.name = name
        self.args = args

    def __repr__(self) -> str:
        return f'FunctionCall("{self.name}", {self.args})'
    
    def output(self, indent: int = 0) -> None:
        print(' ' * indent + f'FunctionCall("{self.name}"')
        for arg in self.args:
            arg.output(indent + 4)
        print(' ' * indent + ')')

class Array(ASTNode):
    def __init__(self, elements: List[ASTNode]) -> None:
        self.elements = elements

    def __repr__(self) -> str:
        return f'Array({self.elements})'
    
    def output(self, indent: int = 0) -> None:
        print(' ' * indent + 'Array(')
        for element in self.elements:
            element.output(indent + 4)
        print(' ' * indent + ')')

class Parser:
    def __init__(self) -> None:
        self.tokens: List[Token] = []
        self.pos: int = 0

    def current_token(self) -> Token:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else Token(TokenType.EOF, None)

    def eat(self, token_type: TokenType) -> None:
        if self.current_token().kind == token_type:
            self.pos += 1
        else:
            raise Exception(f"Unexpected token {self.current_token().kind}, expected {token_type}")

    def parse(self, tokens: List[Token]) -> Optional[ASTNode]:
        self.tokens = tokens
        self.pos = 0
        if not self.tokens:
            return None
        
        if (token := self.current_token().kind) != TokenType.EOF:
            raise Exception(f"parser didn't consume all tokens, found {token}")
        
        return self.expression()

    def expression(self, precedence: int = 0) -> ASTNode:
        left = self.primary()
        while True:
            token = self.current_token()
            token_precedence = self.get_precedence(token.kind)

            if token_precedence <= precedence:
                break

            op = token.kind
            self.eat(op)
            right = self.expression(token_precedence)
            left = BinOp(left, op, right)

        return left

    def primary(self) -> ASTNode:
        token = self.current_token()

        if token.kind == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Number(float(token.value))

        elif token.kind == TokenType.ID:
            # Check if it's a function call
            if self.peek() == TokenType.LPAREN:
                func_name = token.value
                self.eat(TokenType.ID)
                self.eat(TokenType.LPAREN)
                args = []
                while self.current_token().kind != TokenType.RPAREN:
                    args.append(self.expression())
                    if self.current_token().kind == TokenType.COMMA:
                        self.eat(TokenType.COMMA)
                self.eat(TokenType.RPAREN)
                return FunctionCall(func_name, args)
            else:
                # Just a variable
                var_name = token.value
                self.eat(TokenType.ID)
                return Variable(var_name)
        elif token.kind == TokenType.STRING:
            self.eat(TokenType.STRING)
            return String(token.value[1:-1])
        
        elif token.kind == TokenType.NULL:
            self.eat(TokenType.NULL)
            return Number(None)

        elif token.kind == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expression()
            self.eat(TokenType.RPAREN)
            return node

        elif token.kind == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            return UnOp('-', self.primary())

        elif token.kind == TokenType.LBRACK:
            self.eat(TokenType.LBRACK)
            e = []
            while self.current_token().kind != TokenType.RBRACK:
                e.append(self.expression())
                if self.current_token().kind == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
            self.eat(TokenType.RBRACK)
            return Array(e)
    
        elif token.kind == TokenType.VARIABLE_NAME:
            name = token.value
            self.eat(TokenType.VARIABLE_NAME)
            return Variable(name)

        else:
            raise Exception(f"Unexpected token {token.kind}")

    def peek(self) -> TokenType:
        return self.tokens[self.pos + 1].kind if self.pos + 1 < len(self.tokens) else TokenType.EOF

    def get_precedence(self, token_type: TokenType) -> int:
        precedences = {
            TokenType.PLUS: 10,
            TokenType.AMPERSAND: 10,
            TokenType.MINUS: 10,
            TokenType.MUL: 20,
            TokenType.DIV: 20,
            TokenType.AND: 5,
            TokenType.OR: 5,
            TokenType.EQ: 7,
            TokenType.NE: 7,
            TokenType.LT: 7,
            TokenType.GT: 7,
            TokenType.LE: 7,
            TokenType.GE: 7,
        }
        return precedences.get(token_type, 0)
