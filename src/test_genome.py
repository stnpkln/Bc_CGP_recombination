from __future__ import annotations
from copy import deepcopy
from genome import evaluate_fitness, format_inputs_for_new_operation, genome_output, mutate_gene, mutate_individual, active_gene_transplant, subgraph_exchange
from utils import get_active_gene_indexes, get_output_gene_indexes
from constants.operations import operations, op_inputs

import unittest
import numpy as np

test_genome_small = [
    [-1, -1, -1],   # 0
    [0, 0, 0],      # 1
    [2, 0, 1],      # 2
    [-2, 2, -2]     # 3
]                   # (x + x) * x

test_genome = [
            [-1, -1, -1],   # 0   | x
            [0, 0, 0],      # 1   | 2x
            [2, 0, 1],      # 2   | 2x * x
            [2, 1, 1],      # 3   | 
            [1, 2, 1],      # 4   |
            [0, 1, 2],      # 5   | (2x * x) + 2x
            [2, 2, 5],      # 6   | (2x * x) * ((2x * x) + 2x)
            [0, 4, 5],      # 7
            [2, 6, 6],      # 8   | ((2x * x) * ((2x * x) + 2x)) ^ 2
            [-2, 8, -2]     # 9
        ]                   # ((2x * x) * ((2x * x) + 2x)) ^ 2

test_parent1 = [
            [-1, -1, -1],   # 0 A  | x
            [0, 0, 0],      # 1 A  | 2x
            [2, 0, 1],      # 2 A  | 2x * x
            [2, 1, 1],      # 3   | 
            [1, 2, 1],      # 4   |
            [0, 1, 2],      # 5 A  | (2x * x) + 2x
            [2, 2, 5],      # 6 A  | (2x * x) * ((2x * x) + 2x)
            [0, 4, 5],      # 7
            [2, 6, 6],      # 8 A  | ((2x * x) * ((2x * x) + 2x)) ^ 2
            [-2, 8, -2]     # 9 A
        ]                   # ((2x * x) * ((2x * x) + 2x)) ^ 2

test_parent2 = [
            [-1, -1, -1],   # 0 A  | x
            [1, 0, 0],      # 1 A  | 2x
            [0, 0, 1],      # 2 A  | 2x * x
            [3, 1, 1],      # 3   | 
            [2, 1, 0],      # 4 A  |
            [2, 1, 2],      # 5 A  | (2x * x) + 2x
            [2, 2, 5],      # 6   | (2x * x) * ((2x * x) + 2x)
            [1, 4, 5],      # 7 A
            [1, 6, 6],      # 8   | ((2x * x) * ((2x * x) + 2x)) ^ 2
            [-2, 7, -2]     # 9 A
        ]                   # ((2x * x) * ((2x * x) + 2x)) ^ 2

test_genome_small_multiple_inputs = [
    [-1, -1, -1],   # 0   | x
    [-1, -1, -1],   # 1   | y
    [0, 0, 1],      # 2   | x + y
    [2, 2, 1],      # 3   | (x + y) * y
    [-2, 3, -1]     # 4   | (x + y) * y
]                   # (x + y) * y

test_wanted_function = lambda x: (2 * x * x + 2 * x) ** 2

