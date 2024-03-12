import pandas as pd
from constants.functions import *
from evolution import evolve
from timeit import default_timer as timer

from genome import genome_output

runs_per_function = 1
acceptable_boundary = 1e-30
max_generations = 100000
data = pd.DataFrame(columns=['algorithm', 'function', 'fitness_evaluations', 'generations', 'best_fitness', 'time'])
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
	data.loc[len(data)] = {'algorithm': algorithm, 'function': function, 'generations': generations, 'fitness_evaluations': fitness_evaluations, 'best_fitness': best_fitness, 'time': time}

def runCGP(function: dict) -> None:
	start = timer()

	_, fitness, generations, fitness_evaluations = evolve(population_size=5, ncolumns=function['n_columns'], nrows=function['n_inputs'], input_matrix=function['input'], wanted_output=function['wanted_output'], acceptable_boundary=acceptable_boundary, max_generations=max_generations, mutation_rate=function['mutation_rate'])
	
	end = timer()
	time = end - start
	saveRun('1 + lambda', function['name'], fitness_evaluations, generations, fitness, time)

def runFunction(function: dict) -> None:
	for i in range(runs_per_function):
		runCGP(function)

def getCGPData() -> None:
	'''[summary]
	Runs the CGP algorithm on all functions in the constants/functions.py file
	### Returns
	None
	'''
	for function in functions:
		runFunction(functions[function])

getCGPData()
data.to_csv('data.csv')
