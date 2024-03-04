from population import Population
from constants.operations import operations, op_inputs, op_functions
from typing import List
import numpy as np
import timeit


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
    Returns output of genome for given input values
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
    output_gene_indexes = [i for i in range(len(genome)) if genome[i][0] == -2] # get indexes of output genes, may need to be changed, TODO
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

