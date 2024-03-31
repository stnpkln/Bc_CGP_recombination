from typing import Callable, List

import numpy as np

from genome import evaluate_fitness, mutate_individual
from population import Population


def tournament_selection(population_size: int,
                        ncolumns: int,
                        nrows: int,
                        input_matrix: np.ndarray[np.ndarray[int | float]],
                        wanted_output: np.ndarray[float | int],
                        acceptable_boundary: int,
                        max_fitness_evaluations: int,
                        mutation_rate: int,
                        exchange_rate: int,
                        exchange_function: Callable) -> tuple[List[List[int]], float, int, int, List[dict]]:

    population = Population(population_size, ncolumns, nrows, mutation_rate, nparents=2)

    fitness_evaluations = 0
    generation = 0
    top_fitness = np.inf
    top_fitness_over_time = []
    while(fitness_evaluations < max_fitness_evaluations):
        fitness_evaluations += population_size
        generation += 1

        new_parent1, new_parent2, new_parent1_fitness, new_parent2_fitness = tournament(population, input_matrix, wanted_output, population_size, exchange_rate, exchange_function)
        fitness = new_parent1_fitness if new_parent1_fitness < new_parent2_fitness else new_parent2_fitness
        top_individual = new_parent1 if new_parent1_fitness < new_parent2_fitness else new_parent2

        if fitness < top_fitness:
            top_fitness = fitness
            top_fitness_over_time.append({"fitness": top_fitness, "generation": generation})

        # found an acceptable solution before max_fitness_evaluations was reached
        if fitness <= acceptable_boundary:
            break

    return top_individual, fitness, generation, fitness_evaluations, top_fitness_over_time
    
def tournament(population: Population, input_matrix: np.ndarray[np.ndarray[int | float]], wanted_output: np.ndarray[int | float], population_size: int, exchange_rate: float, exchange_function: Callable) -> tuple[List[List[int]], List[List[int]], float, float]:
    individual_indexes_shuffled = [individual_index for individual_index in range(population_size)]
    np.random.shuffle(individual_indexes_shuffled)

    group1 = individual_indexes_shuffled[2:]
    group2 = individual_indexes_shuffled[:2]
    
    parent_1_index, parent_1_fitness = get_best_group_individual(group1, population, input_matrix, wanted_output)
    parent_2_index, parent_2_fitness = get_best_group_individual(group2, population, input_matrix, wanted_output)
    parent_1 = population.get_individual(parent_1_index)
    parent_2 = population.get_individual(parent_2_index)

    generate_new_population(parent_1_index, parent_2_index, population, exchange_rate, exchange_function)

    return parent_1, parent_2, parent_1_fitness, parent_2_fitness

def get_best_group_individual(group: List[int], population: Population, input_matrix: np.ndarray[np.ndarray[int | float]], wanted_output: np.ndarray[int | float]) -> tuple[int, float]:
    best_individual_index = None
    best_fitness = np.inf

    for individual_index in group:
        individual, active_path = population.get_individual_with_active_path(individual_index)
        fitness = evaluate_fitness(genome=individual, input_matrix=input_matrix, wanted_output=wanted_output, genome_active_path_indexes=active_path)
        if fitness < best_fitness:
            best_fitness = fitness
            best_individual_index = individual_index

    return best_individual_index, best_fitness

def generate_new_population(new_parent_1_index: List[List[int]], new_parent_2_index: List[List[int]], population: Population, exchange_rate: float, exchange_function: Callable) -> None:
    '''[summary]
    Generates new children from the given parents and sets them to the population.
    ### Parameters
    1. new_parent1: List[List[int]]
        - parent genome
    2. new_parent2: List[List[int]]
        - parent genome
    3. population: Population
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

    population.set_parent(parent_1, parent_index=0)
    population.set_parent(parent_2, parent_index=1)
    population.set_children([child_1_mutated, child_2_mutated])

