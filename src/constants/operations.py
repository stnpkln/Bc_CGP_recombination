import math
import numpy as np

# toodo add e^n and ln(|x|) to operations, so far they break the program
operations = ['+', '-', '*', '%', 'sin', 'cos']
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

op_functions = {
	'+': lambda x, y: x + y,
	'-': lambda x, y: x - y,
	'*': lambda x, y: x * y,
	'%': lambda x, y: np.mod(x, y, where=(y != 0)),
	'sin': lambda x: np.sin(x),
	'cos': lambda x: np.cos(x),
	'e^n': lambda x: np.exp(x),
	'ln(|x|)': lambda x: np.log(np.absolute(x), where=(x != 0)),
}
