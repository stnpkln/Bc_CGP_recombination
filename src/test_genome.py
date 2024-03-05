import unittest
from genome import evaluate_fitness, get_active_gene_indexes, genome_output, get_genome_column, get_last_possible_input_index, get_number_of_gene_inputs, mutate_gene, mutate_individual
from constants.operations import operations, op_inputs
import numpy as np

test_genome_small = [
    [-1, -1, -1], # 0
    [0, 0, 0], #    1
    [2, 0, 1], #    2
    [-2, 2, -2] #   3
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
        self.assertEqual(len(active_genes), 6, f"Should be 6, active genes are: {active_genes}")
        self.assertEqual(set(active_genes), set([9, 8, 6, 5, 2, 1]), f"active genes are: {active_genes}, but they sould be 9, 8, 6, 5, 2, 1, 0")

    def test_genome_output(self):
        output = genome_output(test_genome, [[1] * 10])
        self.assertListEqual(np.ndarray.tolist(output), [64] * 10, "incorrect genome output")

        output = genome_output(test_genome, [[0, 1, 2, 3, 4, 4, 3, 2, 1, 0]])
        self.assertListEqual(np.ndarray.tolist(output), [0, 64, 9216, 186624, 1638400, 1638400, 186624, 9216, 64, 0], "incorrect genome output with different input values")
        
        output = genome_output(test_genome_small, [[1, 1, 1]])
        self.assertListEqual(np.ndarray.tolist(output), [2, 2, 2], "incorrect genome output with small genome")

        output = genome_output(test_genome_small_multiple_inputs, [[1, 1, 1], [2, 2, 2]])
        self.assertListEqual(np.ndarray.tolist(output), [6, 6, 6], "incorrect genome output in genome with more inputs")
    
    def test_evaluate_fitness(self):
        genome_input = [[0, 1, 2, 3, 4, 4, 3, 2, 1, 0]]
        wanted_output = [0, 64, 9216, 186624, 1638400, 1638400, 186624, 9216, 64, 0]

        self.assertEqual(evaluate_fitness(test_genome, genome_input, wanted_output), 0)

        self.assertTrue(evaluate_fitness(test_genome_small, genome_input, wanted_output) > 0)

    def test_get_number_of_gene_inputs(self):
        gene = [0, 0, 0]
        self.assertEqual(get_number_of_gene_inputs(gene), 2, "incorrect number of inputs for gene")

    def test_get_genome_column(self):
        nrows = 2
        self.assertEqual(get_genome_column(nrows, 0), 0, "incorrect genome row")
        self.assertEqual(get_genome_column(nrows, 1), 0, "incorrect genome row")
        self.assertEqual(get_genome_column(nrows, 2), 1, "incorrect genome row")
        self.assertEqual(get_genome_column(nrows, 9), 4, "incorrect genome row")
    
    def test_last_possible_input_index(self):
        self.assertEqual(get_last_possible_input_index(3, 3, 0), 0, "incorrect last possible input index")
        self.assertEqual(get_last_possible_input_index(3, 3, 1), 0, "incorrect last possible input index")
        self.assertEqual(get_last_possible_input_index(3, 3, 2), 0, "incorrect last possible input index")
        self.assertEqual(get_last_possible_input_index(3, 3, 3), 3, "incorrect last possible input index")
        self.assertEqual(get_last_possible_input_index(3, 3, 4), 3, "incorrect last possible input index")
        self.assertEqual(get_last_possible_input_index(3, 3, 5), 3, "incorrect last possible input index")
        self.assertEqual(get_last_possible_input_index(3, 3, 6), 6, "incorrect last possible input index")
        self.assertEqual(get_last_possible_input_index(3, 3, 7), 6, "incorrect last possible input index")
        self.assertEqual(get_last_possible_input_index(3, 3, 8), 6, "incorrect last possible input index")

        self.assertEqual(get_last_possible_input_index(4, 1, 2), 2, "incorrect last possible input index")

    def test_mutate_gene(self):
        gene, success = mutate_gene([-1, -1, -1], 0, 3, 3)
        self.assertListEqual(gene, [-1, -1, -1], "incorrect mutated gene")
        for i in range(1000):
            gene, success = mutate_gene([0, 0, 0], 5, 3, 3)
            self.assertNotEqual(set(gene), set([0, 0, 0]), "incorrect mutated gene")
            self.assertLess(gene[0], len(operations), "operation out of range after gene mutation")
            self.assertLess(gene[1], 3, "input out of range after gene mutation")
            self.assertLess(gene[2], 3, "input out of range after gene mutation")


    def test_mutate_individual(self):
        gene0 = [-1, -1, -1]
        gene1 = [0, 0, 0]
        gene2 = [2, 0, 1]
        gene3 = [-2, 2, -2]
        test_genome = [gene0, gene1, gene2, gene3]
        mutate_individual(test_genome, 4, 1)

        # checking if the mutation doesnt change the original genome
        self.assertListEqual(test_genome[0], gene0, "mutated genome should not change the original")
        self.assertListEqual(test_genome[1], gene1, "mutated genome should not change the original")
        self.assertListEqual(test_genome[2], gene2, "mutated genome should not change the original")
        self.assertListEqual(test_genome[3], gene3, "mutated genome should not change the original")

        # checking if there is no mutation out of bounds
        for i in range(100):
            mutated_genome = mutate_individual(test_genome, 4, 1)
            for i in range(len(mutated_genome)):
                self.assertLess(mutated_genome[i][0], len(operations), "operation out of range after genome mutation")
                self.assertLess(mutated_genome[i][1], i, "input out of range after genome mutation")
                self.assertLess(mutated_genome[i][2], i, "input out of range after genome mutation")

        # checking if the mutation actually happened
        for i in range(100):
            mutated_genome = mutate_individual(test_genome, 4, 1)
            is_mutated = set(mutated_genome[0]) != set(gene0) or set(mutated_genome[1]) != set(gene1) or set(mutated_genome[2]) != set(gene2) or set(mutated_genome[3]) != set(gene3)
            self.assertTrue(is_mutated, f"mutated genome {mutated_genome} should not be the same as the original {test_genome}")

if __name__ == '__main__':
    unittest.main()