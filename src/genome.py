from population import Population
from constants.operations import operations, op_inputs, op_functions
from typing import List
import numpy as np
from sklearn.metrics import mean_squared_error
from copy import deepcopy
from math import floor

mutation_rate = 0.1

def get_active_gene_indexes(output_gene_indexes: List[int], genome: List[List[int]]):
    '''[summary]
    Returns indexes of active genes in genome
    ### Parameters
    1. output_gene_indexes: List[int]
        - list of indexes of output genes
    2. genome: List[List[int]]
        - genome to search active genes in
    
    ### Returns
    List[int]
        - list of indexes of active genes in genome
    '''
    active_genes_indexes = []
    added_to_active_flag = [False] * len(genome) # flag for each gene if it was added to active genes

    found_new_gene = True
    gene_indexes_to_search = output_gene_indexes.copy()
    while (found_new_gene):
        new_indexes_to_search = []
        for gene_index_to_search in gene_indexes_to_search:
            gene = genome[gene_index_to_search]
            gene_operation = gene[0]

            # in case of input gene, skip it
            if (gene_operation == -1):
                continue

            # add the gene we are working with to active genes
            active_genes_indexes.append(gene_index_to_search)

            # in case of output gene, save it to active genes, and continue
            if (gene_operation == -2):
                input_gene_index = gene[1]
                if (not added_to_active_flag[input_gene_index]):
                    # mark the input of this gene as active, and add it to active genes
                    added_to_active_flag[input_gene_index] = True
                    new_indexes_to_search.append(input_gene_index)
                continue

            # function genes
            for i in range(1, 1 + op_inputs[operations[gene_operation]]): # for each input that the operation of this gene has
                input_gene_index = gene[i] # in case of output gene, use only the first input
                if (not added_to_active_flag[input_gene_index]):
                    # mark the input of this gene as active, and add it to genes to search next
                    added_to_active_flag[input_gene_index] = True
                    new_indexes_to_search.append(input_gene_index)

        found_new_gene = len(new_indexes_to_search) != 0 # if there are no new genes to search, stop the loop
        gene_indexes_to_search = new_indexes_to_search # reassign the genes to search

    return active_genes_indexes

def genome_output(genome: List[List[int]], input_values: List[List[int]]):
    '''[summary]
    ### Parameters
    1. genome: List[List[int]]
        - genome to calculate output for
    2. input_values: List[List[int]]
        - list of input values to calculate output for
        - each list of input values is one input

    ### Returns
    np.ndarray
        - output of genome for given input values
        - works with only one output gene (TODO if necessary)
    '''
    output_gene_indexes = [i for i in range(len(genome)) if genome[i][0] == -2]
    active_gene_indexes = get_active_gene_indexes(output_gene_indexes, genome)
    n_input_nodes = len(input_values) # gen number of input nodes, base on parameter input_values
    nrows = len(active_gene_indexes) + n_input_nodes # number of rows in matrix
    ncols = len(input_values[0]) # number of columns in matrix

    # mapping from gene index to matrix index, so we can use gene indexes to access the matrix, and the matrix can be only as big as the number of active nodes
    gene_to_matrix_mapping = {key: value for key, value in zip(active_gene_indexes[::-1], range(n_input_nodes, nrows))}

    matrix = np.full((nrows, ncols), 0)

    # fill the matrix with input values
    for i in range(n_input_nodes):
        matrix[i] = input_values[i]
        gene_to_matrix_mapping[i] = i

    # fill the matrix with output of genes
    for i in range(len(active_gene_indexes)):
        for gene_index in active_gene_indexes:
            gene = genome[gene_index]
            gene_operation = gene[0]

            # in case of input gene, skip it
            if (gene_operation == -1):
                continue

            # in case of output gene, copy the input gene output
            if (gene_operation == -2):
                last_function_gene_index = gene[1]
                matrix[gene_to_matrix_mapping[gene_index]] = matrix[gene_to_matrix_mapping[last_function_gene_index]]
                continue

            # function genes
            # TODO, so far works only with operations that have two inputs
            first_input = matrix[gene_to_matrix_mapping[gene[1]]]
            second_input = matrix[gene_to_matrix_mapping[gene[2]]]
            matrix[gene_to_matrix_mapping[gene_index]] = op_functions[operations[gene_operation]](first_input, second_input) # calculate the output of the gene

    # return the last column (output column) of the matrix
    return matrix[-1]

def evaluate_fitness(genome: List[List[int]], input: List[List[int]], wanted_output: List[int]):
    '''[summary]
    Returns fitness of genome for given input values and wanted output.
    Fitness is value is calculated as mean squared error between wanted output and output of genome for given input values.
    ### Parameters
    1. genome: List[List[int]]
        - genome to calculate fitness for
    2. input: List[List[int]]
        - list of input values to calculate output for
        - each list of input values is one input
    3. wanted_output: List[int]
        - list of wanted output values
    ### Returns
    float
        - fitness of genome for given input values and wanted output
        - value >= 0.0
    ### TODO
    - make inputs and wanted_output ndArrays
    '''
    output = genome_output(genome, input)
    return mean_squared_error(wanted_output, output)

