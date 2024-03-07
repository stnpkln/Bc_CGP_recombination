import unittest
from utils import get_genome_column, get_last_possible_input_index, get_number_of_gene_inputs, get_output_gene_indexes

test_genome_small = [
    [-1, -1, -1],   # 0
    [0, 0, 0],      # 1
    [2, 0, 1],      # 2
    [-2, 2, -2]     # 3
]                   # (x + x) * x

class TestUtils(unittest.TestCase):

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