import random
import numpy as np
import networkx as nx
from hypergraphx import Hypergraph
from hyperdata_processor import generate_largest_component

# Generate a random hypergraph utilizing the configuration model, in which the degree
# and the order can follow the uniform, Poisson, and power-law distributions.


def uniform_seq(totalnum, average):

    """
    generate a uniform sequence

    Args:
        totalnum(int): the expected number of the sequence
        average(float): the average value of the sequence

    Returns:
        list: the uniform sequence
    """

    sequence = [average] * totalnum
    return sequence


def poisson_seq(totalnum, average):

    """
    generate a random sequence following the Poisson distribution 
    by extracting the degree sequence from a ER network

    Args:
        totalnum(int): the expected number of the sequence
        average(float): the average value of the sequence

    Returns:
        list: the Poisson sequence
    """

    ER_graph = nx.erdos_renyi_graph(totalnum, average/totalnum)
    degree_sequence = [d for n, d in ER_graph.degree()]

    return degree_sequence


def power_seq(totalnum, average):

    """
    generate a random sequence following the power-law distribution 
    by extracting the degree sequence from a BA network

    Args:
        totalnum(int): the expected number of the sequence
        average(float): the average value of the sequence

    Returns:
        list: the power-law sequence
    """

    BA_graph = nx.barabasi_albert_graph(totalnum, int(average/2))
    degree_sequence = [d for n, d in BA_graph.degree()]

    return degree_sequence


def configuration_model(nodesnum, edgesnum, degree_lst, order_lst, step):

    """
    generate a random hypergraph according to the given hyperdegree and 
    order sequences using the cofiguration model

    Args:
        nodesnum(int): the setting number of nodes
        edgesnum(int): the setting number of hyperedges
        degree_lst(list): the given hyperdegree list
        order_lst(list): the given order list
        step(int): the maximum step of cycles

    Returns:
        (hypergraph): the generated random hypergraph
    """

    for _ in range(step):

        same = False

        hypergraph = Hypergraph()

        total_node_lst = []
        for node_idx in range(nodesnum):
            total_node_lst += [node_idx] * degree_lst[node_idx]

        hyperedge_lst = []
        for edge_idx in range(edgesnum):

            if len(set(total_node_lst)) < order_lst[edge_idx]:
                break

            hyperedge_lst.append([])    

            for node_idx in range(order_lst[edge_idx]):
                hyperedge_lst[edge_idx].append(random.choice(total_node_lst))

                while(len(set(hyperedge_lst[edge_idx])) != len(hyperedge_lst[edge_idx])): 
                    hyperedge_lst[edge_idx][node_idx] = random.choice(total_node_lst)

            for node in hyperedge_lst[edge_idx]:                                    
                total_node_lst.remove(node)         # remove the selected nodes

        ## Each hyperedge cannot be identical.
        for i in range(edgesnum):
            for j in range(i+1, edgesnum):
                if i < len(hyperedge_lst) and j < len(hyperedge_lst) \
                and hyperedge_lst[i] == hyperedge_lst[j]:
                    same = True
                    break
            if same:
                break
        if same:
            continue
        else:
            hypergraph = Hypergraph(hyperedge_lst)

    if hypergraph.num_nodes() > 0:
        hypergraph = generate_largest_component(hypergraph)
        return hypergraph

    elif hypergraph.num_nodes() == 0:
        return "cannot generate the hypergraph in the given step"


if __name__ == "__main__":   

    degree_dist = 'uniform'     # hyperdegree distribution
    # degree_dist = 'poisson'
    # degree_dist = 'power'

    order_dist = 'uniform'      # order distribution 
    # order_dist = 'poisson'
    # order_dist = 'power'

    nodesnum = 60               # the setting number of the nodes
    degree_avg = 3              # the setting average hyperdegree
    order_avg = 3               # the setting average order 

    edgesnum = int(nodesnum*degree_avg/order_avg)               # the number of the hyperedges

    if degree_dist == 'uniform':
        degree_lst = uniform_seq(nodesnum, degree_avg)      # hyperdegree sequence following the uniform distribution
    elif degree_dist == 'poisson':
        degree_lst = poisson_seq(nodesnum, degree_avg)     # hyperdegree sequence following the Poisson distribution
    elif degree_dist == 'power':
        degree_lst = power_seq(nodesnum, degree_avg)     # hyperdegree sequence following the power-law distribution
    
    if order_dist == 'uniform':
        order_lst = uniform_seq(edgesnum, order_avg)        # order sequence following the uniform distribution
    elif order_dist == 'poisson':
        order_lst = poisson_seq(edgesnum, order_avg)     # order sequence following the Poisson distribution
    elif order_dist == 'power':
        order_lst = power_seq(edgesnum, order_avg)     # order sequence following the power-law distribution

    step = int(1e4)         # number of repeated steps

    H = configuration_model(nodesnum, edgesnum, degree_lst, order_lst, step)
    print(H)

    if not isinstance(H, str):

        file = open(f"./random_datasets/{order_dist}-{degree_dist}_hg.txt",'w')

        for edge in H.get_edges():
            edge = str(edge).replace('(','').replace(')','') + '\n'
            file.write(edge)

        file.close()
