double sample_func(double *a, int n) {
	// definitions
    // define int variable
	int i = 0;
	// define double variable
	double out = 1.23;
	// define bool variable
	bool flag = true;
	// define array of int
	int array_int[5] = {1, 2, 3, 4, 5};
	// define array of double
	double array_float[3] = {1.23, 4.56, 7.89};
	
	// arithmetics
	// int
	i = (1 + ((2 - 3) * 4));
	i = ((4 / 2) + (5 % 3));
	i = (-2);
	// double
	out = (1.2 + (((3.4 - 5.6) * 7.8) / 9.0));
	out = (-1.0);
	// int and double
	out = ((1 + 2.0) + (((3 - 4.0) * 5) / 6.0));
	
	// Assign, AugAssign
	// int
	i += 1;
	i -= 2;
	i *= 3;
	i /= 4;
	i %= 5;
	// double
	out += (-1.0);
	out -= 2.0;
	out *= 3.0;
	out /= 4.0;
	
	// Array Operations
	// write
	array_int[1] = 100;
	array_float[2] = 123.456;
	// read
	i = (array_int[0] + array_int[1]);
	out = (array_float[0] + array_float[2]);
	
	// Boolean / Logical Operators
	bool is_ok = true;
	bool is_ng = false;
	// OR
	if (is_ok || is_ng) {
		return (1.0 + 1);
	}
	// AND, NOT
	if (is_ok && (!is_ng)) {
		return out;
	}

	// Nested Comparisons
	if (((i == 1) && (out == 1.0)) || (out != 2.0)) {
		out += 1.0;
	}
	// Multiple Comparisons
	if ((i == 1) && (out == 1.0) && (out != 2.0)) {
		out += 1.0;
	}
	// Multiple Comparators
	if (1 < 2 && 2 < i && i < 4 && 4 <= 6) {
		out += 1.0;
	}
	// Multiple Comparators (rare case)
	if (1 > (-1) && (-1) < i && i >= 100) {
		out += 1.0;
	}

	// while statement
	i = 0;
	while (i < n) {
		out += a[i];
		i += 1;
	}

	// function call
	sample_func(array_float, 3);
	return out;
}

