from typing import Type

from .type_system import CppType, type_py2cpp, type_typing2py


class FuncArg:
    def __init__(self, name: str, argtype: Type):
        self.name = name
        self.type = argtype
        self.py_type = type_typing2py(self.type)
        self.cpp_type = type_py2cpp(self.py_type)
        self.cpp_str = self._gen_arg_cpp_str()

    def _gen_arg_cpp_str(self) -> str:
        """Generates C++ format of function arguments"""
        if self.cpp_type == CppType.BOOL:
            return f"bool {self.name}"
        if self.cpp_type == CppType.INT:
            return f"int {self.name}"
        if self.cpp_type == CppType.DOUBLE:
            return f"double {self.name}"
        if self.cpp_type == CppType.ARRAY_INT:
            return f"int *{self.name}"
        if self.cpp_type == CppType.ARRAY_DOUBLE:
            return f"double *{self.name}"
        raise TypeError(f"C++ type {self.cpp_type} is not supported.")
