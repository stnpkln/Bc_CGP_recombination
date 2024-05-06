'''
File: utils.py
Purpose: Contains utility functions used in the CGP algorithm
Author: Petr Bromnik
'''

from constants.operations import operations, op_inputs

import random

def get_last_possible_input_index(ncolumns, nrows, gene_index):
    '''[summary]
    For the given gene index, returns the last index that can be used as its input
    ### Parameters
    1. ncolumns
        - number of columns in the matrix of genes
        - must be > 0
    2. nrows
        - number of rows in the matrix of genes
        - must be > 0
  3. gene_index
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
    1. nrows
        - number of rows in the matrix of genes
        - must be > 0
    2. index
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

def get_number_of_gene_inputs(gene):
    '''[summary]
    Returns the number of inputs for the given gene
    ### Parameters
    1. gene
        - gene to calculate number of inputs for
    ### Returns
    int
        - number of inputs for the given gene
    '''
    if len(gene) == 0:
        raise ValueError("gene must have at least one element")

    return op_inputs[operations[gene[0]]]

def get_output_gene_indexes(genome):
    '''[summary]
    Returns indexes of output genes in genome
    ### Parameters
    1. genome
        - genome to search output genes in
    ### Returns
    List[int]
        - list of indexes of output genes in genome
    '''
    return [i for i in range(len(genome)) if genome[i][0] == -2] # TODO may be optimized (last column of the genome matrix)


def get_active_gene_indexes(genome, output_gene_indexes):
    '''[summary]
    Returns indexes of active genes in genome
    ### Parameters
    1. genome
        - genome to search active genes in
    2. output_gene_indexes
        - list of indexes of output genes

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

def random_bool(chance):
    '''[summary]
    Returns True with the given chance
    ### Parameters
    1. chance: float
        - chance to return True
        - must be >= 0 and <= 1
    ### Returns
    bool
        - True with the given chance
    '''
    return random.uniform(0, 1) < chance

def get_number_of_gene_inputs(gene):
    '''[summary]
    Returns the number of inputs for the given gene
    ### Parameters
    1. gene: List[int]
        - gene to calculate number of inputs for
    ### Returns
    int
        - number of inputs for the given gene
    '''
    return get_number_of_op_inputs(gene[0])

def get_number_of_op_inputs(op):
    '''[summary]
    Returns the number of inputs for the given operation
    ### Parameters
    1. op: str
        - operation to calculate number of inputs for
        - must be in operations
    ### Returns
    int
        - number of inputs for the given operation
    '''
    return op_inputs[operations[op]]

def is_input_gene(gene):
    '''[summary]
    Returns True if the given gene is an input gene
    ### Parameters
    1. gene: List[int]
        - gene to check if it is an input gene
    ### Returns
    bool
        - True if the given gene is an input gene
    '''
    return gene[0] == -1

def is_output_gene(gene):
    '''[summary]
    Returns True if the given gene is an output gene
    ### Parameters
    1. gene: List[int]
        - gene to check if it is an output gene
    ### Returns
    bool
        - True if the given gene is an output gene
    '''
    return gene[0] == -2