def mutate_individual(target: List[List[int]], ncolumns, nrows):
    '''[summary]
    Returns mutated individual, without changing the original
    ### Parameters
    1. target: List[List[int]]
        - individual to mutate
    2. ncolumns: int
        - number of columns in the matrix of genes
    3. nrows: int
        - number of rows in the matrix of genes
    ### Returns
    List[List[int]]
        - mutated individual
    '''
    # deep copy the target, so we don't change the original
    individual = deepcopy(target)
    genome_length = len(individual)
    n_of_genes_to_mutate = floor(genome_length * mutation_rate + 1)

    for i in range(n_of_genes_to_mutate):
        success = False
        mutated_gene = []

        # find a gene that can be mutated
        while(not success):
            gene_index_to_mutate = np.random.randint(genome_length)
            gene = individual[gene_index_to_mutate]
            mutated_gene, success = mutate_gene(gene, gene_index_to_mutate, ncolumns, nrows)

        individual[gene_index_to_mutate] = mutated_gene

    return individual

def mutate_gene(gene: List[int], gene_index, ncolumns, nrows):
    '''[summary]
    Returns mutated gene (may mutate the original)
    ### Parameters
    1. gene: List[int]
        - gene to mutate
    2. gene_index: int
        - index of the gene in the genome
    3. ncolumns: int
        - number of columns in the matrix of genes
    4. nrows: int
        - number of rows in the matrix of genes
    ### Returns
    List[int]
        - mutated gene
    bool
        - True if gene was successfully mutated, False otherwise
    Raises
    ------
    - Exception
        - if last_possible_input_index is 0, meaning that an internal error occured
    ### 
    '''
    allele_to_mutate = np.random.randint(0, len(gene))

    if gene[allele_to_mutate] == -1 or gene[allele_to_mutate] == -2:
        return gene, False

    mutation_to_be_done = True
    while(mutation_to_be_done):
        original = gene[allele_to_mutate]

        # if the gene is an operation, mutate it to another operation
        if allele_to_mutate == 0:
            mutated = np.random.randint(0, len(operations))
        # if the gene is an input, mutate it to another (correct) input
        else:
            last_possible_input_index = get_last_possible_input_index(ncolumns, nrows, gene_index)
            if (last_possible_input_index <= 0):
                raise Exception(f"last_possible_input_index is: {last_possible_input_index}, gene_index is: {gene_index}, ncolumns is: {ncolumns}, nrows is: {nrows}")
            elif (last_possible_input_index == 1):
                return gene, False # impossible to mutate input, if there is only one option available

            mutated = np.random.randint(0, last_possible_input_index)
        
        # if the gene was successfully mutated, stop the loop
        if original != mutated:
            gene[allele_to_mutate] = mutated
            mutation_to_be_done = False

    return gene, True

def get_last_possible_input_index(ncolumns: int, nrows: int, gene_index: int):
    '''[summary]
    For the given gene index, returns the last index that can be used as its input
    ### Parameters
    1. ncolumns: int
        - number of columns in the matrix of genes
        - must be > 0
    2. nrows: int
        - number of rows in the matrix of genes
        - must be > 0
  3. gene_index: int
        - index of the gene in the genome
        - must be >= 0
    ### Returns
    int
        - last possible input index
    Raises
    ------
    ValueError
        - if gene_index < 0 or ncolumns < 1 or nrows < 1
    '''
    if (gene_index < 0 or ncolumns < 1 or nrows < 1):
        raise ValueError("gene_index must be > 0, ncolumns must be > 0, nrows must be > 0")

    column_index = get_genome_column(nrows, gene_index)
    columns_before = column_index
    return columns_before * nrows

def get_genome_column(nrows, index):
    '''[summary]
    Returns the column of the genome for the given index
    ### Parameters
    1. nrows: int
        - number of rows in the matrix of genes
        - must be > 0
    2. index: int
        - index of the gene in the genome
        - must be >= 0
    ### Returns
    int
        - column of the genome for the given index
    Raises
    ------
    ValueError
        - if index < 0 or nrows < 1
    '''
    if (index < 0 or nrows < 1):
        raise ValueError("index and nrows must be positive integers")

    return index // nrows

def get_number_of_gene_inputs(gene: List[int]):
    '''[summary]
    Returns the number of inputs for the given gene
    ### Parameters
    1. gene: List[int]
        - gene to calculate number of inputs for
    ### Returns
    int
        - number of inputs for the given gene
    '''
    if len(gene) == 0:
        raise ValueError("gene must have at least one element")

    return op_inputs[operations[gene[0]]]

