import ast
import inspect
from typing import Any, Dict, List

from .expression import VarCtxt, Variable
from .funcarg import FuncArg
from .statement import ReturnStmt, process_stmt


def transpile(func, arg_types: List[Any]):
    ### Construct AST
    py_src = inspect.getsource(func)
    tree = ast.parse(py_src)
    func_def = tree.body[0]

    ### FUNC NAME
    func_name: str = func_def.name
    ### ARGS
    func_args = [
        FuncArg(arg.arg, arg_types[i]) for i, arg in enumerate(func_def.args.args)
    ]
    ### BODY
    cpp_body: List[Any] = []
    var_table: Dict[str, Variable] = dict()
    # register args to var_table
    for func_arg in func_args:
        var_table[func_arg.name] = Variable(func_arg.name, func_arg.type, VarCtxt.REUSE)

    for stmt in func_def.body:
        processed_stmt = process_stmt(stmt, var_table)
        cpp_body.append(processed_stmt)

    ### construct cpp_src
    cpp_body_str: str = ""
    ret_type_str: str = None

    # depth is 0-indexed
    def convert_stmts_to_strs(block: List, depth: int) -> None:
        nonlocal cpp_body_str, ret_type_str
        for stmt in block:
            if isinstance(stmt, ReturnStmt):
                # detect return statement
                if ret_type_str is None:
                    ret_type_str = stmt.cpp_type_str
                elif ret_type_str != stmt.cpp_type_str:
                    raise TypeError("Multiple return types are not supported.")
            if isinstance(stmt.cpp_str, str):
                cpp_body_str += "\t" * (depth + 1) + stmt.cpp_str + "\n"
            elif isinstance(stmt.cpp_str, list):
                cpp_body_str += "\t" * (depth + 1) + stmt.cpp_str[0] + "\n"
                convert_stmts_to_strs(stmt.body, depth + 1)
                cpp_body_str += "\t" * (depth + 1) + stmt.cpp_str[-1] + "\n"
            else:
                raise TypeError("stmt.cpp_str must be str or list[str].")

    convert_stmts_to_strs(cpp_body, 0)
    header = (
        f"{ret_type_str} {func_name}({', '.join(map(lambda x: x.cpp_str, func_args))}) "
        + "{\n"
    )
    tail = "}\n"
    # concatenates all
    cpp_src = header + cpp_body_str + tail

    return cpp_src
