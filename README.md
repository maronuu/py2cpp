# py2cpp

## What
A transpiler that converts a Python function into a C++ function. Only subset of Python spec is supported.

## Usage
```bash
$ cd example
$ python sample.py > result.cpp
```
`example/result_with_comment.cpp` is the output `result.cpp` with added comments.

The following python function is converted into a c++ function:
```python
def sample_func(a, n):
    ### definitions
    ## define int variable
    i = 0
    ## define float variable
    out = 1.23
    ## define bool variable
    flag = True
    ## define list of int
    array_int = [1, 2, 3, 4, 5]
    ## define list of float
    array_float = [1.23, 4.56, 7.89]

    ### arithmetics
    ## int
    i = 1 + (2 - 3) * 4
    i = 4 // 2 + 5 % 3
    i = -2
    ## float
    out = 1.2 + (3.4 - 5.6) * 7.8 / 9.0
    out = -1.0
    ## int and float
    out = 1 + 2.0 + (3 - 4.0) * 5 / 6.0

    ### Assign/AugAssign
    ## int
    i += 1
    i -= 2
    i *= 3
    i //= 4
    i %= 5
    ## float
    out += -1.0
    out -= 2.0
    out *= 3.0
    out /= 4.0

    ### Array Operations
    array_int[1] = 100
    array_float[2] = 123.456
    i = array_int[0] + array_int[1]
    out = array_float[0] + array_float[2]

    ### Boolean / Logical Operations
    is_ok = True
    is_ng = False
    ## And, Not, Or
    if is_ok or is_ng:
        return 1.0 + 1
    if is_ok and not is_ng:
        return out

    # Nested Comparisons
    if i == 1 and out == 1.0 or out != 2.0:
        out += 1.0
    # Multiple Comparisons
    if i == 1 and out == 1.0 and out != 2.0:
        out += 1.0
    # Multiple Comparators
    if 1 < 2 < i < 4 <= 6:
        out += 1.0
    # Multiple Comparators (rare case)
    if 1 > -1 < i >= 100:
        out += 1.0

    ### While Statement
    i = 0
    while i < n:
        out += a[i]
        i += 1

    ### Func Call
    sample_func(array_float, 3)

    return out
```

The result of transpile:
```cpp
double sample_func(double *a, int n) {
    int i = 0;
    double out = 1.23;
    bool flag = true;
    int array_int[5] = {1, 2, 3, 4, 5};
    double array_float[3] = {1.23, 4.56, 7.89};
    i = (1 + ((2 - 3) * 4));
    i = ((4 / 2) + (5 % 3));
    i = (-2);
    out = (1.2 + (((3.4 - 5.6) * 7.8) / 9.0));
    out = (-1.0);
    out = ((1 + 2.0) + (((3 - 4.0) * 5) / 6.0));
    i += 1;
    i -= 2;
    i *= 3;
    i /= 4;
    i %= 5;
    out += (-1.0);
    out -= 2.0;
    out *= 3.0;
    out /= 4.0;
    array_int[1] = 100;
    array_float[2] = 123.456;
    i = (array_int[0] + array_int[1]);
    out = (array_float[0] + array_float[2]);
    bool is_ok = true;
    bool is_ng = false;
    if (is_ok || is_ng) {
        return (1.0 + 1);
    }
    if (is_ok && (!is_ng)) {
        return out;
    }
    if (((i == 1) && (out == 1.0)) || (out != 2.0)) {
        out += 1.0;
    }
    if ((i == 1) && (out == 1.0) && (out != 2.0)) {
        out += 1.0;
    }
    if (1 < 2 && 2 < i && i < 4 && 4 <= 6) {
        out += 1.0;
    }
    if (1 > (-1) && (-1) < i && i >= 100) {
        out += 1.0;
    }
    i = 0;
    while (i < n) {
        out += a[i];
        i += 1;
    }
    sample_func(array_float, 3);
    return out;
}
```

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
