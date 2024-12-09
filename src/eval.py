
from lexer import Token, TokenType, lex
from typing import List, Union, Optional

from parse import ASTNode, BinOp, Number, String

def get_literal(node: ASTNode) -> Union[int, float, str, None]:

    if isinstance(node, Number):
        return node.value
    elif isinstance(node, String):
        return node.value
    else:
        return None

def evaluate_binop(node: BinOp) -> any:
    left = get_literal(node.left)
    right = get_literal(node.right)

    if left is None or right is None:
        return node
    try:
        match node.op:
            case TokenType.PLUS:
                if type(left) == str or type(right) == str:
                    raise Exception("Cannot add strings")
                return Number(left + right)
            case TokenType.AMPERSAND:
                if type(left) != str or type(right) != str:
                    raise Exception("Cannot concatenate non-strings")
                return String(left + right)
            case TokenType.MINUS:
                return Number(left - right)
            case TokenType.MUL:
                return Number(left * right)
            case TokenType.DIV:
                return Number(left / right)
            case TokenType.EQ:
                return Number(left == right)
            case TokenType.NE:
                return Number(left != right)
            case TokenType.LT:
                return Number(left < right)
            case TokenType.LE:
                return Number(left <= right)
            case TokenType.GT:
                return Number(left > right)
            case TokenType.GE:
                return Number(left >= right)
            case TokenType.AND:
                return Number(left and right)
            case TokenType.OR:
                return Number(left or right)
            case _:
                raise Exception(f"Invalid operator {node.op}")
    except:
        return node