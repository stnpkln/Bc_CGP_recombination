'''
File: functions.py
Purpose: generates data needed for the symbolic regression problems
Author: Petr Bromnik
'''

import numpy as np

training_set_1 = np.array([np.linspace(-1, 1, 20, dtype=float)])
training_set_2 = np.array([np.linspace(0, 2, 20, dtype=float)])
training_set_3 = np.array([np.linspace(0, 4, 20, dtype=float)])
training_set_4 = np.array([np.linspace(-1, 1, 100, dtype=float), np.linspace(-1, 1, 100, dtype=float)])

def koza_2(input):
	x = input[0]
	return x ** 5 - 2 * x ** 3 + x

koza_2_input = training_set_1
koza_2_wanted_output = koza_2(koza_2_input)

def koza_3(input):
	x = input[0]
	return x ** 6 - 2 * x ** 4 + x ** 2

koza_3_input = training_set_1
koza_3_wanted_output = koza_3(koza_3_input)

def nguyen_4(input):
	x = input[0]
	return x ** 6 + x ** 5 + x ** 4 + x ** 3 + x ** 2 + x

nguyen_4_input = training_set_1
nguyen_4_wanted_output = nguyen_4(nguyen_4_input)

def nguyen_5(input):
	x = input[0]
	return np.sin(x ** 2) * np.cos(x) - 1

nguyen_5_input = training_set_1
nguyen_5_wanted_output = nguyen_5(nguyen_5_input)

def nguyen_6(input):
	x = input[0]
	return np.sin(x) + np.sin(x + x ** 2)

nguyen_6_input = training_set_1
nguyen_6_wanted_output = nguyen_6(nguyen_6_input)

def nguyen_7(input):
	x = input[0]
	return np.log(x + 1) + np.log(x ** 2 + 1)

nguyen_7_input = training_set_2
nguyen_7_wanted_output = nguyen_7(nguyen_7_input)

def nguyen_8(input):
	x = input[0]
	return np.sqrt(x)

nguyen_8_input = training_set_3
nguyen_8_wanted_output = nguyen_8(nguyen_8_input)

def nguyen_9(input):
	x = input[0]
	y = input[1]
	return np.sin(x) + np.sin(y ** 2)

nguyen_9_input = training_set_4
nguyen_9_wanted_output = nguyen_9(nguyen_9_input)

def nguyen_10(input):
	x = input[0]
	y = input[1]
	return 2 * np.sin(x) * np.cos(y)

nguyen_10_input = training_set_4
nguyen_10_wanted_output = nguyen_10(nguyen_10_input)

functions = {
	'koza_3': {
		'function': koza_3,
		'input': koza_3_input,
		'wanted_output': koza_3_wanted_output,
		'n_inputs': 1,
		'name': 'Koza 3',
		'n_columns': 150,
		"mutation_rate": 0.07,
	},
	'nguyen_6': {
		'function': nguyen_6,
		'input': nguyen_6_input,
		'wanted_output': nguyen_6_wanted_output,
		'n_inputs': 1,
		'name': 'Nguyen 6',
		'n_columns': 100,
		"mutation_rate": 0.02,
	},
	'nguyen_8': {
		'function': nguyen_8,
		'input': nguyen_8_input,
		'wanted_output': nguyen_8_wanted_output,
		'n_inputs': 1,
		'name': 'Nguyen 8',
		'n_columns': 150,
		"mutation_rate": 0.15,
	},
	'nguyen_9': {
		'function': nguyen_9,
		'input': nguyen_9_input,
		'wanted_output': nguyen_9_wanted_output,
		'n_inputs': 2,
		'name': 'Nguyen 9',
		'n_columns': 150,
		"mutation_rate": 0.15,
	},
	'nguyen_10': {
		'function': nguyen_10,
		'input': nguyen_10_input,
		'wanted_output': nguyen_10_wanted_output,
		'n_inputs': 2,
		'name': 'Nguyen 10',
		'n_columns': 60,
		"mutation_rate": 0.2,
	}
}
