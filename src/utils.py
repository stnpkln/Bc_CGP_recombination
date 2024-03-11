
from constants.operations import operations, op_inputs

from typing import List


def get_last_possible_input_index(ncolumns: int, nrows: int, gene_index: int) -> int:
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

def get_genome_column(nrows: int, index: int) -> int:
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

def get_number_of_gene_inputs(gene: List[int]) -> int:
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

def get_output_gene_indexes(genome: List[List[int]]) -> List[int]:
    '''[summary]
    Returns indexes of output genes in genome
    ### Parameters
    1. genome: List[List[int]]
        - genome to search output genes in
    ### Returns
    List[int]
        - list of indexes of output genes in genome
    '''
    return [i for i in range(len(genome)) if genome[i][0] == -2] # TODO may be optimized (last column of the genome matrix)