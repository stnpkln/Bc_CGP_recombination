from typing import List
from population import Population
from genome import evaluate_fitness, mutate_individual

def evolve(population_size, ncolumns, nrows, input, wanted_output, acceptable_boundary, max_generations):
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
    4. input: List[List[int]]
        - input data for the function
        - must not be empty
    5. wanted_output: List[int]
        - expected output of the function
        - must not be empty
    6. acceptable_boundary: float
        - acceptable fitness value
        - must be >= 0
    7. max_generations: int
        - maximum number of generations to run the algorithm
        - must be >= 1
    ### Returns
    1. List[List[int]]
        - best individual found
    2. float
        - fitness of the best individual
    3. int
        - number of generations the algorithm ran
    Raises
    ------
    ValueError
        - if population_size < 1
        - if nrows < 1
        - if ncolumns < 3
        - if len(input) == 0
        - if len(wanted_output) == 0
        - if len(input) != len(wanted_output)
        - if acceptable_boundary < 0
    '''
    if len(input) == 0:
        raise ValueError("input must not be empty")
    if len(wanted_output) == 0:
        raise ValueError("wanted_output must not be empty")
    if len(input) != len(wanted_output):
        raise ValueError("input and wanted_output must have the same length")
    if acceptable_boundary < 0:
        raise ValueError("acceptable_boundary must be >= 0")

    population = Population(population_size, ncolumns, nrows)

    for generation in range(max_generations):
        new_parent, fitness = get_fittest_individual(population, input, wanted_output)
        
        # found an acceptable solution before max_generations was reached
        if fitness < acceptable_boundary:
            break

        generate_new_population(new_parent, population)
    
    return new_parent, fitness, generation

def generate_new_population(new_parent: List[List[int]], population: Population):
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
        new_child = mutate_individual(new_parent, population.ncolumns, population.nrows)
        new_children.append(new_child)

    population.set_children(new_children)
    population.set_parent(new_parent)

def get_fittest_individual(population: Population, input: List[List[int]], wanted_output: List[int]):
    '''[summary]
    Returns the fittest individual from the given population.
    ### Parameters
    1. population: Population
        - population to get the fittest individual from
    2. input: List[List[int]]
        - input data for the function
    3. wanted_output: List[int]
        - expected output of the function
    ### Returns
    1. List[List[int]]
        - fittest individual
    2. float
        - fitness of the fittest individual
    '''
    parent = population.get_parent()
    children = population.get_children()

    top_fitness = evaluate_fitness(parent, input, wanted_output)
    top_individual = parent

    for child in children:
        child_fitness = evaluate_fitness(child, input, wanted_output)
        # comparing fitness, the best fitness is the lowest
        if (child_fitness <= top_fitness):
            top_fitness = child_fitness
            top_individual = child

    return top_individual, top_fitness