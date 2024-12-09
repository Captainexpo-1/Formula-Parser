from parse import ASTNode, BinOp, UnOp, Number, String, FunctionCall, Variable, Array
from lexer import TokenType


class Transpiler:
    
    comparison_ops = [TokenType.EQ, TokenType.NE, TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE]
    logical_ops = [TokenType.AND, TokenType.OR, TokenType.NOT]
    arithmetic_ops = [TokenType.PLUS, TokenType.MINUS, TokenType.MUL, TokenType.DIV]
    
    
    def __init__(self) -> None:
        self.output = ""
        self.indent = 0
        self.indent_str = "  "
        
    def write(self, text: str, indent=False, nl=False) -> None:
        self.output += ("\n" if nl else "") + self.indent_str * (self.indent if indent else 0) + text

    def writeln(self, text: str, indent=True,nl=False) -> None:
        self.write(text + "\n", indent=indent,nl=nl)

    def transpile(self, node: ASTNode) -> str:
        """Transpile an AST to SQL

        Args:
            node (ASTNode): The root node of the AST

        Returns:
            str: The transpiled SQL
        """
        self.output = ""
        self.indent = 0
        self.visit(node, {})
        return self.output

    def visit(self, node: ASTNode, ctx: dict[any, any]) -> None:
        """Transpile a node to SQL

        Args:
            node (ASTNode): The node to transpile
            ctx (dict[any, any]): The context

        Raises:
            Exception: When the node is invalid
        """
        if isinstance(node, BinOp):
            self.visit_binop(node, ctx)
        elif isinstance(node, UnOp):
            self.visit_unop(node, ctx)
        elif isinstance(node, Number):
            self.visit_number(node, ctx)
        elif isinstance(node, String):
            self.visit_string(node, ctx)
        elif isinstance(node, FunctionCall):
            self.visit_function_call(node, ctx)
        elif isinstance(node, Variable):
            self.visit_variable(node, ctx)
        elif isinstance(node, Array):
            self.visit_array(node, ctx)
        else:
            raise Exception(f"Invalid node {node}")

    def visit_binop(self, node: BinOp, ctx: dict[any, any]) -> None:
        """Transpile a binary operation node to SQL
        
        Args:
            node (BinOp): the binary operation node
            ctx (dict[any, any]): the context
        """
        
        if node.op == TokenType.AMPERSAND:
            #print("AMPERSAND")
            self.write("CONCAT(")
            self.visit(node.left, ctx)
            self.write(", ")
            self.visit(node.right, ctx)
            self.write(")")
            return
        def get_operator_equivalent(operator: TokenType):
            match operator:
                case TokenType.PLUS:
                    return "+"
                case TokenType.MINUS:
                    return "-"
                case TokenType.MUL:
                    return "*"
                case TokenType.DIV:
                    return "/"
                case TokenType.EQ:
                    return "="
                case TokenType.NE:
                    return "!="
                case TokenType.LT:
                    return "<"
                case TokenType.LE:
                    return "<="
                case TokenType.GT:
                    return ">"
                case TokenType.GE:
                    return ">="
                case TokenType.AMPERSAND:
                    return "||"
                case TokenType.DOT:
                    return "."
                case _:
                    raise Exception(f"Invalid operator {operator}")
        self.write("(")
        self.visit(node.left, ctx)
        self.write(f" {get_operator_equivalent(node.op)} ")
        self.visit(node.right, ctx)
        self.write(")")
                
    def visit_function_call(self, node: FunctionCall, ctx: dict[any, any]) -> None:
        """Transpile a function call node to SQL

        Args:
            node (FunctionCall): the function call node
            ctx (dict[any, any]): the context
        """
        if node.name == "IF":
            # Transpile to SQL
            if not ctx.get("in_if", False):
                self.write("CASE")
                self.indent += 1
                self.write("WHEN ",nl=True,indent=True)
            else:
                self.write("WHEN ",nl=True,indent=True)
            self.visit(node.args[0], ctx)

            self.write(" THEN ",indent=False)
            self.indent += 1
            self.visit(node.args[1], ctx)
            self.indent -= 1
            if isinstance(node.args[2], FunctionCall):
                if node.args[2].name == "IF":
                    # Nested IF, should be transpiled to a nested CASE WHEN
                    self.visit(node.args[2], {"in_if": True})
            else:
                self.write("ELSE ",nl=True, indent=True)

                self.visit(node.args[2], ctx)
                self.indent -= 1
            if not ctx.get("in_if", False):
                self.indent -= 1
                self.write("END",nl=True,indent=True)
        elif node.name == "AND":
            self.write("(")
            self.visit(node.args[0], ctx)
            self.write(" AND ") 
            self.visit(node.args[1], ctx)
            self.write(")")
        elif node.name == "OR":
            self.write("(")
            self.visit(node.args[0], ctx)
            self.write(" OR ")
            self.visit(node.args[1], ctx)
            self.write(")")
        elif node.name == "NOT":
            self.write("(")
            self.visit(node.args[0], ctx)
            self.write(" = 0)")
        elif node.name == "TRUE":
            self.write("1")
        elif node.name == "FALSE":
            self.write("0")
        elif node.name == "LEN":
            self.write("LENGTH(")
            self.visit(node.args[0], ctx)
            self.write(")")
        elif node.name == "FIND":
            self.write("INSTR(")
            self.visit(node.args[1], ctx)
            self.write(", ")
            self.visit(node.args[0], ctx)
            self.write(")")
        elif node.name == "CONCATENATE":
            self.write("CONCAT(")
            self.visit(node.args[0], ctx)
            self.write(", ")
            self.visit(node.args[1], ctx)
            self.write(")")
        elif node.name == "SUBSTITUTE":
            self.write("REPLACE(")
            self.visit(node.args[0], ctx)
            self.write(", ")
            self.visit(node.args[1], ctx)
            self.write(", ")
            self.visit(node.args[2], ctx)
            self.write(")")
        elif node.name == "DATETIME_DIFF":
            self.write("DATEDIFF(")
            self.visit(node.args[0], ctx)
            self.write(", ")
            self.visit(node.args[1], ctx)
            self.write(")")
        elif node.name == "TODAY":
            self.write("CURRENT_DATE")
        elif node.name == "IS_BEFORE":
            self.write("(")
            self.visit(node.args[0], ctx)
            self.write(" < ")
            self.visit(node.args[1], ctx)
            self.write(")")
        else:
            self.write(f"{node.name}(")
            for i, arg in enumerate(node.args):
                self.visit(arg, ctx)
                if i < len(node.args) - 1:
                    self.write(", ")
            self.write(")")

    def visit_unop(self, node: UnOp, ctx: dict[any, any]) -> None:
        self.write(f"{node.op.value}")
        self.visit(node.right)

    def visit_number(self, node: Number, ctx: dict[any, any]) -> None:
        if int(node.value) == node.value:
            self.write(str(int(node.value)))
            return 
        self.write(str(node.value))

    def visit_string(self, node: String, ctx: dict[any, any]) -> None:
        self.write(f'"{node.value}"')

    def visit_array(self, node: Array, ctx: dict[any, any]) -> None:
        self.write("[")
        for i, item in enumerate(node.items):
            self.visit(item)
            if i < len(node.items) - 1:
                self.write(", ")
        self.write("]")

    def visit_variable(self, node: Variable, ctx: dict[any, any]) -> None:
        self.write(node.name.replace(" ", "_"))