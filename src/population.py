'''
File: population.py
Purpose: Contains the Population class used in the CGP algorithm
Author: Petr Bromnik
'''

from constants.operations import operations
from genome import evaluate_fitness
from utils import get_active_gene_indexes, get_last_possible_input_index, get_number_of_gene_inputs, get_output_gene_indexes
import numpy as np

class Population:
    def __init__(self, population_size, ncolumns, nrows, mutation_rate, input_matrix, wanted_output, nparents = 1, max_error = 0.01):
        '''[summary]
        Initializes the population with random genomes.
        ### Parameters
        1. population_size
            - number of individuals in the population
            - must be >= 1
        2. ncolumns
            - number of columns in the genome
            - must be >= 3
        3. nrows
            - number of rows in the genome
            - must be >= 1
        4. mutation_rate
            - mutation rate of the algorithm
            - must be >= 0 and <= 1
        ### Raises
        ------
        ValueError
            - if population_size < 1
            - if nrows < 1
            - if ncolumns < 3
        '''
        if population_size < 1:
            raise ValueError("population_size must be >= 1")
        if nrows < 1:
            raise ValueError("nrows must be >= 1")
        if ncolumns < 3:
            raise ValueError("ncolumns must be >= 3")
        if mutation_rate < 0 or mutation_rate > 1:
            raise ValueError("mutation_rate must be >= 0 and <= 1")

        self.nrows = nrows
        self.ncolumns = ncolumns
        self.population = self.get_starting_popultation(population_size)
        self.nparents = nparents
        self.children_indexes = [i for i in range(nparents, population_size)] # 1 becouse its only for children (minus parent with index 0)
        self.mutation_rate = mutation_rate
        self.active_paths = [[] for i in range(population_size)]
        self.fitnesses = [np.inf for i in range(population_size)]
        self.input_matrix = input_matrix
        self.wanted_output = wanted_output
        self.population_size = population_size
        self.max_error = max_error
        self.solution_index = None
        self.reset_all_active_paths()
        self.calculate_fitness_all()

    def get_starting_popultation(self, population_size):
        '''[summary]
        Returns a list of random genomes (population).
        ### Parameters
        1. population_size
            - number of individuals in the population
            - must be >= 1
        ### Returns
        List[List[List[int]]]
            - list of random genomes
        '''
        population = []
        for i in range(population_size):
            population.append(self.get_random_genome())
        return population

    def get_random_genome(self):
        '''[summary]
        Returns a random genome (individual).
        ### Returns
        List[List[int]]
            - random genome
        '''
        genome = []
        for column in range(self.ncolumns):
            for row in range(self.nrows):
                genome.append(self.get_random_gene(row, column, genome))

        return genome


    def get_random_gene(self, rowIndex, columnIndex, genome):
        '''[summary]
        Returns a random gene.
        ### Parameters
        1. rowIndex
            - index of the row in the genome
            - must be >= 0
        2. columnIndex
            - index of the column in the genome
            - must be >= 0
        3. genome
            - genome the gene is to be part of
        ### Returns
        List[int]
            - random gene
        '''
        if rowIndex < 0:
            raise ValueError("rowIndex must be >= 0")
        if columnIndex < 0:
            raise ValueError("columnIndex must be >= 0")

        # input genes, internally represented as [-1, -1, -1]
        gene = [-1, -1, -1]
        if (columnIndex == 0):
            return gene
        
        # output gene, internally represented as [-2, input_index, -2]
        if ((columnIndex == self.ncolumns - 1) and (rowIndex == self.nrows - 1)):
            return [-2, np.random.randint(0, len(genome) - rowIndex), -2]

        # function genes
        operation = np.random.randint(0, len(operations))
        gene[0] = operation

        # generating random inputs
        gene_index = len(genome)
        last_possible_input = get_last_possible_input_index(self.ncolumns, self.nrows, gene_index)
        for i in range(get_number_of_gene_inputs(gene)):
            input = np.random.randint(0, last_possible_input)
            gene[i + 1] = input # to skip operation gene
        
        return gene

    def get_population(self):
        '''[summary]
        ### Returns
        List[List[List[int]]]
            - population
        '''
        return self.population

    def get_individual(self, index):
        '''[summary]
        Returns an individual from the population.
        ### Parameters
        1. index
            - index of the individual
            - must be >= 0
        ### Returns
        List[int]
            - individual
        '''
        if index < 0:
            raise ValueError("index must be >= 0")

        return self.population[index]
    
    def set_individual(self, index, individual):
        '''[summary]
        Sets an individual in the population.
        ### Parameters
        1. index
            - index of the individual
            - must be >= 0
        2. individual
            - individual to set
        ### Returns
        None
        '''
        if index < 0:
            raise ValueError("index must be >= 0")

        self.population[index] = individual
        self.reset_active_path(index)
        self.calculate_fitness(index)

    def get_parent(self, parent_index = 0):
        '''[summary]
        Returns the parent of the population.
        ### Returns
        List[List[int]]
            - parent genome
        '''
        if parent_index >= self.nparents:
            raise ValueError("Parent index out of range")

        return self.population[parent_index]
    
    def get_parent_with_active_path(self, parent_index = 0):
        return (self.get_parent(), self.get_active_path(parent_index))
    
    def set_parent(self, new_parent, parent_index = 0):
        '''[summary]
        Sets the parent of the population.
        ### Parameters
        1. new_parent
            - new parent genome
        ### Returns
        None
        '''
        if parent_index >= self.nparents:
            raise ValueError("Parent index out of range")
    
        self.population[parent_index] = new_parent
        self.reset_active_path(parent_index)
        self.calculate_fitness(parent_index)
    
    def get_children(self):
        '''[summary]
        Returns the children of the population.
        ### Returns
        List[List[List[int]]]
            - children genomes
        '''
        children = []
        for child_index in self.children_indexes:
            children.append(self.population[child_index])
        return children
    
    def get_children_with_active_paths(self):
        children = []
        for child_index in self.children_indexes:
            children.append((self.population[child_index], self.active_paths[child_index]))

        return children

    def set_children(self, new_children):
        '''[summary]
        Sets the children of the population.
        ### Parameters
        1. new_children
            - new children genomes
        ### Returns
        None
        Raises
        ------
        ValueError
            - if the number of new_children is different than required (number of children in the population)
        '''
        if len(new_children) != len(self.children_indexes):
            raise ValueError(f"Number of new_children is different than required, number of new_children:{len(new_children)}, required: {len(self.children_indexes)}")

        for i in range(len(new_children)):
            child_index = self.children_indexes[i]
            self.population[child_index] = new_children[i]
            self.reset_active_path(child_index)
            self.calculate_fitness(child_index)
        
    def get_ninputs(self):
        '''[summary]
        Returns the number of inputs in the genome.
        ### Returns
        int
            - number of inputs
        '''
        return self.nrows
    
    def get_noutputs(self):
        '''[summary]
        Returns the number of outputs in the genome.
        ### Returns
        int
            - number of outputs
        '''
        return self.nrows
    
    def get_mutation_rate(self):
        '''[summary]
        Returns the mutation rate of the population.
        ### Returns
        float
            - mutation rate
        '''
        return self.mutation_rate
    
    def calculate_active_path(self, individual_index):
        '''[summary]
        Returns active paths if given individual indexes
        ### Parameters
        1. individual_index
            - index of individual to evaluate
        ### Returns
        List[int]
            - indexes of active genes
        '''
        individual = self.population[individual_index]
        output_gene_indexes = get_output_gene_indexes(individual)
        active_gene_indexes = get_active_gene_indexes(individual, output_gene_indexes)
        
        return active_gene_indexes
    
    def get_active_path(self, individual_index):
        '''[summary]
        Returns indexes of active genes int the given individual index
        ### Parameters
        1. individual_index
            - index of the individual
        ### Returns
        List[int]
            - indexes of active genes
        '''
        return self.active_paths[individual_index]
    
    def set_active_path(self, individual_index, active_path):
        '''[summary]
        Sets the active path of the individual.
        ### Parameters
        1. individual_index
            - index of the individual
        2. active_path
            - indexes of active genes
        ### Returns
        None
        '''
        self.active_paths[individual_index] = active_path

    def reset_active_path(self, individual_index):
        '''[summary]
        Resets the active path of the individual.
        ### Parameters
        1. individual_index
            - index of the individual
        ### Returns
        None
        '''
        self.set_active_path(individual_index, self.calculate_active_path(individual_index))

    def reset_all_active_paths(self):
        '''[summary]
        Resets all active paths in the population.
        ### Returns
        None
        '''
        for individual_index in range(len(self.population)):
            self.reset_active_path(individual_index)

    def get_individual_with_active_path(self, individual_index):
        '''[summary]
        Returns the individual and its active path.
        ### Parameters
        1. individual_index
            - index of the individual
        ### Returns
        1. List[List[int]]
            - individual
        2. List[int]
            - active path
        '''
        return (self.get_individual(individual_index), self.get_active_path(individual_index))
    
    def get_fitness(self, individual_index):
        '''[summary]
        Returns the fitness of the individual.
        ### Parameters
        1. individual_index
            - index of the individual
        ### Returns
        float
            - fitness of the individual
        '''
        return self.fitnesses[individual_index]
    
    def set_fitness(self, individual_index, fitness):
        '''[summary]
        Sets the fitness of the individual.
        ### Parameters
        1. individual_index
            - index of the individual
        2. fitness
            - fitness of the individual
        ### Returns
        None
        '''
        self.fitnesses[individual_index] = fitness

    def calculate_fitness(self, individual_index):
        '''[summary]
        Calculates the fitness of the individual.
        ### Parameters
        1. individual_index
            - index of the individual
        ### Returns
        None
        '''
        individual, active_path = self.get_individual_with_active_path(individual_index)
        fitness, is_acceptable = evaluate_fitness(individual, active_path, self.input_matrix, self.wanted_output, self.max_error)
        if is_acceptable:
            self.solution_index = individual_index
        self.set_fitness(individual_index, fitness)

    def calculate_fitness_all(self):
        '''[summary]
        Calculates the fitness of all individuals in the population.
        ### Parameters
        1. input_matrix
            - input_matrix data for the function
        2. wanted_output
            - expected output of the function
        ### Returns
        None
        '''
        for i in range(len(self.population)):
            self.calculate_fitness(i)

    def get_fittest_individual(self):
        '''[summary]
        Returns the fittest individual from the population.
        ### Returns
        1. List[List[int]]
            - fittest individual
        2. float
            - fitness of the fittest individual
        '''
        fittest_index = self.fitnesses.index(min(self.fitnesses))
        return (self.get_individual(fittest_index), self.get_fitness(fittest_index))

    def get_children_fitness_array(self):
        '''[summary]
        Returns the fitnesses of the children.
        ### Returns
        List[float]
            - fitnesses of the children
        '''
        children_fitnesses = []
        for child_index in self.children_indexes:
            children_fitnesses.append(self.get_fitness(child_index))
        return children_fitnesses

    def get_fittest_child(self):
        '''[summary]
        Returns the fittest child from the population.
        ### Returns
        1. List[List[int]]
            - fittest child
        2. float
            - fitness of the fittest child
        '''
        best_child_index = self.children_indexes[0]
        best_child_fitness = self.get_fitness(best_child_index)
        for child_index in self.children_indexes:
            if self.fitnesses[child_index] < best_child_fitness:
                best_child_index = child_index
                best_child_fitness = self.fitnesses[child_index]

        return (self.get_individual(best_child_index), best_child_fitness)
    
    def get_fittest_child_index(self):
        '''[summary]
        Returns the fittest child index from the population.
        ### Returns
        1. int
            - fittest child index
        2. float
            - fitness of the fittest child
        '''
        best_child_index = self.children_indexes[0]
        best_child_fitness = self.get_fitness(best_child_index)
        for child_index in self.children_indexes:
            if self.fitnesses[child_index] < best_child_fitness:
                best_child_index = child_index
                best_child_fitness = self.fitnesses[child_index]
        return best_child_index, best_child_fitness

    def get_parent_fitness(self, parent_index=0):
        '''[summary]
        Returns the fitness of the parent.
        ### Returns
        float
            - fitness of the parent
        '''
        return self.get_fitness(parent_index)
    
    def set_parent_by_index(self, new_parent_index, parent_index = 0):
        '''[summary]
        Sets the parent by index.
        ### Parameters
        1. parent_index
            - index of the parent
        ### Returns
        None
        '''
        if parent_index >= self.nparents:
            raise ValueError("Parent index out of range")
        
        if new_parent_index == parent_index:
            return
        else:
            self.move_individual(new_parent_index, parent_index)

    def set_parents_by_indexes(self, new_parent_1_index, new_parent_2_index):
        '''[summary]
        Sets the parents by indexes.
        ### Parameters
        1. new_parent_indexes
            - indexes of the new parents
        ### Returns
        None
        '''
        if self.is_parent(new_parent_1_index) and self.is_parent(new_parent_2_index):
            return
        elif self.is_parent(new_parent_1_index):
            if new_parent_1_index == 0:
                self.move_individual(new_parent_2_index, 1)
            elif new_parent_1_index == 1:
                self.move_individual(new_parent_2_index, 0)
            else:
                raise ValueError("Parent index out of range")
        elif self.is_parent(new_parent_2_index):
            if new_parent_2_index == 0:
                self.move_individual(new_parent_1_index, 1)
            elif new_parent_2_index == 1:
                self.move_individual(new_parent_1_index, 0)
            else:
                raise ValueError("Parent index out of range")
        else:
            self.move_individual(new_parent_1_index, 0)
            self.move_individual(new_parent_2_index, 1)

    def is_parent(self, index):
        '''[summary]
        Returns True if the given index is a parent, False otherwise.
        ### Parameters
        1. index
            - index to check
        ### Returns
        bool
            - True if the given index is a parent, False otherwise
        '''
        return index < self.nparents
    
    def move_individual(self, from_index, to_index):
        '''[summary]
        Moves an individual from one index to another.
        ### Parameters
        1. from_index
            - index to move from
        2. to_index
            - index to move to
        ### Returns
        None
        '''
        self.population[to_index] = self.population[from_index]
        self.active_paths[to_index] = self.active_paths[from_index]
        self.fitnesses[to_index] = self.fitnesses[from_index]