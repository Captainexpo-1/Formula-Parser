import re
from enum import Enum, auto
from typing import List, Tuple, Pattern, Union

class TokenType(Enum):
    SKIP = auto()
    NUMBER = auto()
    ASSIGN = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    MUL = auto()
    DIV = auto()
    PLUS = auto()
    MINUS = auto()
    NEWLINE = auto()
    COMMA = auto()
    DOT = auto()
    LT = auto()
    GT = auto()
    LE = auto()
    GE = auto()
    EQ = auto()
    NE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    IF = auto()
    ELSE = auto()
    TRUE = auto()
    FALSE = auto()
    NULL = auto()
    ID = auto()
    STRING = auto()
    MISMATCH = auto()
    EOF = auto()
    OF = auto()
    VARIABLE_NAME = auto()
    AMPERSAND = auto()
    LBRACK = auto()
    RBRACK = auto()

# Define token specifications
token_specification: List[Tuple[TokenType, Pattern[str]]] = [(i[0], re.compile(i[1])) for i in [
    (TokenType.SKIP,     r'[ \t\n]+'),           # Skip over spaces, newlines, and tabs
    (TokenType.NUMBER,   r'((\d+)\.\d+)(?!\w)'), # Integer or decimal number
    (TokenType.NUMBER,   r'\d+(?!\w)'),          # Decimal number without leading digit
    (TokenType.LPAREN,   r'\('),                 # Left parenthesis
    (TokenType.RPAREN,   r'\)'),                 # Right parenthesis
    (TokenType.LBRACE,   r'\{'),                 # Left brace
    (TokenType.RBRACE,   r'\}'),                 # Right brace
    (TokenType.LBRACK,   r'\['),                 # Left brack
    (TokenType.RBRACK,   r'\]'),                 # Right brack
    (TokenType.MUL,      r'\*'),                 # Multiplication operator
    (TokenType.DIV,      r'/'),                  # Division operator
    (TokenType.PLUS,     r'\+'),                 # Addition operator
    (TokenType.MINUS,    r'-'),                  # Subtraction operator
    (TokenType.COMMA,    r','),                  # Comma
    (TokenType.DOT,      r'\.'),                 # Dot
    (TokenType.LE,       r'<='),                 # Less than or equal to
    (TokenType.GE,       r'>='),                 # Greater than or equal to
    (TokenType.EQ,       r'='),                  # Equal to
    (TokenType.NE,       r'!='),                 # Not equal to
    (TokenType.LT,       r'<'),                  # Less than
    (TokenType.GT,       r'>'),                  # Greater than
    (TokenType.AMPERSAND,r'&'),                  # String concatenations
    (TokenType.ID,       r'[A-Za-z_]\w*'),       # Identifiers
    (TokenType.STRING,   r'"(?:\\.|[^"\\])*"'),  # String literals
    (TokenType.MISMATCH, r'.'),                  # Any other character
]]

class Token:
    def __init__(self, kind: TokenType, value: str) -> None:
        self.kind = kind
        self.value = value

    def __str__(self) -> str:
        return f"{self.kind}: {self.value}"

    def __repr__(self) -> str:
        return str(self)

# Lexer function
def lex(code: str) -> List[Token]:
    pos = 0
    tokens: List[Token] = []
    while pos < len(code):
        match: Union[re.Match[str], None] = None
        if code[pos] == '{':
            pos += 1
            inner = ""
            while code[pos] != '}':
                if code[pos] == "\\":
                    pos += 1
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