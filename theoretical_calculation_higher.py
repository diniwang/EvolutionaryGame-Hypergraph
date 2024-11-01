import numpy as np
from hypergraphx import Hypergraph
from hypergraphx.linalg.linalg import incidence_matrix

# Compute the theoretical critical synergy factors of a specific hypergraph for higher-order strategy updates, 
# including higher-order death-birth (HDB), higher-order imitation (HIM), group-mutual comparison (GMC), group-inner 
# comparison (GIC) and higher-order pair-comparison (PC).


def calculation_higher(hypergraph_data):

        """
        #Compute the theoretical critical synergy factors of a specific hypergraph for higher-order strategy updates, 
        # including higher-order death-birth (HDB), higher-order imitation (HIM), group-mutual comparison (GMC), group-inner 
        # comparison (GIC) and higher-order pair-comparison (PC).
        """

        hypergraph_info = {}

        nodesnum = hypergraph_data.num_nodes()                # number of nodes
        hypergraph_info["num_of_nodes"] = nodesnum

        edgesnum = hypergraph_data.num_edges()                # number of edges
        hypergraph_info["num_of_hyperedges"] = edgesnum

        Incidence_mat = incidence_matrix(hypergraph_data).todense()       # incidence matrix

        Hyperdegree_seq = Incidence_mat.sum(axis=1)
        Hyperdegree_mat = np.diag(Hyperdegree_seq)              # hyperdegree matrix
        hypergraph_info["average_hyperdegree"] = np.mean(Hyperdegree_seq)     # average hyperdegree
        Hyperdegree_sec_seq = Hyperdegree_seq * Hyperdegree_seq
        hyperdegree_hetero = np.mean(Hyperdegree_sec_seq) / (np.mean(Hyperdegree_seq)**2)
        hypergraph_info["hyperdegree_hetero"] = hyperdegree_hetero     # hyperdegree heterogeneity

        Pi_mat = (1/(Hyperdegree_mat.trace())) * Hyperdegree_mat                # stational distribution matrix

        Order_seq = Incidence_mat.sum(axis=0)
        Order_mat = np.diag(Order_seq)          # order matrix
        hypergraph_info["average_order"] = np.mean(Order_seq)         # average order
        Order_sec_seq = Order_seq * Order_seq
        order_hetero = np.mean(Order_sec_seq) / (np.mean(Order_seq)**2)
        hypergraph_info["order_hetero"] = order_hetero     # order heterogeneity


        Order_exc_mat = Order_mat - np.eye(edgesnum)       # order matrix excluding oneself

        Payoff_mat = np.linalg.inv(Hyperdegree_mat) @ Incidence_mat @ Incidence_mat.T         # payoff matrix

        Adjacent_exc_mat = Incidence_mat @ np.linalg.inv(Order_exc_mat) @ Incidence_mat.T
        for i in range(nodesnum):
                Adjacent_exc_mat[i][i] = 0                      # adjacent matrix without self-loops

        Adjacent_mat = Incidence_mat @ np.linalg.inv(Order_mat) @ Incidence_mat.T     # adjacent matrix with self-loops

        Trasition_exc_mat = np.linalg.inv(Hyperdegree_mat) @ Adjacent_exc_mat            # trasition probability matrix without self-loops

        Trasition_mat = np.linalg.inv(Hyperdegree_mat) @ Adjacent_mat            # trasition probability matrix with self-loops

        ## theoretical value of HDB
        r_hdb = ((Pi_mat @ (np.eye(nodesnum) + Trasition_exc_mat)).trace() - 2 * (Pi_mat @ Pi_mat).trace()) / ((Pi_mat @ (Payoff_mat + \
                Trasition_exc_mat @ Payoff_mat)).trace() - 2 * (Pi_mat @ Payoff_mat @ Pi_mat).sum())
        hypergraph_info["r_hdb"] = r_hdb

        ## theoretical value of HIM
        r_him = ((Pi_mat @ (np.eye(nodesnum) +  Trasition_mat)).trace() - 2 * (Pi_mat @ Pi_mat).trace()) / ((Pi_mat @ (Payoff_mat + \
                Trasition_mat @ Payoff_mat)).trace() - 2 * (Pi_mat @ Payoff_mat @ Pi_mat).sum())
        hypergraph_info["r_him"] = r_him

         ## theoretical value of GMC
        r_gmc = ((Pi_mat @  Trasition_mat).trace() - (Pi_mat @ Pi_mat).trace()) / ((Pi_mat @ Trasition_mat @ Payoff_mat).trace() - \
                (Pi_mat @ Payoff_mat @ Pi_mat).sum())
        hypergraph_info["r_gmc"] = r_gmc

        ## theoretical value of GIC
        r_gic = ((Pi_mat @ np.eye(nodesnum)).trace() - (Pi_mat @ Pi_mat).trace()) / ((Pi_mat @ Payoff_mat).trace() - \
                (Pi_mat @ Payoff_mat @ Pi_mat).sum())
        hypergraph_info["r_gic"] = r_gic

        ## theoretical value of HPC
        r_hpc = ((Pi_mat @ np.eye(nodesnum)).trace() - (Pi_mat @ Pi_mat).trace()) / ((Pi_mat @ Payoff_mat).trace() - \
                (Pi_mat @ Payoff_mat @ Pi_mat).sum())
        hypergraph_info["r_hpc"] = r_hpc

        return hypergraph_info


if __name__ == "__main__":
    
        # dataset = "congress-bills"
        dataset = "coauth-DBLP"

        file_hyperedge = open(f'./cleaned_datasets/{dataset}-hyperedges.txt')
        hyperedge = file_hyperedge.readlines()
        hyperedge_lst = []
        for edge in hyperedge:
                edge = edge.strip('\n').split(",")
                hyperedge_lst.append([int(n) for n in edge])

        H = Hypergraph(hyperedge_lst)           # hypergraph construction
        theoretical_solution = calculation_higher(H)

        print(theoretical_solution)
