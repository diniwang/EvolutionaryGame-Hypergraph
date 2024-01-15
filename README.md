# Evolutionary games on any hypergraph

## About The Project
Welcome to the repository for the manuscript "Evolutionary Games on Hypergraphs". This coding folder encompasses some simulations and datasets, designed to facilitate the analysis of evolutionary game dynamics on hypergraph structures.

### Built With

Built Using Languages
* [Python](https://docs.python.org/3/)

## CalculateThresholds

This subdirectory is dedicated to computing the critical thresholds for PGGs: 
* PGG on hypergraph
* Renormalized PGG on hypergraph
* PGG on simple graph


## EvolutionaryGames

This subfolder is used to simulate five types of processes in evolutionary games, including
* HDB
* HIM
* HPC
* GIC
* GMC


## HypergraphGenerator

This subfolder is used to generate some typical hypergraphs based on the configuration model:
* Regular-regular hypergraph
* Regular-pow hypergraph
* Regular-pow hypergraph with adjustable hyperdegree heterogeneity
* Pow-regular hypergarph
* Pow-regular hypergraph with adjustable order heterogeneity
* Pow-pow hypergraph

## RowData

This subfolder contains nine datasets concerning with higher-order interatcions:
* Coauthorship from DBLP
* Coauthorship from Geology field in MAG
* Congress bills
* Human contact in a high school
* Human contact in a primary school
* Email communication from Enron Corporation
* Email communication from an European institution
* Online thread forum from Ask Ubuntu
* Online thread forum from Mathematics Stack Exchange
  
Detailed instructions are shown in each dataset folder.


## ProcessedData

This subfolder includes the processed datasets. In each dataset, there are three significant components, that is 
* Vertices
* Hyperedges
* Hyperedge weights


## DataProcessor

This Jupyter file is used to extract the hypergraph from the dataset.


## SI-Error

This subfolder is used to computer the error due to mean-field estimation in the Supplymentary information.
