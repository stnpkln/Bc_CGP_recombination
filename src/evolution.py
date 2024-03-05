from typing import List
from population import Population
from genome import evaluate_fitness, mutate_individual

def evolve(population_size, ncolumns, nrows, input, wanted_output, acceptable_boundary, max_generations):
    population = Population(population_size, ncolumns, nrows)

    for generation in range(max_generations):
        new_parent, fitness = get_fittest_individual(population, input, wanted_output)
        
        if fitness < acceptable_boundary:
            print(f"i found the solution in generation: {generation}!")
            break

        generate_new_children(new_parent, population)
    
    return new_parent, fitness, generation

def generate_new_children(new_parent: List[List[int]], population: Population):
    n_children = len(population.children_indexes)
    new_children = []

    for i in range(n_children):
        new_child = mutate_individual(new_parent, population.ncolumns, population.nrows)
        new_children.append(new_child)

    population.set_children(new_children)
    population.set_parent(new_parent)

def get_fittest_individual(population: Population, input: List[List[int]], wanted_output: List[int]):
    parent = population.get_parent()
    children = population.get_children()

    top_fitness = evaluate_fitness(parent, input, wanted_output)
    top_individual = parent

    for child in children:
        child_fitness = evaluate_fitness(child, input, wanted_output)
        if (child_fitness <= top_fitness):
            top_fitness = child_fitness
            top_individual = child

    return top_individual, top_fitness