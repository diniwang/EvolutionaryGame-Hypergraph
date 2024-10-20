import numpy as np

from hypergraphx import Hypergraph
from hypergraphx.linalg.linalg import incidence_matrix



if __name__ == "__main__":

    dataset = "congress-bills"          # Select the dataset

    file_hyperedge = open(f'./cleaned_datasets/{dataset}-hyperedges.txt')

    hyperedge = file_hyperedge.readlines()
    
    hyperedge_lst = []
    for i in hyperedge:
        i = i.strip('\n').split(",")
        hyperedge_lst.append([int(t) for t in i])

    H = Hypergraph(hyperedge_lst)           # Construct the hypergraph

    node_lst = H.get_nodes()                # Node list

    nodesnum = len(node_lst)                # Number of nodes

    Incidence_mat = incidence_matrix(H).todense()       # Incidence matrix

    Hyperdegree_seq = Incidence_mat.sum(axis=1)
    Hyperdegree_mat = np.diag(Hyperdegree_seq)       # Hyperdegree matrix

    Pi_mat = (1/(Hyperdegree_mat.trace())) * Hyperdegree_mat                # Stational distribution matrix

    Order_seq = Incidence_mat.sum(axis=0)
    Order_mat = np.diag(Order_seq)       # Order matrix

    Order_exc_seq = Incidence_mat.sum(axis=0) - 1
    Order_exc_mat = np.diag(Order_exc_seq)       # Order matrix excluding oneself

    Payoff_mat = np.linalg.inv(Hyperdegree_mat) @ Incidence_mat @ Incidence_mat.T         # Payoff matrix

    Adjacent_exc_mat = Incidence_mat @ np.linalg.inv(Order_exc_mat) @ Incidence_mat.T
    for i in range(nodesnum):
        Adjacent_exc_mat[i][i] = 0                      # Adjacent matrix without self-loops

    Adjacent_mat = Incidence_mat @ np.linalg.inv(Order_mat) @ Incidence_mat.T     # Adjacent matrix with self-loops

    Trasition_exc_mat = np.linalg.inv(Hyperdegree_mat) @ Adjacent_exc_mat            # Trasition probability matrix without self-loops

    Trasition_mat = np.linalg.inv(Hyperdegree_mat) @ Adjacent_mat            # Trasition probability matrix with self-loops

    # Theoretical value of HDB
    r_hdb = ((Pi_mat @ (np.eye(nodesnum) + Trasition_exc_mat)).trace() - 2 * (Pi_mat @ Pi_mat).trace()) / ((Pi_mat @ (Payoff_mat + \
            Trasition_exc_mat @ Payoff_mat)).trace() - 2 * (Pi_mat @ Payoff_mat @ Pi_mat).sum())
    print("Theoretical critical synergy factor for HDB: ", r_hdb)

    # Theoretical value of HIM
    r_him = ((Pi_mat @ (np.eye(nodesnum) +  Trasition_mat)).trace() - 2 * (Pi_mat @ Pi_mat).trace()) / ((Pi_mat @ (Payoff_mat + \
            Trasition_mat @ Payoff_mat)).trace() - 2 * (Pi_mat @ Payoff_mat @ Pi_mat).sum())
    print("Theoretical critical synergy factor for HIM: ", r_him)

    # Theoretical value of GIC
    r_gic = ((Pi_mat @ np.eye(nodesnum)).trace() - (Pi_mat @ Pi_mat).trace()) / ((Pi_mat @ Payoff_mat).trace() - \
            (Pi_mat @ Payoff_mat @ Pi_mat).sum())
    print("Theoretical critical synergy factor for GIC: ", r_gic)

    # Theoretical value of GMC
    r_gmc = ((Pi_mat @  Trasition_mat).trace() - (Pi_mat @ Pi_mat).trace()) / ((Pi_mat @ Trasition_mat @ Payoff_mat).trace() - \
            (Pi_mat @ Payoff_mat @ Pi_mat).sum())
    print("Theoretical critical synergy factor for GMC: ", r_gmc)

    # Theoretical value of HPC
    r_hpc = ((Pi_mat @ np.eye(nodesnum)).trace() - (Pi_mat @ Pi_mat).trace()) / ((Pi_mat @ Payoff_mat).trace() - \
            (Pi_mat @ Payoff_mat @ Pi_mat).sum())
    print("Theoretical critical synergy factor for HPC: ", r_hpc)
