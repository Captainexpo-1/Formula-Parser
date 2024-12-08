import re
from enum import Enum
class TokenType(Enum):
    SKIP = 1
    NUMBER = 2
    ASSIGN = 3
    LPAREN = 4
    RPAREN = 5
    LBRACE = 6
    RBRACE = 7
    SEMICOLON = 8
    MUL = 9
    DIV = 10
    PLUS = 11
    MINUS = 12
    NEWLINE = 13
    COMMA = 14
    DOT = 15
    LT = 16
    GT = 17
    LE = 18
    GE = 19
    EQ = 20
    NE = 21
    AND = 22
    OR = 23
    NOT = 24
    IF = 25
    ELSE = 26
    TRUE = 27
    FALSE = 28
    NULL = 29
    ID = 30
    STRING = 31
    MISMATCH = 32
    EOF = 33
    OF = 34
    VARIABLE_NAME = 35
    AMPERSAND = 36
    LBRACK = 37
    RBRACK = 38

# Define token specifications
token_specification = [(i[0], re.compile(i[1])) for i in [
    (TokenType.SKIP,     r'[ \t\n]+'),       # Skip over spaces, newlines, and tabs
    (TokenType.NUMBER,   r'((\d+)\.\d+)(?!\w)'),  # Integer or decimal number
    (TokenType.NUMBER,   r'\d+(?!\w)'),        # Decimal number without leading digit
    (TokenType.LPAREN,   r'\('),           # Left parenthesis
    (TokenType.RPAREN,   r'\)'),           # Right parenthesis
    (TokenType.LBRACE,   r'\{'),           # Left brace
    (TokenType.RBRACE,   r'\}'),           # Right brace
    (TokenType.LBRACK,   r'\['),           # Left brack
    (TokenType.RBRACK,   r'\]'),           # Right brack
    (TokenType.SEMICOLON, r';'),           # Statement terminator
    (TokenType.MUL,      r'\*'),           # Multiplication operator
    (TokenType.DIV,      r'/'),            # Division operator
    (TokenType.PLUS,     r'\+'),           # Addition operator
    (TokenType.MINUS,    r'-'),            # Subtraction operator
    (TokenType.COMMA,    r','),            # Comma
    (TokenType.DOT,      r'\.'),           # Dot
    (TokenType.LT,       r'<'),            # Less than
    (TokenType.GT,       r'>'),            # Greater than
    (TokenType.LE,       r'<='),           # Less than or equal to
    (TokenType.GE,       r'>='),           # Greater than or equal to
    (TokenType.EQ,       r'='),           # Equal to
    (TokenType.NE,       r'!='),           # Not equal to
    (TokenType.AMPERSAND,r'&'),            # String concatenation
    (TokenType.AND,      r'AND'),          # Logical AND
    (TokenType.OR,       r'OR'),           # Logical OR
    (TokenType.NOT,      r'NOT'),          # Logical NOT
    (TokenType.IF,       r'IF'),           # IF keyword
    (TokenType.ELSE,     r'ELSE'),         # ELSE keyword
    (TokenType.TRUE,     r'TRUE'),         # TRUE keyword
    (TokenType.FALSE,    r'FALSE'),        # FALSE keyword
    (TokenType.NULL,     r'NULL'),         # NULL keyword
    (TokenType.ID,       r'[A-Za-z_]\w*'), # Identifiers
    (TokenType.STRING,   r'"(?:\\.|[^"\\])*"'),  # String literals
    (TokenType.MISMATCH, r'.'),            # Any other character
]]


class Token:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value
    def __str__(self):
        return f"{self.kind}: {self.value}"
    def __repr__(self): 
        return str(self)

# Lexer function
def lex(code):
    pos = 0
    tokens = []
    while pos < len(code):
        match = None
        if code[pos] == '{':
            pos += 1
            inner = ""
            while code[pos] != '}':
                inner += code[pos]
                pos += 1
            tokens.append(Token(TokenType.VARIABLE_NAME, inner))
            pos += 1
            continue
        for token_kind, regex in token_specification:
            match = regex.match(code, pos)
            if match:
                text = match.group(0)
                if token_kind != TokenType.SKIP:
                    tokens.append(Token(token_kind, text))
                break
        if not match:
            raise Exception(f"Invalid character at position {pos}")
        pos = match.end(0)
    return tokens

# Example usage
if __name__ == '__main__':
    code = '''MIN({Regular Price}, {Sale Price})''' # EX airtable formula
    for token in lex(code):
        print(token)