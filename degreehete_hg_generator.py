import numpy as np
from hypergraphx import Hypergraph
from hyperdata_processor import generate_largest_component
from theoretical_calculation_higher import calculation_higher


def degree_hetero_hypergraph(nodesnum, degree_avg, order_avg, alpha_para):
     
    """
    generate an hyperdegree-heterogeneous hypergraph where the hyperdegree sequence
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
    node_wei = [i ** (-alpha_para) for i in range(1, nodesnum+1)]
    node_prob = node_wei / np.sum(node_wei)

    edge_num = int(nodesnum * degree_avg / order_avg)

    hyperedge_lst = []
    for _ in range(edge_num):
        edge = np.random.choice(node_lst, size=order_avg, replace=False, p=node_prob)
        hyperedge_lst.append(edge)

    hypergraph = Hypergraph(hyperedge_lst)
    hypergraph = generate_largest_component(hypergraph)

    return hypergraph


if __name__ == "__main__":   

    nodesnum = 100               # the setting number of the nodes
    degree_avg = 6              # the setting average hyperdegree
    order_avg = 6               # the setting average order 

    alpha_lst = [i for i in np.arange(0.05, 0.99, 0.0001)]

    edgesnum = int(nodesnum*degree_avg/order_avg)               # the number of the hyperedges

    degree_hete = []             # hyperdegree heterogeneity
    degree_hete_hdb = []         # critical synergy factors for HDB with varying hyperdegree heterogeneities
    degree_hete_him = []         # critical synergy factors for HIM with varying hyperdegree heterogeneities
    degree_hete_gmc = []         # critical synergy factors for GMC with varying hyperdegree heterogeneities

    for alpha in alpha_lst:

        H = degree_hetero_hypergraph(nodesnum, degree_avg, order_avg, alpha)
        H_info = calculation_higher(H)

        degree_hete.append(H_info['hyperdegree_hetero'])
        degree_hete_hdb.append(H_info['r_hdb'])
        degree_hete_him.append(H_info['r_him'])
        degree_hete_gmc.append(H_info['r_gmc'])

    file = open(f"./figures_and_table/hyperdegree_hetero.txt",'w')
    for i in degree_hete:
        file.write(str(i) + '\n')
    file.close()

    file = open(f"./figures_and_table/hyperdegree_hetero_hdb.txt",'w')
    for i in degree_hete_hdb:
        file.write(str(i) + '\n')
    file.close()

    file = open(f"./figures_and_table/hyperdegree_hetero_him.txt",'w')
    for i in degree_hete_him:
        file.write(str(i) + '\n')
    file.close()

    file = open(f"./figures_and_table/hyperdegree_hetero_gmc.txt",'w')
    for i in degree_hete_gmc:
        file.write(str(i) + '\n')
    file.close()
