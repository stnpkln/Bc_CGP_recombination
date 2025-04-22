from __future__ import annotations
from constants.algorithmEnum import AlgorithmEnum
from evolution import evolve
from genome import genome_output, subgraph_exchange
from population import Population

import unittest
import numpy as np

from tournament_selection import generate_new_population, get_best_group_individual
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

test_genome_good_parent = [
    [-1, -1, -1], # 0
    [0, 0, 0], #    1
    [0, 0, 0], #    2
    [-2, 2, -2] #   3
] # x + x

test_genome_bad = [
    [-1, -1, -1], # 0
    [1, 0, 0], #    1
    [0, 0, 1], #    2
    [-2, 0, -2] #   3
] # x

class TestTournamentSelection(unittest.TestCase):

    def test_generate_generate_new_population(self):
        # testing if children are generated
        population = Population(population_size=4, ncolumns=4, nrows=1, mutation_rate=0.1, nparents=2, wanted_output=[1], input_matrix=[[1]])
        population.set_individual(0, test_genome_best_parent)
        population.set_individual(1, test_genome_good_parent)
        generate_new_population(0, 1, population, 1, subgraph_exchange)
        children = population.get_children()
        self.assertEqual(len(children), 2, "4 children should be generated")
        self.assertEqual(len(children[0]), 4, "children should have the same length as parent")

        parent = population.get_parent()

        for i in range(len(parent)):
            self.assertListEqual(parent[i], test_genome_best_parent[i], "parent should not be changed")
            
    def test_get_best_group_individual(self):
        best_parent_function = lambda x: (x + x) * x
        input_matrix = np.array([np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])])
        wanted_output = np.array(best_parent_function(input_matrix[0]))
        population = Population(population_size=4, ncolumns=4, nrows=1, mutation_rate=0.1, nparents=2, wanted_output=wanted_output, input_matrix=input_matrix)
        population.set_individual(0, test_genome_best_parent)
        population.set_individual(1, test_genome_good_parent)
        best_individual_index, best_fitness = get_best_group_individual([0, 1], population)
        self.assertEqual(best_individual_index, 0, "should return the best individual index")
        self.assertEqual(best_fitness, 0, "should return the best fitness")

    def test_evolve_one_input_float_SE(self):
        def func(input: np.ndarray[np.ndarray[int | float]]) -> np.ndarray[int | float]:
            x = input[0]
            return (x * x) + x

        input = np.array([np.linspace(-1, 1, 20, dtype=float)])

        wanted_output = func(input)
        acceptable_boundary = 0
        solution, fitness, *_, found_solution  = evolve(population_size=4,
               ncolumns=10,
               nrows=1,
               input_matrix=input,
               wanted_output=wanted_output,
               acceptable_boundary=acceptable_boundary,
               max_fitness_evaluations=100000,
               mutation_rate=0.1,
               exchange_rate=0.5,
               algorithm=AlgorithmEnum.SUBGRAPH_EXCHANGE)

        solution_output = genome_output(solution, get_active_gene_indexes(solution, get_output_gene_indexes(solution)), input)

        if found_solution:
            self.assertLessEqual(np.round(fitness, 15), acceptable_boundary, "should find a solution for simple problems")
            self.assertListEqual(np.round(wanted_output, 15).tolist(), np.round(solution_output, 15).tolist(), "solution should be correct")
        else:
            print("no solution found in time in test_evolve_one_input_float_SE")

    def test_evolve_two_inputs_float_SE(self):
        def func(input: np.ndarray[np.ndarray[int | float]]) -> np.ndarray[int | float]:
            x = input[0]
            y = input[1]
            return (x + y) * x

        input = np.array([np.linspace(-1, 1, 20, dtype=float), np.linspace(1, 2, 20, dtype=float)])
        wanted_output = func(input)
        solution, fitness, *_, found_solution = evolve(population_size=4,
            ncolumns=10,
            nrows=2,
            input_matrix=input,
            wanted_output=wanted_output,
            acceptable_boundary=0,
            max_fitness_evaluations=100000,
            mutation_rate=0.1,
            exchange_rate=0.5,
            algorithm=AlgorithmEnum.SUBGRAPH_EXCHANGE)

        solution_output = genome_output(solution, get_active_gene_indexes(solution, get_output_gene_indexes(solution)), input)

        if found_solution:
            self.assertEqual(np.round(fitness, 15), 0, "should find a solution for simple problems")
            self.assertListEqual(wanted_output.tolist(), solution_output.tolist(), "solution should be correct")
        else:
            print("no solution found in time in test_evolve_two_inputs_float_SE")

    def test_evolve_one_input_float_AGT(self):
        def func(input: np.ndarray[np.ndarray[int | float]]) -> np.ndarray[int | float]:
            x = input[0]
            return (x * x) + x

        input = np.array([np.linspace(-1, 1, 20, dtype=float)])

        wanted_output = func(input)
        acceptable_boundary = 0
        solution, fitness, *_, found_solution  = evolve(population_size=4,
               ncolumns=10,
               nrows=1,
               input_matrix=input,
               wanted_output=wanted_output,
               acceptable_boundary=acceptable_boundary,
               max_fitness_evaluations=100000,
               mutation_rate=0.1,
               exchange_rate=0.5,
               algorithm=AlgorithmEnum.PASSIVE_ACTIVE_IMPLANTATION)

        solution_output = genome_output(solution, get_active_gene_indexes(solution, get_output_gene_indexes(solution)), input)

        if found_solution:
            self.assertLessEqual(np.round(fitness, 15), acceptable_boundary, "should find a solution for simple problems")
            self.assertListEqual(np.round(wanted_output, 15).tolist(), np.round(solution_output, 15).tolist(), "solution should be correct")
        else:
            print("no solution found in time in test_evolve_one_input_float_AGT")

    def test_evolve_two_inputs_float_AGT(self):
        def func(input: np.ndarray[np.ndarray[int | float]]) -> np.ndarray[int | float]:
            x = input[0]
            y = input[1]
            return (x + y) * x

        input = np.array([np.linspace(-1, 1, 20, dtype=float), np.linspace(1, 2, 20, dtype=float)])
        wanted_output = func(input)
        solution, fitness, *_, found_solution = evolve(population_size=4,
               ncolumns=10,
               nrows=2,
               input_matrix=input,
               wanted_output=wanted_output,
               acceptable_boundary=0,
               max_fitness_evaluations=100000,
               mutation_rate=0.1,
               exchange_rate=0.4,
               algorithm=AlgorithmEnum.PASSIVE_ACTIVE_IMPLANTATION)

        solution_output = genome_output(solution, get_active_gene_indexes(solution, get_output_gene_indexes(solution)), input)

        if found_solution:
            self.assertEqual(np.round(fitness, 15), 0, "should find a solution for simple problems")
            self.assertListEqual(wanted_output.tolist(), solution_output.tolist(), "solution should be correct")
        else:
            print("no solution found in time in test_evolve_two_inputs_float_AGT")

if __name__ == '__main__':
    unittest.main()