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
    
    population = Population(population_size, ncolumns, nrows, mutation_rate)

    fitness_evaluations = 0
    generation = 0
    top_fitness = np.inf
    top_fitness_over_time = []
    while(fitness_evaluations < max_fitness_evaluations):
        fitness_evaluations += population_size
        generation += 1
        new_parent, fitness = get_fittest_individual(population, input_matrix, wanted_output)
        if fitness < top_fitness:
            top_fitness = fitness
            top_fitness_over_time.append({"fitness": top_fitness, "generation": generation})


        # found an acceptable solution before max_fitness_evaluations was reached
        if fitness <= acceptable_boundary:
            break

        generate_new_population(new_parent, population)
    
    return new_parent, fitness, generation, fitness_evaluations, top_fitness_over_time

def generate_new_population(new_parent: List[List[int]], population: Population) -> None:
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

    for i in range(n_children):
        new_child = mutate_individual(new_parent, population.ncolumns, population.nrows, population.mutation_rate)
        new_children.append(new_child)

    population.set_children(new_children)
    population.set_parent(new_parent)

def get_fittest_individual(population: Population, input_matrix: np.ndarray[np.ndarray[int | float]], wanted_output: np.ndarray[float | int]) -> tuple[List[List[int]], float]:
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
    parent, parent_active_path = population.get_parent_with_active_path()
    children_with_active_paths = population.get_children_with_active_paths()

    top_fitness = evaluate_fitness(parent, parent_active_path, input_matrix, wanted_output)
    top_individual = parent

    for child, child_active_path in children_with_active_paths:
        child_fitness = evaluate_fitness(child, child_active_path, input_matrix, wanted_output)
        # comparing fitness, the best fitness is the lowest
        if (child_fitness <= top_fitness):
            top_fitness = child_fitness
            top_individual = child

    return top_individual, top_fitness