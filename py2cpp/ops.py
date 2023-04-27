import ast
from enum import Enum


class OpType(Enum):
    """Operator Types"""

    # Arithmetic Operators
    ADD = 0
    SUB = 1
    MULT = 2
    DIV = 3
    FLOORDIV = 4
    MOD = 5
    # Comparison Operators
    EQ = 6
    NOTEQ = 7
    LT = 8
    LTEQ = 9
    GT = 10
    GTEQ = 11
    # Boolean Operators
    NOT = 12
    AND = 13
    OR = 14
    # Unary Operators
    UADD = 15
    USUB = 16


class Operator:
    def __init__(self, op_type: OpType) -> None:
        self.op_type = op_type
        self.cpp_str = self._generate_cpp_str()

    def _generate_cpp_str(self) -> str:
        if self.op_type is None:
            raise ValueError("op_type is not set.")
        if self.op_type == OpType.ADD:
            return "+"
        if self.op_type == OpType.SUB:
            return "-"
        if self.op_type == OpType.MULT:
            return "*"
        if self.op_type == OpType.DIV:
            return "/"
        if self.op_type == OpType.FLOORDIV:
            return "/"
        if self.op_type == OpType.MOD:
            return "%"
        if self.op_type == OpType.EQ:
            return "=="
        if self.op_type == OpType.NOTEQ:
            return "!="
        if self.op_type == OpType.LT:
            return "<"
        if self.op_type == OpType.LTEQ:
            return "<="
        if self.op_type == OpType.GT:
            return ">"
        if self.op_type == OpType.GTEQ:
            return ">="
        if self.op_type == OpType.NOT:
            return "!"
        if self.op_type == OpType.AND:
            return "&&"
        if self.op_type == OpType.OR:
            return "||"
        if self.op_type == OpType.UADD:
            return "+"
        if self.op_type == OpType.USUB:
            return "-"
        raise TypeError(f"Operator {self.op_type} is not supported")


def process_operator(op: ast.operator) -> Operator:
    """Processes an operator and return corresponding Operator object.

    Args:
        op (ast.operator): An operator to processed

    Raises:
        TypeError: Raised when the operator is not supported

    Returns:
        Operator: A constructed Operator object
    """
    if isinstance(op, ast.Add):
        return Operator(OpType.ADD)
    if isinstance(op, ast.Sub):
        return Operator(OpType.SUB)
    if isinstance(op, ast.Mult):
        return Operator(OpType.MULT)
    if isinstance(op, ast.Div):
        return Operator(OpType.DIV)
    if isinstance(op, ast.FloorDiv):
        return Operator(OpType.FLOORDIV)
    if isinstance(op, ast.Mod):
        return Operator(OpType.MOD)
    if isinstance(op, ast.Eq):
        return Operator(OpType.EQ)
    if isinstance(op, ast.NotEq):
        return Operator(OpType.NOTEQ)
    if isinstance(op, ast.Lt):
        return Operator(OpType.LT)
    if isinstance(op, ast.LtE):
        return Operator(OpType.LTEQ)
    if isinstance(op, ast.Gt):
        return Operator(OpType.GT)
    if isinstance(op, ast.GtE):
        return Operator(OpType.GTEQ)
    if isinstance(op, ast.Not):
        return Operator(OpType.NOT)
    if isinstance(op, ast.And):
        return Operator(OpType.AND)
    if isinstance(op, ast.Or):
        return Operator(OpType.OR)
    if isinstance(op, ast.UAdd):
        return Operator(OpType.UADD)
    if isinstance(op, ast.USub):
        return Operator(OpType.USUB)
    raise TypeError(f"Operator {op} is not supported")
