from population import Population
from constants.operations import operations, op_inputs
from typing import List

# PseudoCode for Nodes To Process (CGP Miller)
# 1: NodesToProcess(G,NP) // return the number of nodes to process
# 2: for all i such that 0 ≤ i < M do
# 3: 	NU[i] = FALSE
# 4: end for
# 5: for all i such that Lg −no ≤ i < Lg do
# 6:	NU[G[i]] ← T RUE
# 7: end for
# 8: for all i such that M −1 ≥ i ≥ ni do // Find active nodes
# 9: 	if NU[i] ← T RUE then
# 10: 		index ← nn(i−ni)
# 11: 		for all j such that 0 ≤ j < nn do // store node genes in NG
# 12: 			NG[ j] ← G[index+ j]
# 13: 		end for
# 14: 		for all j such that 0 ≤ j < Arity(NG[nn −1]) do
# 15: 			NU[NG[ j]] ← T RUE
# 16: 		end for
# 17: 	end if
# 18: end for
# 19: nu = 0
# 20: for all j such that ni ≤ j < M do // store active node addresses in NP
# 21: 	if NU[ j] = T RUE then
# 22: 		NP[nu] ← j
# 23: 		nu ← nu +1
# 24: 	end if
# 25: end for
# 26: return nu

# PseudoCode for decoding genotype (CGP Miller)
# 1: DecodeCGP(G,DIN,O,nu,NP,item)
# 2: for all i such that 0 ≤ i < ni do
# 3: 	o[i] ← DIN[item]
# 4: end for
# 5: for all j such that 0 ≤ j < nu do
# 6: 	n ← NP[ j]−ni
# 7: 	g ← nnn
# 8: 	for all i such that 0 ≤ i < nn −1 do // store data needed by a node
# 9: 		in[i] ← o[G[g+i]]
# 10: 	end for
# 11: 	f = G[g+nn −1] // get function gene of node
# 12: 	o[n+ni] = NF(in, f) // calculate output of node
# 13: end for
# 14: for all j such that 0 ≤ j < no do
# 15: 	O[ j] ← o[G[Lg −no + j]]
# 16: end for

# PseudoCode for evaluating fitness (CGP Miller)
# 1: FitnessCGP(G)
# 2: nu ← NodesToProcess(G,NP)
# 3: f it ← 0
# 4: for all i such that 0 ≤ i < Nf c do
# 5: 	DecodeCGP(G,DIN,O,nu,NP,item)
# 6: 	fi = EvaluateCGP(O,DOUT,i)
# 7: 	f it ← f it + fi
# 8: end for

# beru ze vstupni geny maji -1 a vystupni geny maji -2
def get_active_gene_indexes(output_gene_indexes: List[int], genome: List[List[int]]):
    active_genes_indexes = []
    added_to_active_flag = [False] * len(genome)
    for output_gene_index in output_gene_indexes:
        active_genes_indexes.append(output_gene_index)
        added_to_active_flag[output_gene_index] = True

    found_new_gene = True
    gene_indexes_to_search = output_gene_indexes.copy()
    while (found_new_gene):
        new_indexes_to_search = []
        for gene_index_to_search in gene_indexes_to_search:
            gene = genome[gene_index_to_search]
            gene_operation = gene[0]

            # vstupni gen
            if (gene_operation == -1):
                continue

            # vystupni gen
            if (gene_operation == -2):
                input_gene_index = gene[1]
                if (not added_to_active_flag[input_gene_index]):
                    active_genes_indexes.append(input_gene_index)
                    added_to_active_flag[input_gene_index] = True
                    new_indexes_to_search.append(input_gene_index)
                continue

            # funkcni geny
            for i in range(1, 1 + op_inputs[operations[gene_operation]]):
                input_gene_index = gene[i]
                if (not added_to_active_flag[input_gene_index]):
                    active_genes_indexes.append(input_gene_index)
                    added_to_active_flag[input_gene_index] = True
                    new_indexes_to_search.append(input_gene_index)

        found_new_gene = len(new_indexes_to_search) != 0
        gene_indexes_to_search = new_indexes_to_search

    return active_genes_indexes

