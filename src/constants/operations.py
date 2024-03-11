import math
import numpy as np

# toodo add e^n and ln(|x|) to operations, so far they break the program
operations = ['+', '-', '*', '%', 'sin', 'cos', 'e^n']
op_inputs = {
	'+': 2,
	'-': 2,
	'*': 2,
	'%': 2,
	'sin': 1,
	'cos': 1,
	'e^n': 1,
	'ln(|x|)': 1,
}

# max float64 value is 1.7976931348623157e+308
op_functions = {
	'+': lambda x, y: np.add(x, y, where=(x < 1e+300) & (y < 1e+300)),
	'-': lambda x, y: np.subtract(x, y, where=(x < 1e+300) & (y < 1e+300)),
	'*': lambda x, y: np.multiply(x, y, where=(x < 1e+300) & (y < 1e+300)),
	'%': lambda x, y: np.mod(x, y, where=(y != 0)), # mod is not defined for y = 0
	'sin': lambda x: np.sin(x),
	'cos': lambda x: np.cos(x),
	# max float64 value is 1.7976931348623157e+308, so e^x is not defined for x > 709.782712893384 (ln(1.7976931348623157e+308) = 709.782712893384)
	# max was set to 100 to avoid overflow when calculationg fitness
	'e^n': lambda x: np.exp(x, where=(x <= 100)),
	'ln(|x|)': lambda x: np.log(np.absolute(x), where=(x != 0)),
}