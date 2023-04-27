from enum import Enum
from typing import List, Type


class PyType(Enum):
    BOOL = 0
    INT = 1
    FLOAT = 2
    LIST_INT = 3
    LIST_FLOAT = 4


class CppType(Enum):
    BOOL = 0
    INT = 1
    DOUBLE = 2
    ARRAY_INT = 3
    ARRAY_DOUBLE = 4


def type_typing2py(src: Type) -> PyType:
    if src == bool:
        return PyType.BOOL
    if src == int:
        return PyType.INT
    if src == float:
        return PyType.FLOAT
    if src == List[int]:
        return PyType.LIST_INT
    if src == List[float]:
        return PyType.LIST_FLOAT
    raise TypeError(f"Python type {src} is not supported.")


def type_py2cpp(src: PyType) -> CppType:
    if src == PyType.BOOL:
        return CppType.BOOL
    if src == PyType.INT:
        return CppType.INT
    if src == PyType.FLOAT:
        return CppType.DOUBLE
    if src == PyType.LIST_INT:
        return CppType.ARRAY_INT
    if src == PyType.LIST_FLOAT:
        return CppType.ARRAY_DOUBLE
    raise TypeError(f"Python type {src} is not supported.")
