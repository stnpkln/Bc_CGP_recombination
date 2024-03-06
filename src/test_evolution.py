import unittest
from evolution import evolve, generate_new_children, get_fittest_individual
from population import Population

test_genome_best_parent = [
    [-1, -1, -1], # 0
    [0, 0, 0], #    1
    [2, 0, 1], #    2
    [-2, 2, -2] #   3
] # (x + x) * x

test_genome_best_child = [
    [-1, -1, -1], # 0
    [0, 0, 0], #    1
    [2, 1, 0], #    2
    [-2, 2, -2] #   3
] # (x + x) * x

test_genome_good = [
    [-1, -1, -1], # 0
    [0, 0, 0], #    1
    [2, 0, 0], #    2
    [-2, 2, -2] #   3
] # x * x

test_genome_bad = [
    [-1, -1, -1], # 0
    [1, 0, 0], #    1
    [0, 0, 1], #    2
    [-2, 0, -2] #   3
] # x

wanted_function = lambda x: (x + x) * x

class TestGenome(unittest.TestCase):

    def test_get_fittest_individual(self):
        # testing if children with same fitness is chosen over parent
        population = Population(4, 4, 1)
        population.set_parent(test_genome_best_parent)
        population.set_children([test_genome_good, test_genome_bad, test_genome_best_child])
        input = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
        wanted_output = []
        for x in input[0]:
            wanted_output.append(wanted_function(x))
        top_individual, top_fitness = get_fittest_individual(population, input, wanted_output)
        self.assertEqual(top_fitness, 0.0)
        # the only difference between best child and best parent (easier for testing)
        self.assertEqual(top_individual[2][1], 1, "child with same fitness as parent should be chosen")

    def test_generate_new_children(self):
        # testing if children are generated
        population = Population(5, 4, 1)
        generate_new_children(test_genome_best_parent, population)
        children = population.get_children()
        self.assertEqual(len(children), 4, "4 children should be generated")
        self.assertEqual(len(children[0]), 4, "children should have the same length as parent")

        parent = population.get_parent()

        for i in range(len(parent)):
            self.assertListEqual(parent[i], test_genome_best_parent[i], "parent should not be changed")

        # todo maybe some test for children?

    def test_evolve(self):
        func = lambda x: x + x
        input = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
        wanted_output = []
        for x in input[0]:
            wanted_output.append(func(x))
        solution, fitness, generation = evolve(population_size=10,
               ncolumns=10,
               nrows=1,
               input=input,
               wanted_output=wanted_output,
               acceptable_boundary=1,
               max_generations=10000)
        print(f"fitness: {fitness}, generation: {generation}")
        print(f"solution: {solution}")

if __name__ == '__main__':
    unittest.main()