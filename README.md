# Bachelor thesis

Practical part of bachelor thesis called "USE OF THE CROSSOVER OPERATOR IN CARTESIAN GENETIC PROGRAMMING".

This code and data does not correspond to the final thesis 1:1, but its very close.

## Abstract
The aim of this work is to propose and implement two new crossover methods in Cartesian
Genetic Programming (CGP) and compare them with existing approaches. CGP is a type
of evolutionary algorithm that uses acyclic graphs to represent executable programs. Most
CGP applications use the mutation operator only, but the effort to find a suitable crossover
operator is still ongoing. In this work, the two newly proposed crossover methods are
compared on five symbolic regression problems against the standard 1 + 𝜆 procedure based
purely on mutation. Experimental results show that these methods find solutions in a similar
number of fitness evaluations as 1 + 𝜆 and, in two cases, even significantly earlier.

## Running automated tests
- in `/src` run `python -m unittest`

## Generate documentation
- in root folder run `./generate-docs.sh`

## Running experiments
- in folder `/src/experiment.py`:
	- uncomment getCGPdata() (commented out because of an error in pdoc framework, which runs code when generating documentation)
- run `python experiment.py`
- experiment outputs will be in `data-general.csv` a `data-run-details.csv`

## Data processing and visualizing
- file `/src/graphs/data_visualizer`
- run `python data_visualizer.py`. `data-general.csv` and `data-run-details.csv` must be in the folder you are running the program
- script generates graphs in pdf format and a csv tablewith processed data of given algorithms

Author: Petr Bromnik
Thesis supervisor: Ing. Martin Hurta
Date: April 2024