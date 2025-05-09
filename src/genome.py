'''
File: genome.py
Purpose: Contains the genome operations used in the CGP algorithm
Author: Petr Bromnik
'''

from constants.operations import operations, op_inputs, op_functions
from utils import get_last_possible_input_index, get_number_of_op_inputs, is_input_gene, is_output_gene, random_bool
import numpy as np
from copy import deepcopy
from math import floor

def genome_output(genome, active_gene_indexes, input_matrix):
    '''[summary]
    ### Parameters
    1. genome
        - genome to calculate output for
    2. input_matrix
        - list of input values to calculate output for
        - each list of input values is one input

    ### Returns
    np.ndarray
        - output of genome for given input values
        - works with only one output gene (TODO if necessary)
    '''
    n_input_nodes = len(input_matrix) # gen number of input nodes, base on parameter input_matrix
    nrows = len(active_gene_indexes) + n_input_nodes # number of rows in matrix
    ncols = len(input_matrix[0]) # number of columns in matrix

    # mapping from gene index to matrix index, so we can use gene indexes to access the matrix, and the matrix can be only as big as the number of active nodes
    gene_to_matrix_mapping = {key: value for key, value in zip(active_gene_indexes[::-1], range(n_input_nodes, nrows))}

    matrix = np.full((nrows, ncols), 0.0)

    # fill the matrix with input values
    for i in range(n_input_nodes):
        matrix[i] = input_matrix[i]
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
            n_of_op_inputs = op_inputs[operations[gene_operation]]
            op_function = op_functions[operations[gene_operation]]

            if n_of_op_inputs == 1:
                first_input = matrix[gene_to_matrix_mapping[gene[1]]]
                matrix[gene_to_matrix_mapping[gene_index]] = op_function(first_input)
            elif n_of_op_inputs == 2:
                first_input = matrix[gene_to_matrix_mapping[gene[1]]]
                second_input = matrix[gene_to_matrix_mapping[gene[2]]]
                matrix[gene_to_matrix_mapping[gene_index]] = op_function(first_input, second_input) # calculate the output of the gene

    # return the last column (output column) of the matrix
    return matrix[-1]

def evaluate_fitness(genome, genome_active_path_indexes, input_matrix, wanted_output, max_difference=0.01):
    '''[summary]
    Returns fitness of genome for given input values and wanted output.
    Fitness value is calculated as mean absolute error between wanted output and output of genome for given input values.
    ### Parameters
    1. genome
        - genome to calculate fitness for
    2. input_matrix
        - list of input values to calculate output for
        - each list of input values is one input
    3. wanted_output
        - list of wanted output values
    ### Returns
    float
        - fitness of genome for given input values and wanted output
        - value >= 0.0
    '''
    output = genome_output(genome, genome_active_path_indexes, input_matrix)
    mae = np.absolute(np.subtract(wanted_output, output)).sum()
    if (mae < 0):
        raise ValueError("overflow, mean squared error is negative, something went wrong with the fitness calculation")
    is_acceptable = is_acceptable_solution(output, wanted_output, max_difference)
    return mae, is_acceptable

def mutate_individual(target, ncolumns, nrows, mutation_rate):
    '''[summary]
    Returns mutated individual, without changing the original
    ### Parameters
    1. target
        - individual to mutate
    2. ncolumns
        - number of columns in the matrix of genes
    3. nrows
        - number of rows in the matrix of genes
    4. mutation_rate
        - mutation rate of the algorithm
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

def mutate_gene(gene, gene_index, ncolumns, nrows):
    '''[summary]
    Returns mutated gene (may mutate the original)
    ### Parameters
    1. gene
        - gene to mutate
    2. gene_index
        - index of the gene in the genome
    3. ncolumns
        - number of columns in the matrix of genes
    4. nrows
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
            # in case the mutation is changing the operation, prepare the inputs for the new operation
            if allele_to_mutate == 0:
                format_inputs_for_new_operation(gene, gene_index, mutated, nrows)
            gene[allele_to_mutate] = mutated
            mutation_to_be_done = False

    return gene, True

def active_gene_transplant(receiver, receiver_active_path, donor, donor_active_path, exchange_rate, nrows = 1):
    '''[summary]
    Returns child genome from two parent genomes using recombination 1
    ### Parameters
    1. donor
        - first parent genome
    2. receiver
        - second parent genome
    ### Returns
    List[List[int]]
        - child genome
    '''
    # deep copy the parents, so we don't change the original
    child = deepcopy(receiver)

    exchange_indexes = [gene for gene in donor_active_path if gene not in receiver_active_path and random_bool(exchange_rate)]
    for exchange_index in exchange_indexes:
        donor_gene = donor[exchange_index].copy()
        child[exchange_index] = donor_gene

    return child

