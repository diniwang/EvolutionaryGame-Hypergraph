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



## Higher-order network

#### Random hypergraph generator

- "random_hypergraph_generator.py" is employed to generate a random hypergraph utilizing the configuration model.

  - Input: 
    - the number of nodes for a to-be-generated hypergraph
    - the average hyperdegree for a to-be-generated hypergraph
    - the average order for a to-be-generated hypergraph
    - the hyperdegree distribution for a to-be-generated hypergraph
    - the order distribution for a to-be-generated hypergraph
    
  - Output: 
    - the node list of the generated hypergraph
    - the hyperedge list of the generated hypergraph


#### higher-order data processor

- "higher_order_data_processor.py" is employed to process the raw higher-order network datasets and extract the higher-order sub-networks or partial higher-order networks.
  
  - Input:
    - the raw higher-order network dataset
  
  - Output:
    - the node list of the processed higher-order network
    - the hyperedge list of the processed higher-order network


#### Empirical network dataset

- "raw_datasets" folder includes five row higher-order netowrk datasets capturing distinct real-life senarios, downloaded from <https://github.com/arbenson/ScHoLP-Data>. The contents are as follows:

  - Coauthorship
  - Human contact
  - Congress bills
  - Email
  - Online forum

  Detailed instructions are shown in each dataset folder.


- "cleaned_datasets" folder includes the above five higher-order netowrk datasets proceesed by "higher_order_data_processor.py", applicable for Fig. 6c, d of the main text and Table S2 of the Supplementary Information.



## Evolutionary game

#### Theoretical calculation

- "theoretical_calculation_higher.py" is employed to compute the theoretical values of critical synergy factors $r^*$ for higher-order death birth (HDB), higher-order imitation (HIM), group-mutual-comparison (GMC), group-inner-comparison (GIC) and higher-order pair-comparison (HPC) updates, using Equations from Table 1 in the main text.

  - Input: 
    - the node list of any given hypergraph
    - the hyperedge list of any given hypergraph
    
  - Output: 
    - critical synergy factor $r^*$

- "theoretical_calculation_pairwise.py" is employed to compute the theoretical values of critical synergy factors $r^*_G$ for death birth (DB) and pari-comparison (PC) updates, using Equations [143] and [145] in the Supplementary Information.

  - Input: 
    - the node list of any given hypergraph
    - the hyperedge list of any given hypergraph
    
  - Output: 
    - critical synergy factor $r^*_G$


#### Experimental simulation

- "fixation_probability_simulations.py" is employed to perform Monto Carlo simulations of evolutionary dynamics on a given hypergraph driven by higher-order death birth (HDB), higher-order imitation (HIM), group-mutual-comparison (GMC), group-inner-comparison (GIC) and higher-order pair-comparison (HPC) updates, from the initial configuration of a random mutant to the fixtion state of all cooperators or all defectors. Among these, the probability of all-cooperator occupying the population, known as fixation probability of cooperators, is what we concern about.
  
   - Input:
     - the node list of any give hypergraph
     - the hyperedge list of any give hypergraph
     - the type of the strategy update
     - the given synergy factor
  
   - Output:
     - fixation probability of cooperators



## Illustrations of every figure and table

#### Figure 2

- "Hypergraph_visualization.ipynb" is employed to visulize the random hypergraphs shown in Fig. 2a-d of the main text.
- "fixation_plot" is employed to plot the fixation probaiblities on four hypergraphs shown in Fig. 2a-d of the main text.
  

#### Figure 3
- "varying_property_plot.ipynb" is employed to plot the theoretical critical synergy factors on various hypergraphs, as shown in Fig. 3a-d of the main text.


#### Figure 4
- "overlap_plot.ipynb" is employed to plot the theoretical critical synergy factors on hypergraphs with varying overlaps, as shown in Fig. 4d, h of the main text.
  

#### Figure 6
- "congress_bill_plot.ipynb" is employed to visulize the congress bill networks and plot the fixation probabilities for higher-order and pairwise updates, as shown in Fig. 6c, d of the main text.
- "small_scale_plot.ipynb" is employed to plot the theoretical critical synergy factors for higher-order and pairwise updates on small-sacle higher-order networks, and visulize the six hypergraphs with the smallest $r^* / r^*_G$.
