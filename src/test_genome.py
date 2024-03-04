import unittest
from genome import get_active_gene_indexes, genome_output
from constants.operations import operations, op_inputs
import numpy as np

test_genome_small = [
    [-1, -1, -1], # 0
    [0, 0, 0], #    1
    [2, 0, 1], #    2
    [-2, 2, -1] #   3
] # (x + x) * x

test_genome = [
            [-1, -1, -1], # 0   | x
            [0, 0, 0], #    1   | 2x
            [2, 0, 1], #    2   | 2x * x
            [2, 1, 1], #    3   | 
            [1, 2, 1], #    4   |
            [0, 1, 2], #    5   | (2x * x) + 2x
            [2, 2, 5], #    6   | (2x * x) * ((2x * x) + 2x)
            [0, 4, 5], #    7
            [2, 6, 6], #    8   | ((2x * x) * ((2x * x) + 2x)) ^ 2
            [-2, 8, -2] #   9
        ] # ((2x * x) * ((2x * x) + 2x)) ^ 2

test_genome_small_multiple_inputs = [
    [-1, -1, -1], # 0   | x
    [-1, -1, -1], # 1   | y
    [0, 0, 1], #    2   | x + y
    [2, 2, 1], #    3   | (x + y) * y
    [-2, 3, -1] #   4   | (x + y) * y
] # (x + y) * y

test_wanted_function = lambda x: (2 * x * x + 2 * x) ** 2

class TestGenome(unittest.TestCase):

    def test_get_active_gene_indexes(self):
        active_genes = get_active_gene_indexes([9], test_genome)
        print(active_genes)
        self.assertEqual(len(active_genes), 6, f"Should be 6, active genes are: {active_genes}")
        self.assertEqual(set(active_genes), set([9, 8, 6, 5, 2, 1]), f"active genes are: {active_genes}, but they sould be 9, 8, 6, 5, 2, 1, 0")

    def test_genome_output(self):
        output = genome_output(test_genome, [[1] * 10])
        self.assertListEqual(np.ndarray.tolist(output), [64] * 10)

        output = genome_output(test_genome, [[0, 1, 2, 3, 4, 4, 3, 2, 1, 0]])
        self.assertListEqual(np.ndarray.tolist(output), [0, 64, 9216, 186624, 1638400, 1638400, 186624, 9216, 64, 0])
        
        output = genome_output(test_genome_small, [[1, 1, 1]])
        self.assertListEqual(np.ndarray.tolist(output), [2, 2, 2])

        output = genome_output(test_genome_small_multiple_inputs, [[1, 1, 1], [2, 2, 2]])
        self.assertListEqual(np.ndarray.tolist(output), [6, 6, 6])


if __name__ == '__main__':
    unittest.main()