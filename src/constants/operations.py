'''
File: operations.py
Purpose: Contains the operations used in the CGP algorithm
Author: Petr Bromnik
'''

import numpy as np

operations = ['+', '-', '*', '%', 'sin', 'cos', 'e^n', 'ln(|x|)']
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
# max was set to 1e+30 to avoid overflow when calculationg fitness - for example 1e100 * 1e100 = 1e200, when squared in fitness calculation it would be 1e400 whis is > than max float64 value 
op_functions = {
	'+': lambda x, y: np.add(x, y, where=(x < 1e+30) & (x > -1e30) & (y < 1e+30) & (y > -1e30)),
	'-': lambda x, y: np.subtract(x, y, where=(x < 1e+30) & (x > -1e30) & (y < 1e+30) & (y > -1e30)),
	'*': lambda x, y: np.multiply(x, y, where=(x < 1e+30) & (x > -1e30) & (y < 1e+30) & (y > -1e30)),
	'%': lambda x, y: np.mod(x, y, where=(y != 0)), # mod is not defined for y = 0
	'sin': lambda x: np.sin(x),
	'cos': lambda x: np.cos(x),
	'e^n': lambda x: np.exp(x, where=(x <= 50)),
	'ln(|x|)': lambda x: np.log(np.absolute(x), where=(x != 0)),
}