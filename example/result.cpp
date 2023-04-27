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

