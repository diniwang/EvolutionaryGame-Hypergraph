import numpy as np
import random
import networkx as nx
from hypergraphx import Hypergraph
from hyperdata_processor import generate_largest_component
from theoretical_calculation_higher import calculation_higher


def adjust_power_law_seq(totalnum, average, alpha_para):

    """
    generate a random sequence following the power-law distribution 
    with the ajuestable exponent

    Args:
        totalnum(int): the expected number of the sequence
        average(float): the average value of the sequence
        alpha(float, [0, 1)]): the exponent $\gamma$ of the power-law 
        distribution maintaining $\gamma = (1 + \alpha) / \alpha$

    Returns:
        list: the power-lawer sequence
    """

    node_lst = [i for i in range(totalnum)]
    node_wei = [i ** (-alpha_para) for i in range(1, totalnum+1)]
    node_prob = node_wei / np.sum(node_wei)
    edge_num = int(totalnum * average / 2)

    random_graph = nx.Graph()
    for idx in range(edge_num):
        edge = np.random.choice(node_lst, size=2, replace=False, p=node_prob)
        random_graph.add_edge(*edge)

    degree_sequence = [d for n, d in random_graph.degree()]

    return degree_sequence


def order_hetero_hypergraph(nodesnum, degree_avg, order_avg, alpha_para):

    """
    generate an order-heterogeneous hypergraph where the order sequence
    follows the power-law distribution with the ajuestable exponent

    Args:
        nodesnum(int): the expected number of the hypergraph
        degree_avg(float): the given average hyperdegree of the hypergraph
        degree_avg(float): the given average order of the hypergraph
        alpha(float, [0, 1)]): the exponent $\gamma$ of the power-law 
        distribution maintaining $\gamma = (1 + \alpha) / \alpha$

    Returns:
        hypergraph: the expected hyergraph
    """

    node_lst = [n for n in range(nodesnum)]

    edgesnum = int(nodesnum * degree_avg / order_avg)

    order_seq = adjust_power_law_seq(edgesnum, order_avg, alpha_para)
    order_seq = [i for i in order_seq if (i != 1) and (i != 0)]

    hyperedge_lst = []
    for order in order_seq:
        edge = random.sample(node_lst, order)
        hyperedge_lst.append(edge)

    hypergraph = Hypergraph(hyperedge_lst)
    hypergraph = generate_largest_component(hypergraph)

    return hypergraph


if __name__ == "__main__":   

    nodesnum = 100               # the setting number of the nodes
    degree_avg = 6              # the setting average hyperdegree
    order_avg = 6               # the setting average order 

    alpha_lst = [i for i in np.arange(0.05, 0.99, 0.0001)]

    edgesnum = int(nodesnum * degree_avg / order_avg)               # the number of the hyperedges

    order_hete = []             # order heterogeneity
    order_hete_hdb = []         # critical synergy factors for HDB with varying order heterogeneities
    order_hete_him = []         # critical synergy factors for HIM with varying order heterogeneities
    order_hete_gmc = []         # critical synergy factors for GMC with varying order heterogeneities

    for alpha in alpha_lst:

        H = order_hetero_hypergraph(nodesnum, degree_avg, order_avg, alpha)
        H_info = calculation_higher(H)

        order_hete.append(H_info['order_hetero'])
        order_hete_hdb.append(H_info['r_hdb'])
        order_hete_him.append(H_info['r_him'])
        order_hete_gmc.append(H_info['r_gmc'])


    file = open(f"./figures_and_table/order_hetero.txt",'w')
    for i in order_hete:
        file.write(str(i) + '\n')
    file.close()

    file = open(f"./figures_and_table/order_hetero_hdb.txt",'w')
    for i in order_hete_hdb:
        file.write(str(i) + '\n')
    file.close()

    file = open(f"./figures_and_table/order_hetero_him.txt",'w')
    for i in order_hete_him:
        file.write(str(i) + '\n')
    file.close()

    file = open(f"./figures_and_table/order_hetero_gmc.txt",'w')
    for i in order_hete_gmc:
        file.write(str(i) + '\n')
    file.close()