class TestGenome(unittest.TestCase):

    def test_genome_output(self):
        output = genome_output(test_genome, get_active_gene_indexes(test_genome, get_output_gene_indexes(test_genome)), np.array([np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])]))
        self.assertListEqual(output.tolist(), [64] * 10, "incorrect genome output")

        output = genome_output(test_genome, get_active_gene_indexes(test_genome, get_output_gene_indexes(test_genome)), np.array([np.array([0, 1, 2, 3, 4, 4, 3, 2, 1, 0])]))
        self.assertListEqual(output.tolist(), [0, 64, 9216, 186624, 1638400, 1638400, 186624, 9216, 64, 0], "incorrect genome output with different input values")
        
        output = genome_output(test_genome_small, get_active_gene_indexes(test_genome_small, get_output_gene_indexes(test_genome_small)), np.array([np.array([1, 1, 1])]))
        self.assertListEqual(output.tolist(), [2, 2, 2], "incorrect genome output with small genome")

        output = genome_output(test_genome_small_multiple_inputs, get_active_gene_indexes(test_genome_small_multiple_inputs, get_output_gene_indexes(test_genome_small_multiple_inputs)), np.array([np.array([1, 1, 1]), np.array([2, 2, 2])]))
        self.assertListEqual(output.tolist(), [6, 6, 6], "incorrect genome output in genome with more inputs")

        # floats
        output = genome_output(test_genome_small, get_active_gene_indexes(test_genome_small, get_output_gene_indexes(test_genome_small)), np.array([np.array([0.5, 0.5, 0.5])]))
        self.assertListEqual(output.tolist(), [0.5, 0.5, 0.5], "incorrect genome output with small genome and floats")
    
    def test_evaluate_fitness(self):
        genome_input = np.array([np.array([0, 1, 2, 3, 4, 4, 3, 2, 1, 0])])
        wanted_output = np.array([0, 64, 9216, 186624, 1638400, 1638400, 186624, 9216, 64, 0])

        self.assertEqual(evaluate_fitness(test_genome, get_active_gene_indexes(test_genome, get_output_gene_indexes(test_genome)), genome_input, wanted_output), 0)

        self.assertTrue(evaluate_fitness(test_genome_small, get_active_gene_indexes(test_genome_small, get_output_gene_indexes(test_genome_small)), genome_input, wanted_output) > 0)

    def test_mutate_gene(self):
        gene, success = mutate_gene([-1, -1, -1], 0, 3, 3)
        self.assertListEqual(gene, [-1, -1, -1], "incorrect mutated gene")
        for i in range(1000):
            gene, success = mutate_gene([0, 0, 0], 5, 3, 3)
            self.assertNotEqual(set(gene), set([0, 0, 0]), "incorrect mutated gene")
            self.assertLess(gene[0], len(operations), "operation out of range after gene mutation")
            self.assertLess(gene[1], 3, "input out of range after gene mutation")
            self.assertLess(gene[2], 3, "input out of range after gene mutation")

        target_checked = False
        while not target_checked:
            gene, success = mutate_gene([5, 0, -1], 5, 10, 1)
            if (op_inputs[operations[gene[0]]] == 2):
                self.assertNotEqual(gene[2], -1, "input out of range after gene mutation")
                target_checked = True

        target_checked = False
        while not target_checked:
            gene, success = mutate_gene([1, 0, 0], 5, 10, 1)
            if (op_inputs[operations[gene[0]]] == 1):
                self.assertEqual(gene[2], -1, "input out of range after gene mutation")
                target_checked = True



    def test_mutate_individual(self):
        gene0 = [-1, -1, -1]
        gene1 = [0, 0, 0]
        gene2 = [2, 0, 1]
        gene3 = [-2, 2, -2]
        test_genome = [gene0, gene1, gene2, gene3]
        mutate_individual(test_genome, 4, 1, 0.1)

        # checking if the mutation doesnt change the original genome
        self.assertListEqual(test_genome[0], gene0, "mutated genome should not change the original")
        self.assertListEqual(test_genome[1], gene1, "mutated genome should not change the original")
        self.assertListEqual(test_genome[2], gene2, "mutated genome should not change the original")
        self.assertListEqual(test_genome[3], gene3, "mutated genome should not change the original")

        # checking if there is no mutation out of bounds
        for i in range(100):
            mutated_genome = mutate_individual(test_genome, 4, 1, 0.1)
            for i in range(len(mutated_genome)):
                self.assertLess(mutated_genome[i][0], len(operations), "operation out of range after genome mutation")
                self.assertLess(mutated_genome[i][1], i, "input out of range after genome mutation")
                self.assertLess(mutated_genome[i][2], i, "input out of range after genome mutation")

        # checking if the mutation actually happened
        for i in range(100):
            mutated_genome = mutate_individual(test_genome, 4, 1, 0.1)
            is_mutated = set(mutated_genome[0]) != set(gene0) or set(mutated_genome[1]) != set(gene1) or set(mutated_genome[2]) != set(gene2) or set(mutated_genome[3]) != set(gene3)
            self.assertTrue(is_mutated, f"mutated genome {mutated_genome} should not be the same as the original {test_genome}")

    def test_active_gene_transplant(self):
        child = active_gene_transplant(test_parent1,
                               get_active_gene_indexes(test_parent1, get_output_gene_indexes(test_parent1)),
                               test_parent2,
                               get_active_gene_indexes(test_parent2, get_output_gene_indexes(test_parent2)),
                               1)
        
        # print(child)

    def test_subgraph_exchange(self):
        # should exchange only the first function gene
        parent1 = [[-1, -1, -1], [0, 0, 0], [-2, 1, -2]]
        parent2 = [[-1, -1, -1], [1, 0, 0], [-2, 1, -2]]
        child = subgraph_exchange(receiver=parent1,
                               receiver_active_path=get_active_gene_indexes(parent1, get_output_gene_indexes(parent1)),
                               donor=parent2,
                               donor_active_path=get_active_gene_indexes(parent2, get_output_gene_indexes(parent2)),
                               exchange_rate=1,
                               nrows=1)
        self.assertListEqual(child, [[-1, -1, -1], [1, 0, 0], [-2, 1, -2]], "should exchange only first function gene")

        # should exchange and format inputs
        parent1 = [[-1, -1, -1], [0, 0, 0], [-2, 1, -2]]
        parent2 = [[-1, -1, -1], [5, 0, -1], [-2, 1, -2]]
        child = subgraph_exchange(receiver=parent1,
                                 receiver_active_path=get_active_gene_indexes(parent1, get_output_gene_indexes(parent1)),
                                 donor=parent2,
                                 donor_active_path=get_active_gene_indexes(parent2, get_output_gene_indexes(parent2)),
                                 exchange_rate=1,
                                 nrows=1)
        self.assertListEqual(child, [[-1, -1, -1], [5, 0, -1], [-2, 1, -2]], "should exchange and format inputs")

        parent1 = [[-1, -1, -1], [0, 0, 0], [1, 0, 0], [-2, 2, -2]]
        parent2 = [[-1, -1, -1], [5, 0, -1], [0, 0, 0], [-2, 1, -2]]
        child = subgraph_exchange(receiver=parent1,
                                 receiver_active_path=get_active_gene_indexes(parent1, get_output_gene_indexes(parent1)),
                                 donor=parent2,
                                 donor_active_path=get_active_gene_indexes(parent2, get_output_gene_indexes(parent2)),
                                 exchange_rate=1,
                                 nrows=1)
        self.assertListEqual(child, [[-1, -1, -1], [0, 0, 0], [5, 0, -1], [-2, 2, -2]], "should exchange and format inputs")

        parent1 = [[-1, -1, -1],[0, 0, 0], [1, 0, 0], [0, 0, 0], [1, 2, 0], [-2, 4, -2]]
        parent2 = [[-1, -1, -1],[3, 0, 0], [0, 0, 0], [5, 1, -1], [0, 0, 0], [-2, 3, -2]]
        child = subgraph_exchange(receiver=parent1,
                                    receiver_active_path=get_active_gene_indexes(parent1, get_output_gene_indexes(parent1)),
                                    donor=parent2,
                                    donor_active_path=get_active_gene_indexes(parent2, get_output_gene_indexes(parent2)),
                                    exchange_rate=1,
                                    nrows=1)
        self.assertListEqual(child, [[-1, -1, -1],[0, 0, 0], [3, 0, 0], [0, 0, 0], [5, 2, -1], [-2, 4, -2]], "should exchange and format inputs")

        # should exchange and format inputs (without throwing an exception)
        child = subgraph_exchange(receiver=test_parent1,
                                 receiver_active_path=get_active_gene_indexes(test_parent1, get_output_gene_indexes(test_parent1)),
                                 donor=test_parent2,
                                 donor_active_path=get_active_gene_indexes(test_parent2, get_output_gene_indexes(test_parent2)),
                                 exchange_rate=1,
                                 nrows=1)
        



    def test_format_inputs_for_new_operation(self):
        # should not change anything
        test_genome_formatting = [[-1, -1, -1], [0, 0, 0], [2, 0, 1], [-2, 2, -2]]
        original_genome = deepcopy(test_genome_formatting)
        format_inputs_for_new_operation(gene=test_genome_formatting[2],
                                        gene_index=2,
                                        new_operation=0,
                                        nrows=1)
        self.assertListEqual(test_genome_formatting, original_genome, "formatting should not change anything")

        test_genome_formatting = [[-1, -1, -1], [0, 0, 0], [2, 0, 1], [-2, 2, -2]]
        original_genome = deepcopy(test_genome_formatting)
        format_inputs_for_new_operation(gene=test_genome_formatting[2],
                                        gene_index=2,
                                        new_operation=1,
                                        nrows=1)
        self.assertListEqual(test_genome_formatting, original_genome, "formatting should not change anything")

        # should have one less input
        test_genome_formatting = [[-1, -1, -1], [0, 0, 0], [2, 0, 1], [-2, 2, -2]]
        format_inputs_for_new_operation(gene=test_genome_formatting[2],
                                        gene_index=2,
                                        new_operation=4, # sin
                                        nrows=1)
        self.assertListEqual(test_genome_formatting, [[-1, -1, -1], [0, 0, 0], [2, 0, -1], [-2, 2, -2]], "formatting should change the inputs")

        # should have one more input
        test_genome_formatting = [[-1, -1, -1], [5, 0, -1], [-2, 2, -2]]
        format_inputs_for_new_operation(gene=test_genome_formatting[1],
                                        gene_index=1,
                                        new_operation=2, # *
                                        nrows=1)
        self.assertListEqual(test_genome_formatting[1], [5, 0, 0] , "formatting should change the inputs")

if __name__ == '__main__':
    unittest.main()