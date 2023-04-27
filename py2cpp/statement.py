import ast
from typing import Dict, List

from .expression import Array, Expression, VarCtxt, Variable, process_expr
from .ops import Operator, OpType, process_operator
from .type_system import CppType, type_py2cpp, type_typing2py


class Statement:
    def __init__(self) -> None:
        self.cpp_str = None


class Assign(Statement):
    def __init__(self, targets: List[Expression], value: Expression) -> None:
        super().__init__()
        self.targets = targets
        self.value = value
        self.cpp_str = ""
        for target in targets:
            self.cpp_str += f"{target.cpp_str} = "
        self.cpp_str += f"{value.cpp_str};"


class AugAssign(Statement):
    def __init__(self, target: Expression, op: Operator, value: Expression) -> None:
        super().__init__()
        # check type validity and detect implicit cast
        if op.op_type in (OpType.ADD, OpType.SUB, OpType.MULT):
            if target.cpp_type != value.cpp_type:
                raise TypeError(
                    f"Implicit cast from {value.cpp_type} to {target.cpp_type} is not supported."
                )
        elif op.op_type == OpType.DIV:
            if target.cpp_type == CppType.INT:
                raise TypeError(f"'/=' operation for int variable is not supported.")
        elif op.op_type == OpType.FLOORDIV:
            if not (target.cpp_type == value.cpp_type == CppType.INT):
                raise TypeError(
                    f"'//=' operation except for {target.cpp_type} target and {value.cpp_type} value is not supported."
                )
        elif op.op_type == OpType.MOD:
            if not (target.cpp_type == value.cpp_type == CppType.INT):
                raise TypeError(
                    f"'%=' operation except for {target.cpp_type} target and {value.cpp_type} value is not supported."
                )
        self.target = target
        self.op = op
        self.value = value
        self.cpp_str = f"{target.cpp_str} {op.cpp_str}= {value.cpp_str};"


class IfStmt(Statement):
    def __init__(self, test: Expression, body: List[Statement], orelse) -> None:
        super().__init__()
        self.test = test
        self.body = body
        self.orelse = orelse  # TODO: to support elif, else
        header = f"if {self.test.cpp_str} " + "{"
        lines = list(map(lambda x: x.cpp_str, body))
        tail = "}"
        self.cpp_str = [header] + lines + [tail]


class WhileStmt(Statement):
    def __init__(self, test: Expression, body: List[Statement], orelse) -> None:
        super().__init__()
        self.test = test
        self.body = body
        self.orelse = orelse
        header = f"while {self.test.cpp_str} " + "{"
        lines = list(map(lambda x: x.cpp_str, body))
        tail = "}"
        self.cpp_str = [header] + lines + [tail]


class ReturnStmt(Statement):
    def __init__(self, ret_val: Expression) -> None:
        super().__init__()
        type = ret_val.type
        py_type = type_typing2py(type)
        self.cpp_type = type_py2cpp(py_type)
        self.cpp_type_str = self._gen_ret_type_str()
        self.cpp_str = f"return {ret_val.cpp_str};"

    def _gen_ret_type_str(self) -> str:
        if self.cpp_type == CppType.BOOL:
            return "bool"
        if self.cpp_type == CppType.INT:
            return "int"
        if self.cpp_type == CppType.DOUBLE:
            return "double"
        if self.cpp_type == CppType.ARRAY_INT:
            return "int *"
        if self.cpp_type == CppType.ARRAY_DOUBLE:
            return "double *"


class GeneralStatement(Statement):
    def __init__(self, expr: Expression) -> None:
        super().__init__()
        self.cpp_str = f"{expr.cpp_str};"


def process_assign(stmt: ast.Assign, var_table: Dict[str, Variable]) -> Assign:
    # right value
    rv = process_expr(stmt.value, var_table)
    # left value
    targets = [process_expr(target, var_table) for target in stmt.targets]
    # TODO: to support Multiple targets assignment
    if len(targets) >= 2:
        # multiple targets assignment
        if not all([t.ctx == VarCtxt.REUSE for t in targets]):
            raise ValueError(
                f"Multiple targets are only supported when all variables are already defined."
            )
        # raise ValueError(f"More than 1 target is not supported.")
        if rv.cpp_type not in {CppType.BOOL, CppType.INT, CppType.DOUBLE}:
            raise TypeError(
                f"Multiple targets are only supported for Number-like types."
            )

    # for array type variable, set size
    if isinstance(rv, Array):
        targets[0].set_size(rv.size)
    for target in targets:
        if target.ctx == VarCtxt.NEW:
            target.set_type(rv.type)
            var_table[target.id].set_type(rv.type)
        else:
            # detects implicit cast
            if rv.cpp_type != target.cpp_type:
                raise TypeError(
                    f"Implicit cast from {rv.cpp_type} to {target.cpp_type} is not supported."
                )

    return Assign(targets, rv)


def process_aug_assign(
    stmt: ast.AugAssign, var_table: Dict[str, Variable]
) -> AugAssign:
    # right value
    rv = process_expr(stmt.value, var_table)
    # operator
    op = process_operator(stmt.op)
    # left value
    target = process_expr(stmt.target, var_table)
    return AugAssign(target, op, rv)


def process_if(stmt: ast.If, var_table: Dict[str, Variable]) -> IfStmt:
    condition = process_expr(stmt.test, var_table)
    body = []
    for child_stmt in stmt.body:
        processed_child_stmt = process_stmt(child_stmt, var_table)
        body.append(processed_child_stmt)
    orelse = stmt.orelse
    return IfStmt(condition, body, orelse)


def process_while(stmt: ast.While, var_table: Dict[str, Variable]) -> WhileStmt:
    condition = process_expr(stmt.test, var_table)
    body: List[Statement] = []
    for child_stmt in stmt.body:
        processed_child_stmt = process_stmt(child_stmt, var_table)
        body.append(processed_child_stmt)
    orelse = stmt.orelse
    return WhileStmt(condition, body, orelse)


def process_return(stmt: ast.Return, var_table: Dict[str, Variable]) -> ReturnStmt:
    ret_val = process_expr(stmt.value, var_table)
    return ReturnStmt(ret_val)


def process_general_stmt(
    stmt: ast.Expr, var_table: Dict[str, Variable]
) -> GeneralStatement:
    processed_expr = process_expr(stmt.value, var_table)
    return GeneralStatement(processed_expr)


def process_stmt(
    stmt: ast.stmt, var_table: Dict[str, Variable]
) -> Statement or List[Statement]:
    """Processes a statement according to its type and meta information and return constructed object(s)

    Args:
        stmt (ast.stmt): A statement to be processed
        var_table (Dict[str, Variable]): A variable table

    Raises:
        TypeError: Raised when the statement is not supported.

    Returns:
        Statement or List[Statement]: Constructed Statement object(s)
    """
    if isinstance(stmt, ast.Assign):
        processed_stmt = process_assign(stmt, var_table)
        return processed_stmt
    elif isinstance(stmt, ast.AugAssign):
        processed_stmt = process_aug_assign(stmt, var_table)
        return processed_stmt
    elif isinstance(stmt, ast.If):
        processed_stmts = process_if(stmt, var_table)
        return processed_stmts
    elif isinstance(stmt, ast.While):
        processed_stmts = process_while(stmt, var_table)
        return processed_stmts
    elif isinstance(stmt, ast.Return):
        processed_stmt = process_return(stmt, var_table)
        return processed_stmt
    elif isinstance(stmt, ast.Expr):
        processed_stmt = process_general_stmt(stmt, var_table)
        return processed_stmt
    else:
        raise TypeError(f"Statement {stmt} is not supported.")
