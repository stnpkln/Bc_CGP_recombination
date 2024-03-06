import numpy as np
from constants.operations import operations, op_inputs

class Population:
    def __init__(self, population_size, ncolumns, nrows):
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

        self.nrows = nrows
        self.ncolumns = ncolumns
        self.population = self.get_starting_popultation(population_size)
        self.parent_index = 0
        self.children_indexes = [i for i in range(1, population_size)]

    def get_starting_popultation(self, population_size):
        '''[summary]
        Returns a list of random genomes (population).
        ### Parameters
        1. population_size: int
            - number of individuals in the population
            - must be >= 1
        ### Returns
        List[List[int]]
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
        index = len(genome)
        last_possible_input = index - rowIndex
        for i in range(op_inputs[operations[operation]]):
            input = np.random.randint(0, last_possible_input)
            gene[i + 1] = input
        
        return gene

    def get_population(self):
        '''[summary]
        ### Returns
        List[List[int]]
            - population
        '''
        return self.population

    def get_individual(self, index):
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
    
    def set_individual(self, index, individual):
        '''[summary]
        Sets an individual in the population.
        ### Parameters
        1. index: int
            - index of the individual
            - must be >= 0
        2. individual: List[int]
            - individual to set
        ### Returns
        None
        '''
        if index < 0:
            raise ValueError("index must be >= 0")

        self.population[index] = individual

    def get_parent(self):
        '''[summary]
        Returns the parent of the population.
        ### Returns
        List[List[int]]
            - parent genome
        '''
        return self.population[self.parent_index]
    
    def set_parent(self, new_parent):
        '''[summary]
        Sets the parent of the population.
        ### Parameters
        1. new_parent: List[List[int]]
            - new parent genome
        ### Returns
        None
        '''
        self.population[self.parent_index] = new_parent
    
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

    def set_children(self, new_children):
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
            self.population[self.children_indexes[i]] = new_children[i]
        
