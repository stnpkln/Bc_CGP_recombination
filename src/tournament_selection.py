'''
File: tournament_selection.py
Purpose: Contains the tournament selection algorithm used in CGP
Author: Petr Bromnik
'''

import numpy as np

from genome import mutate_individual
from population import Population


def tournament_selection(population_size,
                        ncolumns,
                        nrows,
                        input_matrix,
                        wanted_output,
                        acceptable_boundary,
                        max_fitness_evaluations,
                        mutation_rate,
                        exchange_rate,
                        exchange_function):
    '''[summary]
    Runs CGP with tournament selection algorithm
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
    9. exchange_rate
        - exchange rate of the algorithm
    10. exchange_function
        - function to exchange genes
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

    population = Population(population_size, ncolumns, nrows, mutation_rate, input_matrix=input_matrix, wanted_output=wanted_output, nparents=2, max_error=acceptable_boundary)

    fitness_evaluations = 0
    generation = 0
    top_fitness = np.inf
    top_fitness_over_time = []
    found_solution = False
    while(fitness_evaluations < max_fitness_evaluations):
        generation += 1
        fitness_evaluations += population_size - 2

        new_parent1, new_parent2, new_parent1_fitness, new_parent2_fitness = tournament(population, population_size, exchange_rate, exchange_function)
        fitness = new_parent1_fitness if new_parent1_fitness < new_parent2_fitness else new_parent2_fitness
        top_individual = new_parent1 if new_parent1_fitness < new_parent2_fitness else new_parent2

        # found an acceptable solution before max_fitness_evaluations was reached
        if population.solution_index != None:
            found_solution = True
            top_fitness_over_time.append({"fitness": 0.0, "generation": generation})
            break

        if fitness < top_fitness:
            top_fitness = fitness
            top_fitness_over_time.append({"fitness": top_fitness, "generation": generation})

    if population.solution_index != None:
        top_individual = population.get_individual(population.solution_index)
        fitness = population.get_fitness(population.solution_index)

    return top_individual, fitness, generation, fitness_evaluations, top_fitness_over_time, found_solution
    
def tournament(population, population_size, exchange_rate, exchange_function):
    '''[summary]
    Runs the tournament selection algorithm
    ### Parameters
    1. population
        - population to run the tournament on
    2. population_size
        - number of individuals in the population
    3. exchange_rate
        - exchange rate of the algorithm
    4. exchange_function
        - function to exchange genes
    ### Returns
    1. List[List[int]]
        - parent 1 genome
    2. List[List[int]]
        - parent 2 genome
    3. float
        - fitness of parent 1
    4. float
        - fitness of parent 2
    '''
    individual_indexes_shuffled = [individual_index for individual_index in range(population_size)]
    np.random.shuffle(individual_indexes_shuffled)

    group1 = individual_indexes_shuffled[2:]
    group2 = individual_indexes_shuffled[:2]
    
    parent_1_index, parent_1_fitness = get_best_group_individual(group1, population)
    parent_2_index, parent_2_fitness = get_best_group_individual(group2, population)
    parent_1 = population.get_individual(parent_1_index)
    parent_2 = population.get_individual(parent_2_index)

    generate_new_population(parent_1_index, parent_2_index, population, exchange_rate, exchange_function)

    return parent_1, parent_2, parent_1_fitness, parent_2_fitness

def get_best_group_individual(group, population):
    best_individual_index = None
    best_fitness = np.inf

    for individual_index in group:
        fitness = population.get_fitness(individual_index)
        if fitness < best_fitness:
            best_fitness = fitness
            best_individual_index = individual_index

    return best_individual_index, best_fitness

def generate_new_population(new_parent_1_index, new_parent_2_index, population, exchange_rate, exchange_function):
    '''[summary]
    Generates new children from the given parents and sets them to the population.
    ### Parameters
    1. new_parent1
        - parent genome
    2. new_parent2
        - parent genome
    3. population
        - population to set the children to
    ### Returns
    None
    '''
    parent_1, parent_1_active_path = population.get_individual_with_active_path(new_parent_1_index)
    parent_2, parent_2_active_path = population.get_individual_with_active_path(new_parent_2_index)

    child_1 = exchange_function(parent_1, parent_1_active_path, parent_2, parent_2_active_path, exchange_rate, population.nrows)
    child_2 = exchange_function(parent_2, parent_2_active_path, parent_1, parent_1_active_path, exchange_rate, population.nrows)

    child_1_mutated = mutate_individual(child_1, population.ncolumns, population.nrows, population.mutation_rate)
    child_2_mutated = mutate_individual(child_2, population.ncolumns, population.nrows, population.mutation_rate)

    population.set_parents_by_indexes(new_parent_1_index, new_parent_2_index) # parents first, as they can be one of the previous children
    population.set_children([child_1_mutated, child_2_mutated])