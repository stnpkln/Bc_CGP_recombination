from typing import List

import numpy as np

from genome import evaluate_fitness, mutate_individual
from population import Population

def one_plus_lambda(population_size: int,
                    ncolumns: int,
                    nrows: int,
                    input_matrix: np.ndarray[np.ndarray[int | float]],
                    wanted_output: np.ndarray[float | int],
                    acceptable_boundary: int,
                    max_fitness_evaluations: int,
                    mutation_rate: int) -> tuple[List[List[int]], float, int, int, List[dict]]:
    
    population = Population(population_size, ncolumns, nrows, mutation_rate, input_matrix=input_matrix, wanted_output=wanted_output)

    fitness_evaluations = 0
    generation = 0
    top_fitness = np.inf
    top_fitness_over_time = []
    while(fitness_evaluations < max_fitness_evaluations):
        generation += 1
        new_parent_index, fitness = get_fittest_individual_index(population)
        if fitness < top_fitness:
            top_fitness = fitness
            top_fitness_over_time.append({"fitness": top_fitness, "generation": generation})

        # found an acceptable solution before max_fitness_evaluations was reached
        if fitness <= acceptable_boundary:
            break

        generate_new_population(new_parent_index, population)
        fitness_evaluations += population.fitness_evaluations
    
    top_individual = population.get_individual(new_parent_index)
    return top_individual, fitness, generation, fitness_evaluations, top_fitness_over_time

def generate_new_population(new_parent_index: int, population: Population) -> None:
    '''[summary]
    Generates new children from the given parent and sets them to the population.
    ### Parameters
    1. new_parent: List[List[int]]
        - parent genome
    2. population: Population
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

def get_fittest_individual_index(population: Population) -> tuple[int, float]:
    '''[summary]
    Returns the fittest individual from the given population.
    ### Parameters
    1. population: Population
        - population to get the fittest individual from
    2. input_matrix: np.ndarray[np.ndarray[int | float]]
        - input_matrix data for the function
    3. wanted_output: np.ndarray[float | int]
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