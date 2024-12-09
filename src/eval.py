from parse import *
from lexer import Token, TokenType, lex

def reduce(l: list, func):
    if len(l) == 0:
        return None
    result = l[0]
    for i in range(1, len(l)):
        result = func(result, l[i])
    return result
def get_function_call(name: str, args: list[ASTNode], env) -> ASTNode:
    args = [evaluate(arg, env) for arg in args]
    match name:
        case "TRUE":
            return 1
        case "FALSE":
            return 0
        case "ADD":
            return sum(args)
        case "SUB":
            return reduce(args, lambda a, b: a - b)
        case "MUL":
            return reduce(args, lambda a, b: a * b)
        case "DIV":
            return reduce(args, lambda a, b: a / b)
        case "AND":
            return all(arg == 1 for arg in args)
        case "OR":
            return any(arg == 1 for arg in args)
        
        

def evaluate(node: ASTNode, env: dict[str, any]) -> any:
    def get_var(name: str) -> any:
        if name not in env:
            raise Exception(f"Variable {name} not found")
        return env[name]
    if isinstance(node, Number):
        return node.value
    elif not isinstance(node, ASTNode):
        return node
    elif isinstance(node, String):
        return node.value
    elif isinstance(node, Variable):
        return get_var(node.name)
    elif isinstance(node, BinOp):
        left = evaluate(node.left, env)
        right = evaluate(node.right, env)
        match node.op:
            case TokenType.PLUS:
                if type(left) == str or type(right) == str:
                    raise Exception("Cannot add strings")
                return left + right
            case TokenType.AMPERSAND:
                if type(left) != str or type(right) != str:
                    raise Exception("Cannot concatenate non-strings")
                return left + right
            case TokenType.MINUS:
                return left - right
            case TokenType.MUL:
                return left * right
            case TokenType.DIV:
                return left / right
            case TokenType.EQ:
                return left == right
            case TokenType.NE:
                return left != right
            case TokenType.LT:
                return left < right
            case TokenType.LE:
                return left <= right
            case TokenType.GT:
                return left > right
            case TokenType.GE:
                return left >= right
            case TokenType.AND:
                return left and right
            case TokenType.OR:
                return left or right
            case _:
                raise Exception(f"Invalid operator {node.op}")
    elif isinstance(node, UnOp):
        right = evaluate(node.right, env)
        match node.op:
            case TokenType.NOT:
                return not right
            case _:
                raise Exception(f"Invalid operator {node.op}")
            
    elif isinstance(node, FunctionCall):
        return get_function_call(node.name, node.args, env)
    else:
        raise Exception(f"Invalid node {node}")
    
