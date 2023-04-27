import ast
from enum import Enum
from typing import Dict, List, Type

from .ops import Operator, OpType, process_operator
from .type_system import CppType, type_py2cpp, type_typing2py


class VarCtxt(Enum):
    """Variable context types"""

    NEW = 0  # newly defined
    REUSE = 1  # already defined


class Expression:
    def __init__(self, type: Type) -> None:
        self.type = type

        self.py_type = None
        self.cpp_type = None
        self.cpp_str = None

        if self.type is not None:
            self.py_type = type_typing2py(self.type)
            self.cpp_type = type_py2cpp(self.py_type)


class Variable(Expression):
    def __init__(self, id: str, type: Type, ctx: VarCtxt, size: int = None) -> None:
        super().__init__(type)
        self.id = id
        self.ctx = ctx
        self.size = size
        self._reflect_ctx()

    def set_type(self, type: Type) -> None:
        """Sets the type of Variable and update cpp_str"""
        self.type = type
        self._reflect_ctx()

    def set_size(self, size: int) -> None:
        """Sets the size of array and update cpp_str"""
        self.size = size
        self._reflect_ctx()

    def _reflect_ctx(self) -> None:
        if self.type is None:
            return
        self.py_type = type_typing2py(self.type)
        self.cpp_type = type_py2cpp(self.py_type)
        if self.ctx == VarCtxt.NEW:
            self.cpp_str = self._gen_vardef_cpp_str()
        elif self.ctx == VarCtxt.REUSE:
            self.cpp_str = self.id
        else:
            raise ValueError("ctx must be NEW or REUSE.")

    def _gen_vardef_cpp_str(self) -> str:
        if self.cpp_type == CppType.BOOL:
            return f"bool {self.id}"
        if self.cpp_type == CppType.INT:
            return f"int {self.id}"
        if self.cpp_type == CppType.DOUBLE:
            return f"double {self.id}"
        if self.cpp_type == CppType.ARRAY_INT:
            return f"int {self.id}[{self.size}]"
        if self.cpp_type == CppType.ARRAY_DOUBLE:
            return f"double {self.id}[{self.size}]"
        raise TypeError(f"C++ type {self.cpp_type} is not supported.")


class Constant(Expression):
    def __init__(self, value: int or float or bool) -> None:
        if not isinstance(value, (int, float, bool)):
            raise TypeError(f"Invalid value type {type(value)}")
        super().__init__(type(value))
        # True / False in Python is equivalent to true / false in C++.
        self.cpp_str = str(value).lower() if isinstance(value, bool) else str(value)


class Array(Expression):
    def __init__(self, value: list) -> None:
        if not isinstance(value, list):
            raise TypeError(f"{value} is not a list.")

        self.size = len(value)
        if self.size == 0:
            raise ValueError("Literal [] is not supported.")

        ele_type = type(value[0])
        if not all([type(ele) == ele_type for ele in value]):
            raise TypeError(f"All elements in a list must have the same type.")
        if ele_type == int:
            super().__init__(List[int])
        elif ele_type == float:
            super().__init__(List[float])
        else:
            raise TypeError(f"Element type {ele_type} is not supported.")

        self.cpp_str = "{" + ", ".join(map(str, value)) + "}"


class Compare(Expression):
    def __init__(
        self, left: Expression, ops: List[Operator], comps: List[Expression]
    ) -> None:
        super().__init__(bool)
        self.left = left
        self.ops = ops
        self.comps = comps
        # for multiple (oprator, comparator) pairs
        conditions = [f"{left.cpp_str} {ops[0].cpp_str} {comps[0].cpp_str}"]
        for idx in range(1, len(comps)):
            conditions.append(
                f"{comps[idx-1].cpp_str} {ops[idx].cpp_str} {comps[idx].cpp_str}"
            )
        self.cpp_str = f"({' && '.join(conditions)})"


