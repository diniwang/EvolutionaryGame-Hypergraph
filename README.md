# Higher-order-StrategyUpdates

Welcome to the repository for paper: Emergence of cooperation promoted by higher-order strategy updates

Authors: Dini Wang, Peng Yi*, Yiguang Hong, Jie Chen and Gang Yan*

The coding program involves the content of the main functions, methods and data, regarding higher-order networks, evolutionary games and illustrations of every figure and table. The first part encompasses hypergraph generators (in Python 3), higher-order data processors (in Python 3) and empirical network datasets; The second part encompasses theoretical calculations (in Python 3) and experimental simulations (in Python 3); The third part encompasses Fig. 2, 3, 4 and 6, as well as Table 1 and S2 in the main text or Supplementary Information.


## Requirements

To be capble to perform the coding program, you should have:

- A recent version of Linux, MacOSX (Mojave or above) or Windows
- Python 3.8 or higher
- NumPy
- SciPy
- Hypergraphx
- NetworkX
- Random
- Numba
- Multiprocessing
- Matplotlib


## Higher-order network

#### Random hypergraph generator

- "random_hg_generator.py" is employed to generate a random hypergraph utilizing the configuration model, in which the degree and the order can follow the uniform, Poisson, and power-law distributions.

- "degreehete_hg_generator.py" is employed to generate a degree-heterogeneous hypergraph with the adjustable exponent of the power-law distribution of the hyperdegree.
  
- "orderhete_hg_generator.py" is employed to generate an order-heterogeneous hypergraph with the adjuastable exponent of the power-law distribution of the order.


#### Higher-order data processor

- "hyperata_processor.py" is employed to process the raw higher-order network datasets and extract the higher-order sub-networks or partial higher-order networks.


#### Empirical network dataset

- "raw_datasets" folder includes the row higher-order netowrk datasets capturing distinct real-life senarios, downloaded from <https://github.com/arbenson/ScHoLP-Data>. The contents are as follows:

  - "contact-higher-school" folder contains a human contact dataset in a high school, where each node is a student and each hyperedge is a group of students in close proximity during an interval.
  - "congress-bills" folder contains a congress bill dataset, where a node is a congressperson and a hyperedge is comprised of the sponsor and co-sponsors of a bill.
  - "email-Eu" folder contains an email network from a European institution, where a node is an email account and a hyperedge involves the sender and all recipients of an email.
  - "threads-math-sc" folder contains an online forum network in the forum Mathematics Stack Exchange, where each node is a user and each hyperedge represents a thread involving multiple users.

  Detailed instructions are shown in each dataset folder.

- "cleaned_datasets" folder includes the above five higher-order netowrk datasets proceesed by "hyperata_processor.py", applicable for Fig. 6c, d of the main text and Table S2 of the Supplementary Information.



## Evolutionary game

#### Theoretical calculation

- "theoretical_calculation_higher.py" is employed to compute the theoretical values of critical synergy factors $r^*$ for higher-order death birth (HDB), higher-order imitation (HIM), group-mutual-comparison (GMC), group-inner-comparison (GIC) and higher-order pair-comparison (HPC) updates, using Equations from Table 1 in the main text.


- "theoretical_calculation_pairwise.py" is employed to compute the theoretical values of critical synergy factors $r^*_G$ for death birth (DB) and pari-comparison (PC) updates, using Equations [143] and [145] in the Supplementary Information.



#### Experimental simulation

- "selection-algorithm.py" is employed to choose an element according to a given probability distribution.

- "game_fitnesses.py" is employed to compute the individual and group fitnesses in each game round.
  
- "strategy_updates.py" is employed to conduct five distint higher-order updates, including birth (HDB), higher-order imitation (HIM), group-mutual-comparison (GMC), group-inner-comparison (GIC) and higher-order pair-comparison (HPC) updates, and two classical pairwise updates, including death-birth (DB) and pair-comparison (PC).

- "evolution_simulations.py" is employed to perform Monto Carlo simulations of evolutionary dynamics on a given hypergraph driven by both higher-order nad pairwise udpates, from the initial configuration of a random mutant to the fixtion state of all cooperators or all defectors. Among these, the probability of all-cooperator occupying the population, known as fixation probability of cooperators, is what we concern about.



## Illustrations of every figure and table

- "figure_2.ipynb" is employed to visualize the random hypergarph shown in Fig. 2a-d of the main text, and plot the fixation probaiblities on four hypergraphs shown in Fig. 2a-d of the main text.

- "figure_3.ipynb" is employed to plot the theoretical critical synergy factors on both homogeneous and heterogenous hypergraphs, as shown in Fig. 3a-d of the main text.
  
- "figure_4.ipynb" is employed to plot the theoretical critical sysnergy factors accroding to varying overlaps of homogeneous hypergraphs, as shown in Fig. 4d and 4h in the main text.

- "figure_6.ipynb" is employed to visualize the congress-bill network and exhibit the fixation probabilities on it governing by different synergy factors and update mechanisms, as shown in Fig. 6c-d in the main text; this file also processes the comparison between higher-order and pairwise udpates, and visualizes highly differentiated hypergraphs of size 7, as shown in Fig. 6e.
