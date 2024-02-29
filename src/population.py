import numpy as np
from constants.operations import operations, op_inputs

class Population:
    def __init__(self, population_size, ncolumns, nrows):
        self.nrows = nrows
        self.ncolumns = ncolumns
        self.population = self.get_starting_popultation(population_size)

    def get_starting_popultation(self, population_size):
        population = []
        for i in range(population_size):
            population.append(self.get_random_genome())
        return population

    def get_random_genome(self):
        genome = []
        for column in range(self.ncolumns):
            for row in range(self.nrows):
                genome.append(self.get_random_gene(row, column, genome))

        return genome


    def get_random_gene(self, rowIndex, columnIndex, genome):
        gene = [-1, -1, -1] # aby slo poznat kolik má gen vstupů
        if (columnIndex == 0):
            # vstupy do genomu
            return gene
        
        if ((columnIndex == self.ncolumns - 1) and (rowIndex == self.nrows - 1)):
            # vystup z genomu
            return [-2, np.random.randint(0, len(genome) - rowIndex), -2]

        # pridani operace
        operation = np.random.randint(0, len(operations))
        gene[0] = operation

        # generovani vstupu do genu (zatim bez levels back)
        index = len(genome)
        last_possible_input = index - rowIndex
        for i in range(op_inputs[operations[operation]]):
            input = np.random.randint(0, last_possible_input)
            gene[i + 1] = input
        
        return gene

    def get_population(self):
        return self.population

    def get_genome(self, index):
        return self.population[index]
    
    def get_first_function_node_index(self):
        return self.nrows
    
    def get_last_function_node_index(self):
        return self.ncolumns * self.nrows - 1