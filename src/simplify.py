
from lexer import Token, TokenType, lex
from typing import List, Union, Optional

from parse import ASTNode, BinOp, UnOp, Number, String

def get_literal(node: ASTNode) -> Union[int, float, str, None]:
    if isinstance(node, Number):
        return node.value
    elif isinstance(node, String):
        return node.value
    else:
        return None

def simplify_unop(node: UnOp) -> ASTNode:
    right = get_literal(node.right)
    if right is None:
        return node
    try:
        if node.op == TokenType.MINUS:
            return Number(-right)
        else:
            raise Exception(f"Invalid operator {node.op}")
    except:
        return node

def simplify_binop(node: BinOp) -> ASTNode:
    left = get_literal(node.left)
    right = get_literal(node.right)

    if left is None or right is None:
        return node
    try:
        if node.op == TokenType.PLUS:
            if isinstance(left, str) or isinstance(right, str):
                raise Exception("Cannot add strings")
            return Number(left + right)
        elif node.op == TokenType.AMPERSAND:
            if isinstance(left, str) and isinstance(right, str):
                return String(left + right)
            else:
                raise Exception("Cannot concatenate non-strings")
        
        left = float(left)
        right = float(right)
            
        match node.op:
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