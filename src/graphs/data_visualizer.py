
'''
File: data_visualizer.py
Purpose: Contains functions to visualize the data from the CGP runs
Author: Petr Bromnik
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mannwhitneyu, tstd

def load_general_data(file_path):
	data_general = pd.read_csv(file_path, sep=",", names=['run_id', 'algorithm', 'function', 'fitness_evaluations', 'generations', 'time', 'found_solution'])
	return data_general

def load_run_details_data(file_path):
	data_run_details = pd.read_csv(file_path, sep=",", names=['run_id', 'generation', 'fitness'])
	return data_run_details

def plot_general_by_evaluations(data_general, function):
	function_data = data_general[data_general['function'] == function]
	plt.figure(figsize=(10, 6))
	ax = sns.violinplot(data=function_data,
					 	x="algorithm",
						y="fitness_evaluations",
						hue="algorithm",
						order=["1 + lambda", "Passive Active Implantation", "Subgraph Exchange"],
						palette={"1 + lambda": "white", "Passive Active Implantation": "white", "Subgraph Exchange": "white"},
						linewidth=0,
						inner=None
						)
	sns.violinplot(ax=ax,
					data=function_data,
					x="algorithm",
					y="fitness_evaluations",
					hue="algorithm",
					order=["1 + lambda", "Passive Active Implantation", "Subgraph Exchange"],
					palette={"1 + lambda": "red", "Passive Active Implantation": "blue", "Subgraph Exchange": "green"},
					fill=False,
					inner=None
					)

	sns.swarmplot(ax=ax,
				data=function_data,
				x="algorithm",
				y="fitness_evaluations",
				hue="algorithm",
				order=["1 + lambda", "Passive Active Implantation", "Subgraph Exchange"],
				palette={"1 + lambda": "red", "Passive Active Implantation": "blue", "Subgraph Exchange": "green"})


	ax.set_xticks([0, 1, 2])
	ax.set_xticklabels(["1 + 4", "IAGdN", "VPNC"])
	plt.xticks(fontsize=12)
	plt.xlabel("Algoritmus", fontsize=14)
	plt.ylabel("Počet fitness evaluací", fontsize=14)
	plt.title(function, loc="right", fontsize=16)

	return ax

def plot_fitness_progression(data_run_details, data_general, function):
	function_data = data_general[data_general['function'] == function]
	full_data = pd.merge(function_data, data_run_details, on='run_id', how='left')

	algorithms = ["Passive Active Implantation", "Subgraph Exchange", "1 + lambda"]
	algorithm_acromyns = {"Passive Active Implantation": "IAGdN",
					   "Subgraph Exchange": "VPNC",
					   "1 + lambda": "1 + 4"}

	new_df = pd.DataFrame(columns=["algorithm", 'generation', 'fitness', 'fitness_evaluations'])

	for algorithm in algorithms:
		algo_df = full_data[full_data['algorithm'] == algorithm]
		max_generations = algo_df['generations'].max()
		linspace = np.linspace(1, max_generations, 1000, dtype=int)
		for gen in linspace:
			gen_less_or_equal = algo_df[algo_df['generation'] <= gen]
			fitness_in_gen_per_run = gen_less_or_equal.groupby('run_id').agg({'generation': 'max', 'fitness': 'min'})
			mean_fitness_in_gen = fitness_in_gen_per_run["fitness"].mean()
			fitness_evaluations = gen * 4 if algorithm == "1 + lambda" else gen * 2
			new_df.loc[len(new_df)] = {"algorithm": algorithm_acromyns[algorithm], "generation": gen, "fitness": mean_fitness_in_gen, "fitness_evaluations": fitness_evaluations}

	fig = plt.figure(figsize=(12, 8))

	ax = sns.lineplot(data=new_df, x="fitness_evaluations", y="fitness", hue="algorithm", palette={"1 + 4": "red", "IAGdN": "blue", "VPNC": "green"})
	ax.set(yscale="log", xscale="log")
	ax.set_xlabel("Počet fitness evaluací", fontsize=16)
	ax.set_ylabel("Průměrné fitness", fontsize=16)
	ax.legend(title="Algoritmus", title_fontsize=14, fontsize=14)

	plt.title(function, loc="right", fontsize=18)
	return ax

def plot_nguyen_6_fitness_progression(data_general, data_run_details):
	ax = plot_fitness_progression(data_general=data_general, data_run_details=data_run_details, function="Nguyen 6")
	plt.savefig(f"nguyen_6_fitness_per_generation.png")

def plot_nguyen_8_fitness_progression(data_general, data_run_details):
	ax = plot_fitness_progression(data_general=data_general, data_run_details=data_run_details, function="Nguyen 8")
	plt.savefig(f"nguyen_8_fitness_per_generation.png")

def plot_nguyen_9_fitness_progression(data_general, data_run_details):
	ax = plot_fitness_progression(data_general=data_general, data_run_details=data_run_details, function="Nguyen 9")
	plt.savefig(f"nguyen_9_fitness_per_generation.png")

def plot_nguyen_10_fitness_progression(data_general, data_run_details):
	ax = plot_fitness_progression(data_general=data_general, data_run_details=data_run_details, function="Nguyen 10")
	plt.savefig(f"nguyen_10_fitness_per_generation.png")

def plot_koza_3_fitness_progression(data_general, data_run_details):
	ax = plot_fitness_progression(data_general=data_general, data_run_details=data_run_details, function="Koza 3")
	plt.savefig(f"koza_3_fitness_per_generation.png")

def plot_koza_3_evaluations(data):
	ax = plot_general_by_evaluations(data_general=data, function="Koza 3")
	ax.set_ylim(bottom=0, top=6e6)
	ax.set_yticks([0.0, 1.5e6, 3.0e6, 4.5e6, 6.0e6])
	ax.set_yticklabels(["0.0e+00", "1.5e+06", "3.0e+06", "4.5e+06", "6.0e+06"])
	plt.savefig(f"koza_3_evaluations.png")

def plot_nguyen_10_evaluations(data):
	ax = plot_general_by_evaluations(data_general=data, function="Nguyen 10")
	ax.set_ylim(bottom=0, top=2e4)
	ax.set_yticks([0.0, 5e3, 1e4, 1.5e4, 2e4])
	ax.set_yticklabels(["0.0e+00", "5.0e+03", "1.0e+04", "1.5e+04", "2e+04"])
	plt.savefig(f"nguyen_10_evaluations.png")

def plot_nguyen_9_evaluations(data):
	ax = plot_general_by_evaluations(data_general=data, function="Nguyen 9")
	ax.set_ylim(bottom=0, top=1e7)
	ax.set_yticks([0.0, 2.5e6, 5.0e6, 7.5e6, 1.0e7])
	ax.set_yticklabels(["0.0e+00", "2.5e+06", "5.0e+06", "7.5e+06", "1.0e+07"])
	plt.savefig(f"nguyen_9_evaluations.png")

def plot_nguyen_8_evaluations(data):
	ax = plot_general_by_evaluations(data_general=data, function="Nguyen 8")
	ax.set_ylim(bottom=0, top=1e7)
	ax.set_yticks([0.0, 2.5e6, 5.0e6, 7.5e6, 1.0e7])
	ax.set_yticklabels(["0.0e+00", "2.5e+06", "5.0e+06", "7.5e+06", "1.0e+07"])
	plt.savefig(f"nguyen_8_evaluations.png")

def plot_nguyen_6_evaluations(data):
	ax = plot_general_by_evaluations(data_general=data, function="Nguyen 6")
	ax.set_ylim(bottom=0, top=1e7)
	ax.set_yticks([0.0, 2.5e6, 5.0e6, 7.5e6, 1.0e7])
	ax.set_yticklabels(["0.0e+00", "2.5e+06", "5.0e+06", "7.5e+06", "1.0e+07"])
	plt.savefig(f"nguyen_6_evaluations.png")

def calculate_significance(data, output_path):
	functions = ["Koza 3", "Nguyen 6", "Nguyen 8", "Nguyen 9", "Nguyen 10"]
	algorithms = ["1 + lambda", "Passive Active Implantation", "Subgraph Exchange"]
	new_df = pd.DataFrame(columns=["function", 'algorithm', "mean", "SR", "STD", "Q1", "Q2", "Q3", 'p-value', 'is_significant'])
	for function in functions:
		for algorithm in algorithms:
			one_plus_lambda_evaluations = data[(data['function'] == function) & (data['algorithm'] == "1 + lambda")]['fitness_evaluations']
			algorithm_evaluations = data[(data['function'] == function) & (data['algorithm'] == algorithm)]['fitness_evaluations']

			algorithm_better_significance = mannwhitneyu(algorithm_evaluations, one_plus_lambda_evaluations, alternative="less", method="exact").pvalue
			success_n = len(algorithm_evaluations[algorithm_evaluations < 1e7])
			all_n = len(algorithm_evaluations)
			success_rate = success_n / all_n
			success_rate = round(success_rate, 2)
			standart_deviation = tstd(algorithm_evaluations)
			quartiles = np.percentile(algorithm_evaluations, [25, 50, 75])
			mean = algorithm_evaluations.mean()
			mean = round(mean, 0)

			new_df.loc[len(new_df)] = {"function": function,
							  "algorithm": algorithm,
							  "mean": mean,
							  "SR": success_rate,
							  "STD": standart_deviation,
							  "Q1": quartiles[0],
							  "Q2": quartiles[1],
							  "Q3": quartiles[2],
							  "p-value": algorithm_better_significance if algorithm != "1 + lambda" else "-",
							  "is_significant": algorithm_better_significance < 0.05 if algorithm != "1 + lambda" else "-"}

	new_df.to_csv(output_path, index=False)

data = load_general_data("data-general.csv") # load the general data
detail_data = load_run_details_data("data-run-details.csv") # load the detailed data

# generates violin plots
sns.set_style("darkgrid")
plot_koza_3_evaluations(data)
plot_nguyen_6_evaluations(data)
plot_nguyen_8_evaluations(data)
plot_nguyen_9_evaluations(data)
plot_nguyen_10_evaluations(data)

# generates fitness progression plots
sns.set_style("ticks")
plot_nguyen_6_fitness_progression(data, detail_data)
plot_nguyen_8_fitness_progression(data, detail_data)
plot_nguyen_9_fitness_progression(data, detail_data)
plot_nguyen_10_fitness_progression(data, detail_data)
plot_koza_3_fitness_progression(data, detail_data)

# creates a csv file, which contains general data about the runs of the individual algorithms
calculate_significance(data, "significance.csv")