class BinOp(Expression):
    def __init__(self, left: Expression, op: Operator, right: Expression) -> None:
        prefix = ""
        # check type validity and initialize evaluated type
        # addition, subtraction, multiplication
        if op.op_type in (OpType.ADD, OpType.SUB, OpType.MULT):
            if left.cpp_type == CppType.INT and right.cpp_type == CppType.INT:
                super().__init__(int)
            elif left.cpp_type == CppType.INT and right.cpp_type == CppType.DOUBLE:
                super().__init__(float)
            elif left.cpp_type == CppType.DOUBLE and right.cpp_type == CppType.INT:
                super().__init__(float)
            elif left.cpp_type == CppType.DOUBLE and right.cpp_type == CppType.DOUBLE:
                super().__init__(float)
            else:
                raise TypeError(
                    f"Invalid operand types: {left.cpp_type} and {right.cpp_type}"
                )
        # division
        elif op.op_type == OpType.DIV:
            if left.cpp_type == CppType.INT and right.cpp_type == CppType.INT:
                # (INT)/(INT) in Python is equivalent to (double)(INT)/(INT) in C++
                prefix = "(double)"
                # to be evaluated as float in Python, as double in C++
                super().__init__(float)
            elif left.cpp_type == CppType.INT and right.cpp_type == CppType.DOUBLE:
                super().__init__(float)
            elif left.cpp_type == CppType.DOUBLE and right.cpp_type == CppType.INT:
                super().__init__(float)
            elif left.cpp_type == CppType.DOUBLE and right.cpp_type == CppType.DOUBLE:
                super().__init__(float)
            else:
                raise TypeError(
                    f"Invalid operand types: {left.cpp_type} and {right.cpp_type}"
                )
        # floor division
        elif op.op_type == OpType.FLOORDIV:
            if left.cpp_type == CppType.INT and right.cpp_type == CppType.INT:
                # (INT)//(INT) in Python is equivalent to (INT)/(INT) in C++
                # to be evaluated as int
                super().__init__(int)
            elif left.cpp_type == CppType.DOUBLE or right.cpp_type == CppType.DOUBLE:
                raise TypeError(
                    f"FloorDiv with operands ({left.cpp_type}, {right.cpp_type}) is not supported."
                )
            else:
                raise TypeError(
                    f"Invalid operand types: {left.cpp_type} and {right.cpp_type}"
                )
        # modulo
        elif op.op_type == OpType.MOD:
            if left.cpp_type == CppType.INT and right.cpp_type == CppType.INT:
                # (INT)%(INT) in Python is equivalent to (INT)%(INT) in C++
                # to be evaluated as int
                super().__init__(int)
            elif left.cpp_type == CppType.DOUBLE or right.cpp_type == CppType.DOUBLE:
                raise TypeError(
                    f"Modulo with operands ({left.cpp_type}, {right.cpp_type}) is not supported."
                )
            else:
                raise TypeError(
                    f"Invalid operand types: {left.cpp_type} and {right.cpp_type}"
                )

        self.left = left
        self.op = op
        self.right = right
        self.cpp_str = f"({prefix}{left.cpp_str} {op.cpp_str} {right.cpp_str})"


class UnaryOp(Expression):
    def __init__(self, op: Operator, operand: Expression) -> None:
        super().__init__(operand.type)
        self.op = op
        self.operand = operand
        self.cpp_str = f"({op.cpp_str}{operand.cpp_str})"


class BoolOp(Expression):
    def __init__(self, op: Operator, values: List[Expression]) -> None:
        super().__init__(bool)
        self.op = op
        self.values = values
        self.cpp_str = f"({values[0].cpp_str}"
        # for multiple operands
        for value in values[1:]:
            self.cpp_str += f" {op.cpp_str} {value.cpp_str}"
        self.cpp_str += ")"


class Subscript(Expression):
    def __init__(
        self, value: Expression, slice: Expression, array_type: Type, ctx: VarCtxt
    ):
        if array_type == List[int]:
            super().__init__(int)
        elif array_type == List[float]:
            super().__init__(float)
        else:
            raise TypeError(f"Array type {array_type} is not supported.")
        self.value = value
        self.slice = slice
        self.ctx = ctx
        self.cpp_str = f"{value.cpp_str}[{slice.cpp_str}]"


