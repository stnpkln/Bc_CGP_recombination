'''
File: experiment.py
Purpose: Runs the CGP algorithm (parallel) on problems of symbolic regression
Author: Petr Bromnik
'''

import pandas as pd
from constants.algorithmEnum import AlgorithmEnum, algorithm_names
from constants.functions import *
from evolution import evolve
from timeit import default_timer as timer
import multiprocessing
import uuid

acceptable_boundary = 0.01 # acceptable difference between all every value of wanted output and the actual output
max_fitness_evaluations = 1e7 # maximum number of fitness evaluations to run the algorithm
runs_per_function = 10 # number of runs per function
single_function_runs = False # whether to run the algorithm on a single function
function_to_run = "nguyen_8" # function to run the algorithm on, if single_function_runs is True

def saveRun(algorithm, function, fitness_evaluations, generations, time, top_fitness_over_time, run_id, found_solution):
	'''[summary]
	Saves the run data to a pandas DataFrame
	### Parameters
	1. algorithm: str
		- name of the algorithm used
	2. function: str
		- name of the function used
	3. fitness_evaluations: int
		- number of fitness evaluations the algorithm ran
	4. generations: int
		- number of generations the algorithm ran
	6. time: float
		- time the algorithm took to run
	### Returns
	None
	'''
	general_header = ['run_id', 'algorithm', 'function', 'fitness_evaluations', 'generations', 'time', 'found_solution']
	general_data = pd.DataFrame(columns=general_header)
	general_data.loc[len(general_data)] = {'run_id': run_id, 'algorithm': algorithm, 'function': function, 'generations': generations, 'fitness_evaluations': fitness_evaluations, 'time': time, 'found_solution': found_solution}
	with open('data-general.csv', 'a') as f:
		general_data.to_csv(f, header=False, index=False)

	run_details_header = ['run_id', 'generation', 'fitness']
	run_details = pd.DataFrame(columns=run_details_header, data=top_fitness_over_time)
	run_details['run_id'] = run_id
	with open('data-run-details.csv', 'a') as f:
		run_details.to_csv(f, header=False, index=False)

def runCGP(function, algorithm) -> None:
	'''[summary]
	Runs the CGP algorithm on a specific function
	### Parameters
	1. function: dict
		- function to run the algorithm on
	2. algorithm: AlgorithmEnum
		- algorithm to run the function with
	### Returns
	None
	'''
	run_id = uuid.uuid4()
	seed = int(run_id) % 2**32 -1
	start = timer()

	function_name = function['name']

	population_size = 5 if algorithm == AlgorithmEnum.MUTATION_ONLY else 4
	try:
		*_, generations, fitness_evaluations, top_fitness_over_time, found_solution = evolve(population_size=population_size,
																											ncolumns=function['n_columns'],
																											nrows=function['n_inputs'],
																											input_matrix=function['input'],
																											wanted_output=function['wanted_output'],
																											acceptable_boundary=acceptable_boundary,
																											max_fitness_evaluations=max_fitness_evaluations,
																											mutation_rate=function['mutation_rate'],
																											seed=seed,
																											algorithm=algorithm)

		end = timer()
		time = end - start
		algo_name = algorithm_names[algorithm]

	except Exception as e:
		print(e)
		fitness_evaluations = generations = time = 0
		top_fitness_over_time = []
		algo_name = algorithm_names[algorithm]
		function_name = function_name + " ERROR"

	saveRun(algo_name, function['name'], fitness_evaluations, generations, time, top_fitness_over_time, str(run_id), found_solution)

def runFunction(function_key) -> None:
	'''[summary]
	Runs the CGP algorithm on a specific function
	### Parameters
	1. function_key: str
		- name of the function to run
	### Returns
	None
	'''
	for algorithm in AlgorithmEnum:
		for _ in range(runs_per_function):
			run = multiprocessing.Process(target=runCGP, args=(functions[function_key], algorithm,))
			run.start()

def getCGPData() -> None:
	'''[summary]
	Runs the CGP algorithm on all functions in the constants/functions.py file
	### Returns
	None
	'''
	if single_function_runs:
		runFunction(function_to_run)
	else:
		for function in functions:
			runFunction(function)

# getCGPData()