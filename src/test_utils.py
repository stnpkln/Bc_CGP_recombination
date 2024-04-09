from utils import get_active_gene_indexes, get_genome_column, get_last_possible_input_index, get_number_of_gene_inputs, get_output_gene_indexes

import unittest

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

class TestUtils(unittest.TestCase):

    def test_get_active_gene_indexes(self):
        active_genes = get_active_gene_indexes(test_genome, [9])
        self.assertEqual(len(active_genes), 6, f"Should be 6, active genes are: {active_genes}")
        self.assertEqual(set(active_genes), set([9, 8, 6, 5, 2, 1]), f"active genes are: {active_genes}, but they sould be 9, 8, 6, 5, 2, 1, 0")

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

    def test_get_output_gene_indexes(self):
        self.assertListEqual([3], get_output_gene_indexes(test_genome_small), "incorrect output gene indexes")
        pass

if __name__ == '__main__':
    unittest.main()