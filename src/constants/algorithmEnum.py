'''
File: algorithmEnum.py.py
Purpose: Contains the AlgorithmEnum enum class and name dictionary
Author: Petr Bromnik
'''

import enum

class AlgorithmEnum(enum.Enum):
	MUTATION_ONLY = 1
	SUBGRAPH_EXCHANGE = 2
	PASSIVE_ACTIVE_IMPLANTATION = 3

algorithm_names = {
	AlgorithmEnum.MUTATION_ONLY: "1 + lambda",
	AlgorithmEnum.SUBGRAPH_EXCHANGE: "Subgraph Exchange",
	AlgorithmEnum.PASSIVE_ACTIVE_IMPLANTATION: "Passive Active Implantation"
}