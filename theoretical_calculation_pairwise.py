import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix
from scipy.sparse import triu
from hypergraphx import Hypergraph
from hypergraphx.linalg.linalg import incidence_matrix
from hypergraphx.linalg.linalg import adjacency_matrix

# Compute the theoretical critical synergy factors of a specific hypergraph for pairwise strategy updates, 
# including death-birth (DB) and pair-comparison (PC).

def CartProb(mAdja, mAdjb):

    """
    compute the Cartesian product of two matrices

    Args:
        mAdja (numpy.array(numpy.float_)): the probability distribution array

    Returns:
        int: the selected element
    """
        
    """
    computes the Cartesian product of two matrices
    :param mAdja: the adjacency matrix of a network
    :param mAdjb: the adjacency matrix of another network
    :return: the Cartesian product of two matrices
    """

    mAdja_csr = csr_matrix(mAdja)
    mAdjb_csr = csr_matrix(mAdjb)

    wa = mAdja_csr.sum(axis=0)
    wb = mAdjb_csr.sum(axis=0)

    nodes1a = triu(mAdja_csr).row
    nodes2a = triu(mAdja_csr).col
    weightsa = triu(mAdja_csr).data

    nodes1b = triu(mAdjb_csr).row
    nodes2b = triu(mAdjb_csr).col
    weightsb = triu(mAdjb_csr).data

    n = wa.shape[1]
    m = wb.shape[1]

    en = len(weightsa)
    em = len(weightsb)

    prodnodes1a = (nodes1a.reshape(en, 1)) @ np.ones((1, m), dtype=int) + np.ones((en, 1), dtype=int) @ (np.arange(0, (m-1)*n+1, n)).reshape((1, m))
    prodnodes2a = (nodes2a.reshape(en, 1)) @ np.ones((1, m), dtype=int) + np.ones((en, 1), dtype=int) @ (np.arange(0, (m-1)*n+1, n)).reshape((1, m))
    cart_data_a = (weightsa.reshape(en, 1)) @ wb

    prodnodes1b = n * (nodes1b.reshape(em, 1)) @ np.ones((1, n), dtype=int) + np.ones((em, 1), dtype=int) @ (np.arange(n)).reshape((1, n))
    prodnodes2b = n * (nodes2b.reshape(em, 1)) @ np.ones((1, n), dtype=int) + np.ones((em, 1), dtype=int) @ (np.arange(n)).reshape((1, n))
    cart_data_b = (weightsb.reshape(em, 1)) @ wa

    prodAdj = coo_matrix((cart_data_a.A.flatten(), (prodnodes1a.flatten(), prodnodes2a.flatten())), shape=(n*m, n*m)) + \
            coo_matrix((cart_data_b.A.flatten(), (prodnodes1b.flatten(), prodnodes2b.flatten())), shape=(n*m, n*m))

    prodAdj_mat = csr_matrix(np.maximum(prodAdj.A, (prodAdj.T).A), shape=(n*m, n*m))

    return prodAdj_mat


def ComputeCoaTime(mAdj):

    """
    computes the coalescence time matrix of a graph
    :param mAdja: the adjacency matrix of a graph
    :return: the coalescence time matrix of a graph
    """
        
    n = mAdj.shape[0]

    C = CartProb(mAdj, mAdj)

    s = C.sum(axis=0)

    C_degree = C.sum(axis=1)
    C_diag = np.diag(C_degree.A.flatten())
    C_Laplacian = C_diag - C           # laplacian matrix of C

    mAdj_degree = mAdj.sum(axis=1)
    mAdj_diag = np.diag(mAdj_degree)
    mAdj_N_Laplacian = np.linalg.inv(mAdj_diag) @ mAdj - np.eye(n)      # nomalized laplacian matrix of mAdj

    diagcoords = list(range(0, n*n, n+1))           # diagonal coordinates

    othercoords = [i for i in range(n*n) if i not in diagcoords]        # non-diagonal coordinates

    other_s = s[0, othercoords]

    other_L = C_Laplacian[np.ix_(othercoords, othercoords)]

    otherdata = np.linalg.inv(other_L) @ other_s.T

    coalescence_time = np.zeros((n, n))

    ii = 0
    for x in range(n):
        for y in range(n):
            if x != y:
                coalescence_time[x][y] = otherdata[ii]
                ii += 1

    return coalescence_time


def calculation_pairwise(hypergraph_data):

    """
    Compute the theoretical critical synergy factors of a specific hypergraph for higher-order strategy updates, 
    including higher-order death-birth (HDB), higher-order imitation (HIM), group-mutual comparison (GMC), group-inner 
    comparison (GIC) and higher-order pair-comparison (PC).
    """

    pairwise_info = {}

    Incidence_mat = incidence_matrix(hypergraph_data).todense()       # incidence matrix

    Hyperdegree_seq = Incidence_mat.sum(axis=1)
    Hyperdegree_mat = np.diag(Hyperdegree_seq)       # hyperdegree matrix

    Payoff_mat = np.linalg.inv(Hyperdegree_mat) @ Incidence_mat @ Incidence_mat.T         # payoff matrix

    Adjacent_mat = adjacency_matrix(hypergraph_data).todense()
    Adjacent_mat = Adjacent_mat.astype(np.int_)              # adjacent matrix

    Degree_proj_seq = Adjacent_mat.sum(axis=1)
    Degree_proj_mat = np.diag(Degree_proj_seq)          # degree matrix of the projected graph

    Pi_proj_mat = (1/(Degree_proj_mat.trace())) * Degree_proj_mat          # stational distribution matrix

    Transition_mat = np.linalg.inv(Degree_proj_mat) @ Adjacent_mat         # trasition probability matrix
    
    Coatime_mat = ComputeCoaTime(Adjacent_mat)       # coalesence time matrix

    ## theoretical value of HDB
    r_db = (np.sum((Pi_proj_mat @ Transition_mat @ Transition_mat) * Coatime_mat)) / (np.sum((Pi_proj_mat @ Transition_mat \
            @ Transition_mat @ Payoff_mat) * Coatime_mat) - np.sum((Pi_proj_mat @ Payoff_mat) * Coatime_mat))
    pairwise_info["r_db"] = round(r_db, 4)

    ## theoretical value of HPC
    r_pc = (np.sum((Pi_proj_mat @ Transition_mat) * Coatime_mat)) / (np.sum((Pi_proj_mat @ Transition_mat @ Payoff_mat) \
            * Coatime_mat) - np.sum((Pi_proj_mat @ Payoff_mat) * Coatime_mat))
    pairwise_info["r_pc"] = round(r_pc, 4)

    return pairwise_info


if __name__ == "__main__":    

    dataset = "congress-bills"          # name of the dataset
    file_hyperedge = open(f'./cleaned_datasets/{dataset}-hyperedges.txt')

    hyperedge = file_hyperedge.readlines()

    hyperedge_lst = []
    for edge in hyperedge:
        edge = edge.strip('\n').split(",")
        hyperedge_lst.append([int(n) for n in edge])

    H = Hypergraph(hyperedge_lst)           # hypergraph construction
    theoretical_solution = calculation_pairwise(H)

    print(theoretical_solution)