def subgraph_exchange(receiver, receiver_active_path, donor, donor_active_path, exchange_rate, nrows):
    '''[summary]
    Returns child genome from two parent genomes using recombination 2
    ### Parameters
    1. parent1
        - first parent genome
    2. parent2
        - second parent genome
    ### Returns
    List[List[int]]
        - child genome
    '''

    # deep copy the parents, so we don't change the original
    child = deepcopy(receiver)

    possible_exchange_indexes = [gene for gene in receiver_active_path if gene in donor_active_path]
    exchange_index = np.random.choice(possible_exchange_indexes)

    receiver_flags = [False for _ in range(len(receiver))]
    exchange(receiver=child, receiver_flags=receiver_flags, receiver_index=exchange_index, donor=donor, donor_index=exchange_index, exchange_rate=exchange_rate, nrows=nrows)
    return child


def exchange(receiver, receiver_flags, receiver_index, donor, donor_index, exchange_rate, nrows):
    '''[summary]
    Recursively exchanges the genes between the receiver and the donor
    ### Parameters
    1. receiver
        - genome of the receiver
    2. receiver_flags
        - flags for each gene in receiver, if it was already exchanged
    3. receiver_index
        - index of the gene in the receiver
    4. donor
        - genome of the donor
    5. donor_index
        - index of the gene in the donor
    6. exchange_rate
        - exchange rate of the algorithm
    7. nrows
        - number of rows in the matrix of genes
    ### Returns
    None
    '''
    if receiver_flags[receiver_index]:
        return
    
    receiver_gene = receiver[receiver_index]
    donor_gene = donor[donor_index]
    if is_input_gene(receiver_gene) or is_input_gene(donor_gene):
        return
    
    if is_output_gene(receiver_gene):
        if is_output_gene(donor_gene):
            exchange(receiver=receiver,
                        receiver_flags=receiver_flags,
                        receiver_index=receiver_gene[1],
                        donor=donor,
                        donor_index=donor_gene[1],
                        exchange_rate=exchange_rate,
                        nrows=nrows)
            return
        else:
            raise Exception("output gene mismatch in subgraph exchange")
        
    next_receiver_genes = []
    next_donor_genes = []
    for i in range(1, len(receiver_gene)):
        if receiver_gene[i] != -1 and donor_gene[i] != -1 and random_bool(exchange_rate):
            next_receiver_genes.append(receiver_gene[i])
            next_donor_genes.append(donor_gene[i])
    
    format_inputs_for_new_operation(receiver[receiver_index], receiver_index, donor_gene[0], nrows)
    receiver_gene[0] = donor_gene[0]
    receiver_flags[receiver_index] = True

    for i in range(len(next_receiver_genes)):
        exchange(receiver=receiver,
                    receiver_flags=receiver_flags,
                    receiver_index=next_receiver_genes[i],
                    donor=donor,
                    donor_index=next_donor_genes[i],
                    exchange_rate=exchange_rate,
                    nrows=nrows)

def format_inputs_for_new_operation(gene, gene_index, new_operation, nrows):
    '''[summary]
    Prepares the given gene for a change of operation allele, by changing the inputs to match the new operation.
    Shortened inputs are set to -1, if a new input is needed, it is set to a random (in bounds) value.
    ### Parameters
    1. gene
        - gene to prepare inputs for
    2. gene_index
        - index of the gene to prepare in given genome
    3. operation
        - new operation to be inside gene
    4. nrows
        - number of rows in the matrix of genes
    '''
    ncolumns = len(gene) / nrows
    operation_inputs = get_number_of_op_inputs(new_operation)
    for input_number in range(1, len(gene)):
        if input_number <= operation_inputs and gene[input_number] == -1:
            gene[input_number] = np.random.randint(get_last_possible_input_index(ncolumns, nrows, gene_index))
        elif input_number > operation_inputs and gene[input_number] != -1:
            gene[input_number] = -1

def is_acceptable_solution(output, wanted_output, max_difference):
    '''[summary]
    Returns True if the difference between output and wanted_output is less than max_difference, False otherwise
    ### Parameters
    1. output
        - output to compare
    2. wanted_output
        - wanted output to compare
    3. max_difference
        - maximum difference between output and wanted_output
    ### Returns
    bool
        - True if the difference between output and wanted_output is less than max_difference, False otherwise
    '''
    return np.absolute(np.subtract(wanted_output, output)).max() <= max_difference
