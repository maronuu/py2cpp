from typing import List

from py2cpp import transpile


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


def main():
    cpp_src = transpile(sample_func, (List[float], int))
    print(cpp_src)


if __name__ == "__main__":
    main()