class Index(Expression):
    def __init__(self, value: Expression):
        if value.cpp_type != CppType.INT:
            raise TypeError("Index must be an integer.")
        super().__init__(int)
        self.value = value
        self.cpp_str = value.cpp_str


class FunctionCall(Expression):
    def __init__(self, func_id: str, func_args: List[Variable or Constant], ret_type):
        super().__init__(ret_type)
        func_args_strs: List[str] = []
        for arg in func_args:
            if isinstance(arg, Variable):
                func_args_strs.append(arg.id)
            elif isinstance(arg, Constant):
                func_args_strs.append(arg.cpp_str)
            else:
                raise TypeError(f"Argument type {arg.cpp_type} is not supported.")
        self.cpp_str = f"{func_id}({', '.join(func_args_strs)})"


def process_expr(expr: ast.expr, var_table: Dict[str, Variable]) -> Expression:
    """Processes an expression and returns a constructed Expression object.

    Args:
        expr (ast.expr): An expression to be processed.
        var_table (Dict[str, Variable]): A variable table

    Returns:
        Expression: A constructed Expression object
    """
    # variables
    if isinstance(expr, ast.Name):
        if isinstance(expr.ctx, ast.Load):
            # when loaded, no type annotation needed
            if expr.id not in var_table:
                raise ValueError(
                    f"Variable {expr.id} must be defined before this expression."
                )
            return Variable(expr.id, var_table[expr.id].type, VarCtxt.REUSE)
        elif isinstance(expr.ctx, ast.Store):
            if expr.id in var_table:
                # already defined, so no type annotation needed
                return Variable(expr.id, var_table[expr.id].type, VarCtxt.REUSE)
            # to define new variable, so type annotation is needed
            var_table[expr.id] = Variable(expr.id, None, VarCtxt.NEW)
            return Variable(expr.id, None, VarCtxt.NEW)
        else:
            raise TypeError(f"Variable context {expr.ctx} is not supported.")
    # literals
    elif isinstance(expr, ast.Constant):
        return Constant(expr.value)

    elif isinstance(expr, ast.List):
        py_list = [c.value for c in expr.elts]
        return Array(py_list)

    # comparisons
    elif isinstance(expr, ast.Compare):
        target = process_expr(expr.left, var_table)
        ops = [process_operator(op) for op in expr.ops]
        comps = [process_expr(comp, var_table) for comp in expr.comparators]
        return Compare(target, ops, comps)

    # operations
    elif isinstance(expr, ast.BinOp):
        left = process_expr(expr.left, var_table)
        op = process_operator(expr.op)
        right = process_expr(expr.right, var_table)
        return BinOp(left, op, right)

    elif isinstance(expr, ast.UnaryOp):
        op = process_operator(expr.op)
        operand = process_expr(expr.operand, var_table)
        return UnaryOp(op, operand)

    elif isinstance(expr, ast.BoolOp):
        op = process_operator(expr.op)
        values = [process_expr(v, var_table) for v in expr.values]
        return BoolOp(op, values)

    elif isinstance(expr, ast.Subscript):
        var: Variable = process_expr(expr.value, var_table)
        idx: Index = process_expr(expr.slice, var_table)
        array_type = var_table[var.id].type
        return Subscript(var, idx, array_type, VarCtxt.REUSE)

    elif isinstance(expr, ast.Index):
        var = process_expr(expr.value, var_table)
        return Index(var)

    # function call
    elif isinstance(expr, ast.Call):
        func_id = expr.func.id
        func_args = [process_expr(arg, var_table) for arg in expr.args]
        if func_id in var_table:
            ret_type = var_table[func_id].type
        else:
            # cannot decide return type now
            ret_type = None
        return FunctionCall(func_id, func_args, ret_type)

    else:
        raise TypeError(f"Value type {type(expr)} is not supported,")
