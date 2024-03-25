from evolution import evolve, generate_new_population, get_fittest_individual
from genome import genome_output
from population import Population

import unittest
import numpy as np

from utils import get_active_gene_indexes, get_output_gene_indexes

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

class TestEvolution(unittest.TestCase):

    def test_get_fittest_individual(self):
        def func(input: np.ndarray[int | float]) -> np.ndarray[int | float]:
            x = input[0]
            return (x + x) * x

        # testing if children with same fitness is chosen over parent
        population = Population(4, 4, 1, 0.1)
        population.set_parent(test_genome_best_parent)
        population.set_children([test_genome_good, test_genome_bad, test_genome_best_child])
        input = np.array([np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])]) 
        wanted_output = func(input)
        top_individual, top_fitness = get_fittest_individual(population, input, wanted_output)
        self.assertEqual(top_fitness, 0.0)
        # the only difference between best child and best parent (easier for testing)
        self.assertEqual(top_individual[2][1], 1, "child with same fitness as parent should be chosen")

    def test_generate_generate_new_population(self):
        # testing if children are generated
        population = Population(5, 4, 1, 0.1)
        generate_new_population(test_genome_best_parent, population)
        children = population.get_children()
        self.assertEqual(len(children), 4, "4 children should be generated")
        self.assertEqual(len(children[0]), 4, "children should have the same length as parent")

        parent = population.get_parent()

        for i in range(len(parent)):
            self.assertListEqual(parent[i], test_genome_best_parent[i], "parent should not be changed")

    def test_evolve_one_input_int(self):
        def func(input: np.ndarray[np.ndarray[int | float]]) -> np.ndarray[int | float]:
            x = input[0]
            return (x ** 3)

        input = np.array([np.arange(1, 11, 1, dtype=int)])
        wanted_output = func(input)
        solution, fitness, generation, fitness_evaluations = evolve(population_size=10,
               ncolumns=10,
               nrows=1,
               input_matrix=input,
               wanted_output=wanted_output,
               acceptable_boundary=0,
               max_fitness_evaluations=10000,
               mutation_rate=0.1)

        solution_output = genome_output(solution, get_active_gene_indexes(solution, get_output_gene_indexes(solution)), input)
        # print("-------------------")
        # print("ONE INPUT INT")
        # print(f"fitness: {fitness}, generation: {generation}")
        # print(f"solution: {solution}")
        # print(f"wanted output: {wanted_output}")
        # print(f"output of the solution: {solution_output}")
        # print("fitness evaluations: ", fitness_evaluations)

        self.assertEqual(fitness, 0, "should find a solution for simple problems")
        self.assertListEqual(wanted_output.tolist(), solution_output.tolist(), "solution should be correct")

    def test_evolve_one_input_float(self):
        def func(input: np.ndarray[np.ndarray[int | float]]) -> np.ndarray[int | float]:
            x = input[0]
            return (x * x) + x

        input = np.array([np.linspace(-1, 1, 20, dtype=float)])

        wanted_output = func(input)
        acceptable_boundary = 1e-31
        solution, fitness, generation, fitness_evaluations = evolve(population_size=10,
               ncolumns=10,
               nrows=1,
               input_matrix=input,
               wanted_output=wanted_output,
               acceptable_boundary=acceptable_boundary,
               max_fitness_evaluations=10000,
               mutation_rate=0.1)

        solution_output = genome_output(solution, get_active_gene_indexes(solution, get_output_gene_indexes(solution)), input)
        # print("-------------------")
        # print("ONE INPUT FLOAT")
        # print(f"fitness: {fitness}, generation: {generation}")
        # print(f"solution: {solution}")
        # print(f"wanted output: {wanted_output}")
        # print(f"output of the solution: {solution_output}")
        # print("fitness evaluations: ", fitness_evaluations)

        self.assertLessEqual(fitness, acceptable_boundary, "should find a solution for simple problems")
        self.assertListEqual(np.round(wanted_output, 15).tolist(), np.round(solution_output, 15).tolist(), "solution should be correct")

    def test_evolve_two_inputs_int(self):
        def func(input: np.ndarray[np.ndarray[int | float]]) -> np.ndarray[int | float]:
            x = input[0]
            y = input[1]
            return (x + y) * x

        input = np.array([np.arange(1, 11, 1, dtype=int), np.arange(2, 22, 2, dtype=int)])
        wanted_output = func(input)
        solution, fitness, generation, fitness_evaluations = evolve(population_size=10,
               ncolumns=10,
               nrows=2,
               input_matrix=input,
               wanted_output=wanted_output,
               acceptable_boundary=0,
               max_fitness_evaluations=10000,
               mutation_rate=0.1)

        solution_output = genome_output(solution, get_active_gene_indexes(solution, get_output_gene_indexes(solution)), input)
        # print("-------------------")
        # print("TWO INPUTS INT")
        # print(f"fitness: {fitness}, generation: {generation}")
        # print(f"solution: {solution}")
        # print(f"wanted output: {wanted_output}")
        # print(f"output of the solution: {solution_output}")
        # print("fitness evaluations: ", fitness_evaluations)

        self.assertEqual(fitness, 0, "should find a solution for simple problems")
        self.assertListEqual(wanted_output.tolist(), solution_output.tolist(), "solution should be correct")

if __name__ == '__main__':
    unittest.main()