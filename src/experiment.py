import pandas as pd
from sklearn.metrics import mean_squared_error
from constants.functions import *
from evolution import evolve
from timeit import default_timer as timer
import multiprocessing

from genome import genome_output
from utils import get_active_gene_indexes, get_output_gene_indexes

acceptable_boundary = 1e-30
max_fitness_evaluations = 1e5
def saveRun(algorithm: str, function: str, fitness_evaluations: int, generations: int, best_fitness: float, time: float) -> None:
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
	header = ['algorithm', 'function', 'fitness_evaluations', 'generations', 'best_fitness', 'time']
	data = pd.DataFrame(columns=header)
	data.loc[len(data)] = {'algorithm': algorithm, 'function': function, 'generations': generations, 'fitness_evaluations': fitness_evaluations, 'best_fitness': best_fitness, 'time': time}
	with open('data.csv', 'a') as f:
		data.to_csv(f, header=f.tell()==0)

def runCGP(function: dict) -> None:
	start = timer()

	solution, fitness, generations, fitness_evaluations = evolve(population_size=5, ncolumns=function['n_columns'], nrows=function['n_inputs'], input_matrix=function['input'], wanted_output=function['wanted_output'], acceptable_boundary=acceptable_boundary, max_fitness_evaluations=max_fitness_evaluations, mutation_rate=function['mutation_rate'])

	if fitness < acceptable_boundary:
		solution_active_path = get_active_gene_indexes(solution, get_output_gene_indexes(solution))
		solution_output = genome_output(solution, solution_active_path, function['input'])
		recalculated_fitness = mean_squared_error(function['wanted_output'], solution_output)
		if recalculated_fitness > acceptable_boundary:
			print(f"recalculated fitness: {recalculated_fitness}")
			print(f"original fitness: {fitness}")
			print(f"found solution in {fitness_evaluations} fitness evaluations")
			print(f"wanted output: {function['wanted_output']}")
			print(f"found output: {solution_output}")
			print(f"active path: {solution_active_path}")
			print(f"genome: {solution}")
			raise ValueError("recalculated fitness is not acceptable")

	end = timer()
	time = end - start
	saveRun('1 + lambda', function['name'], fitness_evaluations, generations, fitness, time)

def getCGPData() -> None:
	'''[summary]
	Runs the CGP algorithm on all functions in the constants/functions.py file
	### Returns
	None
	'''
	for function in functions:
		run = multiprocessing.Process(target=runCGP, args=(functions[function],))
		run.start()

getCGPData()