import numpy as np
from numba import jit
import multiprocessing
import functools
import time
from hypergraphx import Hypergraph
from hypergraphx.linalg.linalg import incidence_matrix
from strategy_updates import hdb_update, him_update, gmc_update, gic_update, hpc_update, db_update, pc_update


# Perform Monto Carlo simulations of evolutionary dynamics on a given hypergraph driven by higher-order death birth (HDB), 
# higher-order imitation (HIM), group-mutual-comparison (GMC), group-inner-comparison (GIC) and higher-order pair-comparison 
# (HPC) updates, from the initial configuration of a random mutant to the fixtion state of all cooperators or all defectors. 
# Among these, the probability of all-cooperator occupying the population, known as fixation probability of cooperators, 
# is what we concern about.


@jit(nopython=True)
def evolution(incidence_mat, delta_para, r_factor, round_num, protocol):

    """
    simulate a complete evolutionary process which starts from a single cooperator and ends as absoption 
    state of either all-cooperators or all-defectors

    Args:
        incidence_mat(numpy.array(numpy.float_)): the incidence matrix of the given hypergraph
        delta_para(numpy.float_): the strength of selection
        r_factor(numpy.float_): the synergy factor of the public goods game
        round_num(numpy.int_): the number of the evolution rounds

    Returns:
        numpy.int_: all cooperators (return 1) or all defectors (return 0)
    """

    nodesnum = incidence_mat.shape[0]           # number of nodes

    strategy_arr = np.zeros((nodesnum, 1), dtype=np.float_)
    cooperator_idx = np.random.randint(nodesnum)
    strategy_arr[cooperator_idx][0] = np.float_(1)

    for round in range(round_num):
        if protocol == 0:
            strategy_arr = hdb_update(incidence_mat, strategy_arr, delta_para, r_factor)
        elif protocol == 1:
            strategy_arr = him_update(incidence_mat, strategy_arr, delta_para, r_factor)
        elif protocol == 2:
            strategy_arr = gmc_update(incidence_mat, strategy_arr, delta_para, r_factor)
        elif protocol == 3:
            strategy_arr = gic_update(incidence_mat, strategy_arr, delta_para, r_factor)
        elif protocol == 4:
            strategy_arr = hpc_update(incidence_mat, strategy_arr, delta_para, r_factor)
        elif protocol == 5:
            strategy_arr = db_update(incidence_mat, strategy_arr, delta_para, r_factor)
        elif protocol == 6:
            strategy_arr = pc_update(incidence_mat, strategy_arr, delta_para, r_factor)
        else:
            print("Invalid input")

        cooperator_num = np.sum(strategy_arr)
        if cooperator_num == 0:
            return np.int_(0)
        if cooperator_num == nodesnum:
            return np.int_(1)

    return cooperator_num / nodesnum


@jit(nopython=True)
def fixation_prob(core, incidence_mat, delta_para, r_factor, round_num, test_num, protocol):

    """
    repeat the evolutionary processes to compute the fixation probability of cooperation, that
    is the population reaches the full cooperation state

    Args:
        incidence_mat(numpy.array(numpy.float_)): the incidence matrix of the given hypergraph
        selection_stren(numpy.float_): the strength of selection
        pgg_factor(numpy.float_): the synergy factor of the public goods game
        round_num(numpy.int_): the number of the evolution rounds
        test_num(numpy.int_): the number of the parallel tests

    Returns:
        float_: the fixation probability of cooperation
    """

    test_arr = np.zeros(test_num, dtype=np.int_)

    for test in range(test_num):
        freq_c = evolution(incidence_mat, delta_para, r_factor, round_num, protocol)
        test_arr[test] = freq_c
    
    return np.sum(test_arr == 1) / (np.sum(test_arr == 1) + np.sum(test_arr == 0))


if __name__ == "__main__":

    dataset = "congress-bills"            # tested dataset
    test_num = np.int_(1e4)              # number of parallel tests
    round_num = np.int_(1e6)             # rounds of evolution
    delta_para = np.float_(0.025)              # selection strength
    r_factor = np.float_(2.2485)                      # synergy factor of PGG
    protocol = 6                     # hdb, him, gmc, gic, hpc, db and pc correspond to 0, 1, 2, 3, 4, 5 and 6, respectively
    cpu_cores_num = 8                     # number of cpu-core which is used to run this programme

    file_hyperedge = open(f'./cleaned_datasets/{dataset}-hyperedges.txt')
    hyperedge = file_hyperedge.readlines()
    hyperedge_lst = []
    for i in hyperedge:
        i = i.strip('\n').split(",")
        hyperedge_lst.append([int(t) for t in i])

    H = Hypergraph(hyperedge_lst)           # hypergraph construction

    incidence_mat = incidence_matrix(H).todense()       # incidence matrix
    incidence_mat = incidence_mat.astype(np.float_)

    core_lst = np.arange(cpu_cores_num)

    pool = multiprocessing.Pool()
    t1 = time.time()

    pt = functools.partial(fixation_prob, incidence_mat=incidence_mat, delta_para=delta_para, 
                           r_factor=r_factor, round_num=round_num, test_num=test_num, protocol=protocol)
    
    rho_c_list = pool.map(pt, core_lst)

    rho_c = np.mean(rho_c_list)

    pool.close()
    pool.join()

    t2 = time.time()

    print("r="+str(r_factor)+",", "rho_c="+str(rho_c))
    print("total time:" + (t2 - t1).__str__())
