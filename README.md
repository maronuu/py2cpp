# py2cpp

## What
A transpiler that converts a Python function into a C++ function. Only subset of Python spec is supported.

## Usage
```bash
$ cd example
$ python sample.py > result.cpp
```
`example/result_with_comment.cpp` is the output `result.cpp` with added comments.

## Spec
### Types of elements in Python's List
In Python, a list can store elements of different types, but in C++ arrays, this is not allowed. If multiple types are found in a list in the source code, it is considered an error.

### Type conversion
For type conversion between int and float, the following rules are defined. t, v are variables of int or float.

|Statement|Specification|
|---|---|
|`t = v`  (t is already defined)|t and v must be of the same type|
|`t += v`|t and v must be of the same type|
|`t -= v`|t and v must be of the same type|
|`t *= v`|t and v must be of the same type|
|`t /= v`|t must be int|
|`t //= v`|t, v both must be int|
|`t %= v`|t, v both must be int|

### Div(`/`, `/=`)

|Python|C++|
|---|---|
|`(INT)/(INT)`|`(double)(INT)/(INT)`|
|`(INT)/(FLOAT)`|`(INT)/(DOUBLE)`|
|`(FLOAT)/[=](INT)`|`(DOUBLE)/[=](INT)`|
|`(FLOAT)/[=](FLOAT)`|`(DOUBLE)/[=](DOUBLE)`|

### Floor Div, Modulo (`//`, `//=`, `%`, `%=`)

|Python|C++|
|---|---|
|`(INT)//[=](INT)`|`(INT)/[=](INT)`|
|`(INT)%[=](INT)`|`(INT)%[=](INT)`|
|Other Operands|Not Supported|

### Empty List `[]`
For this transpiler, only array element reference and writing are supported.
If a variable is initialized with an Empty List [] and there are no conditions like 
- (1) attaching Type Annotation,
- (2) appending an element with a known type, or 
- (3) specifying as an argument of a function with a known argument type, the element type cannot be determined. 

Therefore, initialization with an Empty List [] is prohibited.

### Multiple Return Types
Python functions can return variables of different types, but in C++, the return type must be specified, making it impossible. Therefore, different Return Types are prohibited.
