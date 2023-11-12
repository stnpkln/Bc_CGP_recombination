# Poznámky k bakalářské práci

## Zdroje přečtené:
- [Cartesian Genetic Programming](https://link.springer.com/book/10.1007/978-3-642-17310-3) (z1)
- [Cartesian genetic programming: its status and future](https://link.springer.com/article/10.1007/s10710-019-09360-6) (z2)
- [Towards Discrete Phenotypic Recombination in Cartesian Genetic Programming](https://link.springer.com/chapter/10.1007/978-3-031-14721-0_5) (z3)

## Zdroje ke zvážení:
- [Positional Independence and Recombination in Cartesian Genetic Programming](https://link.springer.com/chapter/10.1007/11729976_32)
- [A New Crossover Technique for Cartesian Genetic Programming](https://www.researchgate.net/publication/220742582_A_new_crossover_technique_for_Cartesian_genetic_programming)

## Body ke kterým by se hodilo vyhledat informace a citace:
1.	Lehký úvod do CGP (částečně možná popsat vlastními slovy, ale je lepší mít z čeho vycházet)
2.	Proč je problém s křížením?
3.	Jak funguje CGP bez křížení
4.	Vymyšlené algoritmy křížení
5.	Plusy, nedostatky daných algorytmů
6.	???

## 1. Lehký úvod do CGP

### Co je to bloat? (z1)
>When evolutionary algorithms are applied to many representations of programs, a
>phenomenon called bloat happens. This is where, as the generations proceed, the
>chromosomes become larger and larger without any increase in fitness. Such programs generally have large sections of code that contain inefficient or redundant
>subexpressions. This can be a handicap, as it can mean that processing such bloated
>programs is time-consuming. Eventually, an evolved program could even exceed
>the memory capacity of the host computer. In addition, the evolved solutions can be
>very hard to understand and are very inelegant. There are many theories about the
>causes of bloat and many proposed practical remedies [36, 37, 41]. It is worth noting
>that Cartesian GP cannot suffer from genotype growth, as the genotype is of fixed
>size; in addition, it also appears not to suffer from phenotypic growth [27]. Indeed, it
>will be seen that program sizes remain small even when very large genotype lengths
>are allowed

### Proč "Kartezske" geneticke programovani? (z1)
>It is called ‘Cartesian’ because it represents a program
>using a two-dimensional grid of nodes

### Obecná struktura CGP (z1)
>In CGP, programs are represented in the form of directed acyclic graphs. These
>graphs are represented as a two-dimensional grid of computational nodes. The genes
>that make up the genotype in CGP are integers that represent where a node gets its
>data, what operations the node performs on the data and where the output data required by the user is to be obtained.


### Co jsou to "non-coding" uzly (z1)
>When the genotype is decoded, some nodes may be ignored.
>This happens when node outputs are not used in the calculation of output data.
>When this happens, we refer to the nodes and their genes as "non-coding".

### Genotyp a fenotyp a jejich velikost v CGP (z1)
>We call the program that results from the decoding of a genotype a phenotype. The
>genotype in CGP has a fixed length. However, the size of the phenotype (in terms of
>the number of computational nodes) can be anything from zero nodes to the number
>of nodes defined in the genotype.

Dá se teda říct že genotyp se skládá z veškerých uzlů které jedinec obsahuje.
Fenotyp se pak skládá z uzlů (nebo spíše z jejich přeložení), které nejsou "non-coding" - tedy jsou "encoding" hádám.

### Typy genů v uzlech (function vs connection) (z1)
>In CGP, each node in the directed graph represents a particular function and is encoded by a number of genes. One gene is
>the address of the computational node function in the function look-up table. We
>call this a ***function gene***. The remaining node genes say where the node gets its data
>from. These genes represent addresses in a data structure (typically an array). We
>call these ***connection genes***.

### Typy funkcí v uzlech (z1)
>The types of computational node functions used in CGP are decided by the user
and are listed in a function look-up table

### Odkud berou uzly své vstupy (z1)
>Nodes take their inputs in a feed-forward manner from
either the output of nodes in a previous column or from a program input (which is
sometimes called a terminal).

### Počet vstupů do uzlu (z1)
>The number of connection genes a node has is chosen
>to be the maximum number of inputs (often called the arity) that any function in
the function look-up table has.

### Volitelné parametry CGP (z1)
>CGP has three parameters that are chosen by the user. These are the ***number
>of columns***, the ***number of rows*** and ***levels-back***. These are denoted by nc, nr and
>l, respectively. The product of the first two parameters determine the maximum
>number of computational nodes allowed: Ln = ncnr. The parameter l controls the
>connectivity of the graph encoded. Levels-back constrains which columns a node
>can get its inputs from. If l = 1, a node can get its inputs only from a node in the
>column on its immediate left or from a primary input.

### Dekódování Genotypu (z1)
>the algorithmic process is recursive in nature and works from the output
>genes first. The process begins by looking at which nodes are ‘activated’ by being
>directly addressed by output genes. Then these nodes are examined to find out which
>nodes they in turn require.

## 2. Problémy s křížením

### Původní křížení v CGP (z1)
>Crossover operators have received relatively little attention in CGP. Originally, a
>one-point crossover operator was used in CGP (similar to the n-point crossover in
>genetic algorithms) but was found to be disruptive to the subgraphs within the chromosome, and had a detrimental affect on the performance of CGP [5].

## 3. Jak funguje CGP bez operátoru křížení
- ***TODO*** najít nějaký vhodný zdroj který toto možná popisuje? Možná jen popsat mými slovy?
- Využívá se pouze operátor pro mutace
- Důležitý pojem - ***neutral drift*** - v podstatě mutace "non-coning" genů které se neprojeví na FIT hodnocení jednotlivce, ale pomáhá aby algorytmus nezůstal v lokálním minimu

### Neutral drift
>We have already seen that in a CGP genotype there may be genes that are entirely
>inactive, having no influence on the phenotype and hence on the fitness. Such inactive genes therefore have a neutral effect on genotype fitness. This phenomenon is
>often referred to as neutrality. CGP genotypes are dominated by redundant genes.
>For instance, Miller and Smith showed that in genotypes having 4000 nodes, the
>percentage of inactive nodes is approximately 95%! [6].



## 4. Možné algoritmy křížení

### FP crossover operátor (z1)
>Some work by Clegg et al. [2] has investigated crossover in CGP (and GP in general).
> Their approach uses a floating-point crossover operator, similar to that found in evolutionary programming, and also adds an extra >layer of encoding to the genotype, in which all genes are encoded as a floating-point number in the range [0,1].
A larger population and tournament selection were also used instead of the (1 + 4) evolutionary strategy normally used in CGP, to tr>y and improve the population diversity. 
The results of the new approach appear promising when applied to two symbolic regression problems, but further work is required on a >range of problems in order to assess its advantages [2].

### Nalezená využití operátoru křížení (z1)
>Crossover has also been found to be useful in an imageprocessing application as discussed in Sect. 6.4.3. Crossover operators (cone-based
>crossover) have been devised for digital-circuit evolution (see Sect. 3.6.2). In situations where a CGP genotype is divided into a collection of chromosomes, crossover
>can be very effective. Sect. 3.8 discusses how new genotypes created by selecting
>the best chromosomes from parents’ genotypes can produce super-individuals. This
>allows difficult multiple-output problems to be solved.

***TODO najít si definici cone-based crossover***