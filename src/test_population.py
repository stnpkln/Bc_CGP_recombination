import unittest
from population import Population
from constants.operations import operations, op_inputs

class TestPopulation(unittest.TestCase):

    def test_get_random_gene(self):
        # empty population
        with self.assertRaises(ValueError): 
            Population(0, 0, 0)

        # inputs
        p = Population(5, 10, 1)
        gene = p.get_random_gene(0, 0, [])
        self.assertEqual(gene, [-1, -1, -1], "Should be [-1, -1, -1]")
        gene = p.get_random_gene(0, 9, [0] * 9)

        #vystupy
        self.assertEqual(gene[0], -2 , "output gene should have no operation")
        self.assertNotEqual(gene[1], -2 , "output gene should have input")
        self.assertEqual(gene[2], -2 , "output gene should have only one input")

    def test_get_random_genome(self):
        ncols = 100
        nrows = 20
        p = Population(5, ncols, nrows)

        # basic tests
        genome = p.get_random_genome()
        self.assertEqual(len(genome), 2000, "length should be the same as rows * columns")
        self.assertEqual(len(genome[0]), 3, "length of a gene should be 3")
        self.assertEqual(len(genome[ncols]), 3, "length of a gene should be 3")

        # test if all genes are correct
        for i in range(len(genome)):
            gene = genome[i]
            if i < nrows:
                self.assertEqual(gene, [-1, -1, -1], " first gene should be [-1, -1, -1]")
                continue
            if i == (ncols * nrows - 1):
                self.assertEqual(gene[0], -2, "output gene should have no operation")
                self.assertNotEqual(gene[1], -2, "output gene should have input")
                self.assertEqual(gene[2], -2, "output gene should have only one input")
                self.assertTrue(gene[1] in range((len(genome) - 1) - i % nrows), "input should be in range of genome")
                continue

            self.assertTrue(gene[0] in range(len(operations)), f"operation should be in range of operations, received {gene[0]} in a gene with index {i}, but operations have max value {len(operations)}")
            self.assertTrue(gene[1] in range((len(genome) - 1) - i % nrows), f"first input should be in range of genome, got {gene[1]} in a gene with index {i} and genome length {len(genome)}")
            self.assertTrue((gene[2] in range((len(genome) - 1) - i % nrows) or gene[2] == -1), f"second input should be in range of genome, got {gene[2]} in a gene with index {i} and genome length {len(genome)}")

    def test_get_starting_population(self):
        nrows = 10
        ncols = 10
        pupulation_size = 5
        p = Population(pupulation_size, nrows, ncols)
        population = p.get_starting_popultation(5)
        self.assertEqual(len(population), pupulation_size, f"population should have {pupulation_size} genomes")
        for genome in population:
            self.assertEqual(len(genome), nrows * ncols, f"genome should have {nrows * ncols} genes")

    def test_init(self):
        ncols = 10
        nrows = 10
        pupulation_size = 5
        p = Population(pupulation_size, ncols, nrows)

        self.assertEqual(p.ncolumns, ncols, f"ncolumns should be {ncols}")
        self.assertEqual(p.nrows, nrows, f"nrows should be {nrows}")
        self.assertEqual(len(p.population), pupulation_size, f"population should have {pupulation_size} genomes")

        ncols = 50
        nrows = 1
        p = Population(pupulation_size, ncols, nrows)

        self.assertEqual(p.ncolumns, ncols, f"ncolumns should be {ncols}")
        self.assertEqual(p.nrows, nrows, f"nrows should be {nrows}")
        self.assertEqual(len(p.population), pupulation_size, f"population should have {pupulation_size} genomes")

if __name__ == '__main__':
    unittest.main()