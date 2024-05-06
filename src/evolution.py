'''
File: evolution.py
Purpose: Contains the evolve function that runs the CGP algorithm
Author: Petr Bromnik
'''

from one_plus_lambda import one_plus_lambda

from genome import active_gene_transplant, subgraph_exchange
import numpy as np
from constants.functions import *
from tournament_selection import tournament_selection
from constants.algorithmEnum import AlgorithmEnum

def evolve(population_size,
           ncolumns,
           nrows,
           input_matrix,
           wanted_output,
           acceptable_boundary,
           max_fitness_evaluations,
           mutation_rate,
           seed = None,
           algorithm = AlgorithmEnum.MUTATION_ONLY,
           exchange_rate = 0.5):
    '''[summary]
    Runs the 1 + lambda evolutionary algorithm to find a genome that solves the given problem.
    ### Parameters
    1. pupulation_size: int
        - number of individuals in the population
        - must be >= 1
    2. ncolumns: int
        - number of columns in the genome
        - must be >= 3
    3. nrows: int
        - number of rows in the genome
        - must be >= 1
    4. input_matrix: np.ndarray[np.ndarray[int | float]]
        - input_matrix data for the function
        - must not be empty
    5. wanted_output: np.ndarray[float | int]
        - expected output of the function
        - must not be empty
    6. acceptable_boundary: float
        - acceptable fitness value
        - must be >= 0
    7. max_fitness_evaluations: int
        - maximum number of fitness evaluations to run the algorithm
        - must be >= 1
    8. mutation_rate: float
        - mutation rate of the algorithm
        - must be >= 0 and <= 1
    9. seed: int
        - seed for the random number generator
        - default None
    10. algorithm: AlgorithmEnum
        - algorithm to be run
        - default MUTATION_ONLY
    11. exchange_rate: float
        - exchange rate of the algorithm
        - default 0.5
    ### Returns
    1. List[List[int]]
        - best individual found
    2. float
        - fitness of the best individual
    3. int
        - number of generations the algorithm ran
    4. int
        - number of fitness evaluations the algorithm ran
    5. List[dict]
        - list of dictionaries containing the top fitness and generation at each generation
        - [{"fitness": float, "generation": int}]
    Raises
    ------
    ValueError
        - if population_size < 1
        - if nrows < 1
        - if ncolumns < 3
        - if len(input_matrix) == 0
        - if len(wanted_output) == 0
        - if len(input matrix row) != len(wanted_output)
        - if acceptable_boundary < 0
    '''
    if len(input_matrix) == 0:
        raise ValueError("input_matrix must not be empty")
    if len(wanted_output) == 0:
        raise ValueError("wanted_output must not be empty")
    for input_row in input_matrix:
        if len(input_row) != len(wanted_output):
            raise ValueError("input_row and wanted_output must have the same length")
    if acceptable_boundary < 0:
        raise ValueError("acceptable_boundary must be >= 0")
    if mutation_rate < 0 or mutation_rate > 1:
        raise ValueError("mutation_rate must be >= 0 and <= 1")
    
    if (seed):
        np.random.seed(seed)

    if (algorithm == AlgorithmEnum.MUTATION_ONLY):
        return one_plus_lambda(population_size,
                        ncolumns,
                        nrows,
                        input_matrix,
                        wanted_output,
                        acceptable_boundary,
                        max_fitness_evaluations,
                        mutation_rate)
    elif (algorithm == AlgorithmEnum.SUBGRAPH_EXCHANGE):
        return tournament_selection(population_size,
                        ncolumns,
                        nrows,
                        input_matrix,
                        wanted_output,
                        acceptable_boundary,
                        max_fitness_evaluations,
                        mutation_rate,
                        exchange_rate,
                        exchange_function=subgraph_exchange)
    elif (algorithm ==  AlgorithmEnum.PASSIVE_ACTIVE_IMPLANTATION):
                return tournament_selection(population_size,
                        ncolumns,
                        nrows,
                        input_matrix,
                        wanted_output,
                        acceptable_boundary,
                        max_fitness_evaluations,
                        mutation_rate,
                        exchange_rate,
                        exchange_function=active_gene_transplant)
    else:
        raise ValueError("Unknown algorithm type")
