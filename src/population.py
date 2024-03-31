from constants.operations import operations, op_inputs
from utils import get_active_gene_indexes, get_last_possible_input_index, get_number_of_gene_inputs, get_output_gene_indexes
from typing import List
import numpy as np

class Population:
    def __init__(self, population_size: int, ncolumns: int, nrows: int, mutation_rate: float, nparents: int = 1) -> None:
        '''[summary]
        Initializes the population with random genomes.
        ### Parameters
        1. population_size: int
            - number of individuals in the population
            - must be >= 1
        2. ncolumns: int
            - number of columns in the genome
            - must be >= 3
        3. nrows: int
            - number of rows in the genome
            - must be >= 1
        4. mutation_rate: int
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
        self.reset_all_active_paths()

    def get_starting_popultation(self, population_size: int) -> List[List[List[int]]]:
        '''[summary]
        Returns a list of random genomes (population).
        ### Parameters
        1. population_size: int
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

    def get_random_genome(self) -> List[List[int]]:
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


    def get_random_gene(self, rowIndex: int, columnIndex: int, genome: List[List[int]]) -> List[int]:
        '''[summary]
        Returns a random gene.
        ### Parameters
        1. rowIndex: int
            - index of the row in the genome
            - must be >= 0
        2. columnIndex: int
            - index of the column in the genome
            - must be >= 0
        3. genome: List[List[int]]
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

    def get_population(self) -> List[List[List[int]]]:
        '''[summary]
        ### Returns
        List[List[List[int]]]
            - population
        '''
        return self.population

    def get_individual(self, index: int) -> List[int]:
        '''[summary]
        Returns an individual from the population.
        ### Parameters
        1. index: int
            - index of the individual
            - must be >= 0
        ### Returns
        List[int]
            - individual
        '''
        if index < 0:
            raise ValueError("index must be >= 0")

        return self.population[index]
    
    def set_individual(self, index: int, individual: List[List[int]]) -> None:
        '''[summary]
        Sets an individual in the population.
        ### Parameters
        1. index: int
            - index of the individual
            - must be >= 0
        2. individual: List[List[int]]
            - individual to set
        ### Returns
        None
        '''
        if index < 0:
            raise ValueError("index must be >= 0")

        self.population[index] = individual
        self.reset_active_path(index)

    def get_parent(self, parent_index = 0) -> List[List[int]]:
        '''[summary]
        Returns the parent of the population.
        ### Returns
        List[List[int]]
            - parent genome
        '''
        if parent_index >= self.nparents:
            raise ValueError("Parent index out of range")

        return self.population[parent_index]
    
    def get_parent_with_active_path(self, parent_index = 0) -> tuple[List[List[int]], List[int]]:
        return (self.get_parent(), self.get_active_path(parent_index))
    
    def set_parent(self, new_parent: List[List[int]], parent_index = 0) -> None:
        '''[summary]
        Sets the parent of the population.
        ### Parameters
        1. new_parent: List[List[int]]
            - new parent genome
        ### Returns
        None
        '''
        if parent_index >= self.nparents:
            raise ValueError("Parent index out of range")
    
        self.population[parent_index] = new_parent
        self.reset_active_path(parent_index)
    
    def get_children(self) -> List[List[List[int]]]:
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
    
    def get_children_with_active_paths(self) -> List[tuple[List[List[int]], List[int]]]:
        children = []
        for child_index in self.children_indexes:
            children.append((self.population[child_index], self.active_paths[child_index]))

        return children

    def set_children(self, new_children: List[List[List[int]]]) -> None:
        '''[summary]
        Sets the children of the population.
        ### Parameters
        1. new_children: List[List[List[int]]]
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
        
    def get_ninputs(self) -> int:
        '''[summary]
        Returns the number of inputs in the genome.
        ### Returns
        int
            - number of inputs
        '''
        return self.nrows
    
    def get_noutputs(self) -> int:
        '''[summary]
        Returns the number of outputs in the genome.
        ### Returns
        int
            - number of outputs
        '''
        return self.nrows
    
    def get_mutation_rate(self) -> float:
        '''[summary]
        Returns the mutation rate of the population.
        ### Returns
        float
            - mutation rate
        '''
        return self.mutation_rate
    
    def calculate_active_path(self, individual_index: int):
        '''[summary]
        Returns active paths if given individual indexes
        ### Parameters
        1. individual_index: int
            - index of individual to evaluate
        ### Returns
        List[int]
            - indexes of active genes
        '''
        individual = self.population[individual_index]
        output_gene_indexes = get_output_gene_indexes(individual)
        active_gene_indexes = get_active_gene_indexes(individual, output_gene_indexes)
        
        return active_gene_indexes
    
    def get_active_path(self, individual_index: List) -> List[int]:
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
    
    def set_active_path(self, individual_index: int, active_path: List[int]) -> None:
        self.active_paths[individual_index] = active_path

    def reset_active_path(self, individual_index: int) -> None:
        self.set_active_path(individual_index, self.calculate_active_path(individual_index))

    def reset_all_active_paths(self) -> None:
        for individual_index in range(len(self.population)):
            self.reset_active_path(individual_index)

    def get_individual_with_active_path(self, individual_index) -> tuple[List[List[int]], List[int]]:
        return (self.get_individual(individual_index), self.get_active_path(individual_index))