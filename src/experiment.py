from typing import List
import pandas as pd
from sklearn.metrics import mean_squared_error
from constants.algorithmEnum import AlgorithmEnum, algorithm_names
from constants.functions import *
from evolution import evolve
from timeit import default_timer as timer
import multiprocessing
import uuid

from genome import genome_output
from utils import get_active_gene_indexes, get_output_gene_indexes

acceptable_boundary = 1e-30
max_fitness_evaluations = 1e3
runs_per_function = 6
single_function_runs = False
function_to_run = ""
def saveRun(algorithm: str, function: str, fitness_evaluations: int, generations: int, best_fitness: float, time: float, top_fitness_over_time: List[dict], run_id: str) -> None:
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
	5. best_fitness: float
		- fitness of the best individual
	6. time: float
		- time the algorithm took to run
	### Returns
	None
	'''
	general_header = ['run_id', 'algorithm', 'function', 'fitness_evaluations', 'generations', 'best_fitness', 'time']
	general_data = pd.DataFrame(columns=general_header)
	general_data.loc[len(general_data)] = {'run_id': run_id, 'algorithm': algorithm, 'function': function, 'generations': generations, 'fitness_evaluations': fitness_evaluations, 'best_fitness': best_fitness, 'time': time}
	with open('data-general.csv', 'a') as f:
		general_data.to_csv(f, header=False, index=False)

	run_details_header = ['run_id', 'generation', 'fitness']
	run_details = pd.DataFrame(columns=run_details_header, data=top_fitness_over_time)
	run_details['run_id'] = run_id
	with open('data-run-details.csv', 'a') as f:
		run_details.to_csv(f, header=False, index=False)

def runCGP(function: dict, algorithm: AlgorithmEnum) -> None:
	run_id = uuid.uuid4()
	seed = int(run_id) % 2**32 -1
	start = timer()

	population_size = 5 if algorithm == AlgorithmEnum.MUTATION_ONLY else 4
	solution, fitness, generations, fitness_evaluations, top_fitness_over_time = evolve(population_size=population_size,
																					 ncolumns=function['n_columns'],
																					 nrows=function['n_inputs'],
																					 input_matrix=function['input'],
																					 wanted_output=function['wanted_output'],
																					 acceptable_boundary=acceptable_boundary,
																					 max_fitness_evaluations=max_fitness_evaluations,
																					 mutation_rate=function['mutation_rate'],
																					 seed=seed,
																					 algorithm=algorithm)

	if fitness < acceptable_boundary:
		solution_active_path = get_active_gene_indexes(solution, get_output_gene_indexes(solution))
		solution_output = genome_output(solution, solution_active_path, function['input'])
		recalculated_fitness = mean_squared_error(function['wanted_output'], solution_output)
		if recalculated_fitness > acceptable_boundary:
			raise ValueError("recalculated fitness is not acceptable")

	end = timer()
	time = end - start
	algo_name = algorithm_names[algorithm]
	saveRun(algo_name, function['name'], fitness_evaluations, generations, fitness, time, top_fitness_over_time, str(run_id))

def runFunction(function_key: str) -> None:
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
		function = functions[function_to_run]
		runFunction(function)
	else:
		for function in functions:
			runFunction(function)

getCGPData()