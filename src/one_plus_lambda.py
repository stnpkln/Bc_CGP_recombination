'''
File: one_plus_lambda.py
Purpose: Contains the one plus lambda algorithm used in CGP
Author: Petr Bromnik
'''

import numpy as np

from genome import mutate_individual
from population import Population

def one_plus_lambda(population_size,
                    ncolumns,
                    nrows,
                    input_matrix,
                    wanted_output,
                    acceptable_boundary,
                    max_fitness_evaluations,
                    mutation_rate):
    '''[summary]
    Runs CGP with one plus lambda algorithm
    ### Parameters
    1. population_size
        - number of individuals in the population
    2. ncolumns
        - number of columns in the genome
    3. nrows
        - number of rows in the genome
    4. input_matrix
        - input_matrix data for the function
    5. wanted_output
        - expected output of the function
    6. acceptable_boundary
        - acceptable fitness value
    7. max_fitness_evaluations
        - maximum number of fitness evaluations to run the algorithm
    8. mutation_rate
        - mutation rate of the algorithm
    ### Returns
    1. List[List[int]]
        - best individual found
    2. float
        - fitness of the best individual
    3. int
        - number of generations the algorithm ran
    4. int
        - number of fitness evaluations the algorithm ran
    5. List[Dict[str, Union[float, int]]]
        - list of the best fitness over time
    6. bool
        - whether the solution was found
    '''

    population = Population(population_size, ncolumns, nrows, mutation_rate, input_matrix=input_matrix, wanted_output=wanted_output, max_error=acceptable_boundary)


    fitness_evaluations = 0
    generation = 0
    top_fitness = np.inf
    top_fitness_over_time = []
    found_solution = False
    while(fitness_evaluations < max_fitness_evaluations):
        generation += 1
        fitness_evaluations += population_size - 1
        new_parent_index, fitness = get_fittest_individual_index(population)

        # found an acceptable solution before max_fitness_evaluations was reached
        if population.solution_index != None:
            new_parent_index = population.solution_index
            found_solution = True
            top_fitness_over_time.append({"fitness": 0.0, "generation": generation})
            break

        if fitness < top_fitness:
            top_fitness = fitness
            top_fitness_over_time.append({"fitness": top_fitness, "generation": generation})

        generate_new_population(new_parent_index, population)
    
    top_individual = population.get_individual(new_parent_index)
    return top_individual, fitness, generation, fitness_evaluations, top_fitness_over_time, found_solution

def generate_new_population(new_parent_index, population):
    '''[summary]
    Generates new children from the given parent and sets them to the population.
    ### Parameters
    1. new_parent: List[List[int]]
        - parent genome
    2. population
        - population to set the children to
    ### Returns
    None
    '''
    n_children = len(population.children_indexes) # number of thildren to generate
    new_children = []
    new_parent = population.get_individual(new_parent_index)

    for i in range(n_children):
        new_child = mutate_individual(new_parent, population.ncolumns, population.nrows, population.mutation_rate)
        new_children.append(new_child)

    population.set_parent_by_index(new_parent_index) # parent first, as he can be one of the previous children
    population.set_children(new_children)

def get_fittest_individual_index(population):
    '''[summary]
    Returns the fittest individual from the given population.
    ### Parameters
    1. population
        - population to get the fittest individual from
    2. input_matrix
        - input_matrix data for the function
    3. wanted_output
        - expected output of the function
    ### Returns
    1. List[List[int]]
        - fittest individual
    2. float
        - fitness of the fittest individual
    '''
    parent_index = 0
    parent_fitness = population.get_parent_fitness()
    fittest_child_index, child_fitness = population.get_fittest_child_index()

    if child_fitness <= parent_fitness:
        return fittest_child_index, child_fitness

    return parent_index, parent_fitness