import unittest
from genome import get_active_gene_indexes
from constants.operations import operations, op_inputs

class TestGenome(unittest.TestCase):

    def test_get_active_gene_indexes(self):
        genome = [
            [-1, -1, -1], # 0
            [-1, -1, -1], # 1
            [2, 0, 1], # 2
            [3, 1, 1], # 3
            [1, 2, 1], # 4
            [0, 1, 2], # 5
            [3, 2, 5], # 6
            [0, 4, 5], # 7
            [2, 6, 6], # 8
            [-2, 8, -2] # 9
        ]
        active_genes = get_active_gene_indexes([9], genome)
        self.assertEqual(len(active_genes), 7, f"Should be 7, active genes are: {active_genes}")
        self.assertTrue(set(active_genes), set(9, 8, 6, 5, 2, 1, 0), f"active genes are: {active_genes}, but they sould be 9, 8, 6, 5, 2, 1, 0")


if __name__ == '__main__':
    unittest.main()