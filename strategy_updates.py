import numpy as np
from numba import jit
from selection_algorithm import rand_selection
from game_fitnesses import individual_fitness, group_fitness, group_exc_fitness


@jit(nopython=True)
def hdb_update(incidence_mat, strategy_arr, delta_para, r_factor):

    """
    Update the strategy acoording to the HDB update mechanism

    Args:
        incidence_mat(numpy.array(numpy.float_)): the incidence matrix of the given hypergraph
        strategy_arr(numpy.array(numpy.float_)): the individual strategy array
        selection_stren(numpy.float_): the strength of selection
        pgg_factor(numpy.float_): the synergy factor of the public goods game

    Returns:
        numpy.array(numpy.float_): the updated individual strategy array
    """

    nodesnum = incidence_mat.shape[0]           # number of nodes
    edgesnum = incidence_mat.shape[1]           # number of hyperedges

    update_node_idx = np.random.randint(nodesnum)        # selection of a to-be-updated node

    nbr_group_arr = incidence_mat[update_node_idx, :]
    nbr_group_exc_fit = nbr_group_arr.reshape(edgesnum, 1) * \
        group_exc_fitness(incidence_mat, strategy_arr, delta_para, r_factor, update_node_idx)
    nbr_group_prob = nbr_group_exc_fit / np.sum(nbr_group_exc_fit)        # probabilities of selecting each neighboring group

    selected_group_idx = rand_selection(nbr_group_prob)           # selection of a neighboring group

    nbr_node_arr = incidence_mat[:, selected_group_idx]
    nbr_node_exc_arr = nbr_node_arr.copy()
    nbr_node_exc_arr[update_node_idx] = np.float_(0)
    nbr_node_exc_fit = nbr_node_exc_arr.reshape(nodesnum, 1) * \
        individual_fitness(incidence_mat, strategy_arr, delta_para, r_factor)
    nbr_node_prob = nbr_node_exc_fit / np.sum(nbr_node_exc_fit)         # probabilities of selecting each neighbor

    selected_node_idx = rand_selection(nbr_node_prob)           # selection of a neighbor

    strategy_arr[update_node_idx, 0] = strategy_arr[selected_node_idx, 0]         # realization of an HDB strategy update
    
    return strategy_arr


@jit(nopython=True)
def him_update(incidence_mat, strategy_arr, delta_para, r_factor):

    """
    Update the strategy acoording to the HDB update mechanism

    Args:
        incidence_mat(numpy.array(numpy.float_)): the incidence matrix of the given hypergraph
        strategy_arr(numpy.array(numpy.float_)): the individual strategy array
        selection_stren(numpy.float_): the strength of selection
        pgg_factor(numpy.float_): the synergy factor of the public goods game

    Returns:
        numpy.array(numpy.float_): the updated individual strategy array
    """

    nodesnum = incidence_mat.shape[0]           # number of nodes
    edgesnum = incidence_mat.shape[1]           # number of hyperedges

    update_node_idx = np.random.randint(nodesnum)        # selection of a to-be-updated node

    nbr_group_arr = incidence_mat[update_node_idx, :]
    nbr_group_fit = nbr_group_arr.reshape(edgesnum, 1) * \
        group_fitness(incidence_mat, strategy_arr, delta_para, r_factor)
    nbr_group_prob = nbr_group_fit / np.sum(nbr_group_fit)        # probabilities of selecting each neighboring group

    selected_group_idx = rand_selection(nbr_group_prob)           # selection of a neighboring group

    nbr_node_orgarr = incidence_mat[:, selected_group_idx]
    nbr_node_arr = nbr_node_orgarr.copy()
    nbr_node_fit = nbr_node_arr.reshape(nodesnum, 1) * \
        individual_fitness(incidence_mat, strategy_arr, delta_para, r_factor)
    nbr_node_prob = nbr_node_fit / np.sum(nbr_node_fit)         # probabilities of selecting each neighbor (including oneself)

    selected_node_idx = rand_selection(nbr_node_prob)           # selection of a neighbor (including oneself)

    strategy_arr[update_node_idx, 0] = strategy_arr[selected_node_idx, 0]         # realization of an HIM strategy update
    
    return strategy_arr


@jit(nopython=True)
def gmc_update(incidence_mat, strategy_arr, delta_para, r_factor):

    """
    Update the strategy acoording to the GMC update mechanism

    Args:
        incidence_mat(numpy.array(numpy.float_)): the incidence matrix of the given hypergraph
        strategy_arr(numpy.array(numpy.float_)): the individual strategy array
        selection_stren(numpy.float_): the strength of selection
        pgg_factor(numpy.float_): the synergy factor of the public goods game

    Returns:
        numpy.array(numpy.float_): the updated individual strategy array
    """

    nodesnum = incidence_mat.shape[0]           # number of nodes
    edgesnum = incidence_mat.shape[1]           # number of hyperedges

    update_node_idx = np.random.randint(nodesnum)        # selection of a to-be-updated node

    nbr_group_arr = incidence_mat[update_node_idx, :]
    nbr_group_fit = nbr_group_arr.reshape(edgesnum, 1) * \
        group_fitness(incidence_mat, strategy_arr, delta_para, r_factor)
    nbr_group_prob = nbr_group_fit / np.sum(nbr_group_fit)        # probabilities of selecting each neighboring group

    selected_group_idx = rand_selection(nbr_group_prob)           # selection of a neighboring group

    nbr_node_arr = incidence_mat[:, selected_group_idx]
    nbr_node_exc_arr = nbr_node_arr.copy()
    nbr_node_exc_arr[update_node_idx] = np.float_(0)
    nbr_node_prob = nbr_node_exc_arr.reshape(nodesnum, 1) / np.sum(nbr_node_exc_arr)         # probabilities of selecting each neighbor

    selected_node_idx = rand_selection(nbr_node_prob)           # selection of a neighbor

    strategy_arr[update_node_idx, 0] = strategy_arr[selected_node_idx, 0]           # realization of a GMC strategy update
    
    return strategy_arr


@jit(nopython=True)
def gic_update(incidence_mat, strategy_arr, delta_para, r_factor):

    """
    Update the strategy acoording to the GIC update mechanism

    Args:
        incidence_mat(numpy.array(numpy.float_)): the incidence matrix of the given hypergraph
        strategy_arr(numpy.array(numpy.float_)): the individual strategy array
        selection_stren(numpy.float_): the strength of selection
        pgg_factor(numpy.float_): the synergy factor of the public goods game

    Returns:
        numpy.array(numpy.float_): the updated individual strategy array
    """

    nodesnum = incidence_mat.shape[0]           # number of nodes
    edgesnum = incidence_mat.shape[1]           # number of hyperedges

    update_node_idx = np.random.randint(nodesnum)        # selection of a to-be-updated node

    nbr_group_arr = incidence_mat[update_node_idx, :]
    nbr_group_prob = nbr_group_arr.reshape(edgesnum, 1) / np.sum(nbr_group_arr)        # probabilities of selecting each neighboring group

    selected_group_idx = rand_selection(nbr_group_prob)           # selection of a neighboring group

    nbr_node_orgarr = incidence_mat[:, selected_group_idx]
    nbr_node_arr = nbr_node_orgarr.copy()
    nbr_node_fit = nbr_node_arr.reshape(nodesnum, 1) * \
        individual_fitness(incidence_mat, strategy_arr, delta_para, r_factor)
    nbr_node_prob = nbr_node_fit / np.sum(nbr_node_fit)         # probabilities of selecting each neighbor (including oneself)

    selected_node_idx = rand_selection(nbr_node_prob)           # selection of a neighbor (including oneself)

    strategy_arr[update_node_idx, 0] = strategy_arr[selected_node_idx, 0]           # realization of a GIC strategy update
    
    return strategy_arr


@jit(nopython=True)
def hpc_update(incidence_mat, strategy_arr, delta_para, r_factor):

    """
    Update the strategy acoording to the HPC update mechanism

    Args:
        incidence_mat(numpy.array(numpy.float_)): the incidence matrix of the given hypergraph
        strategy_arr(numpy.array(numpy.float_)): the individual strategy array
        selection_stren(numpy.float_): the strength of selection
        pgg_factor(numpy.float_): the synergy factor of the public goods game

    Returns:
        numpy.array(numpy.float_): the updated individual strategy array
    """

    nodesnum = incidence_mat.shape[0]
    edgesnum = incidence_mat.shape[1]

    update_node_idx = np.random.randint(nodesnum)        # selection of a to-be-updated node

    nbr_group_arr = incidence_mat[update_node_idx, :]
    nbr_group_prob = nbr_group_arr.reshape(edgesnum, 1) / np.sum(nbr_group_arr)        # probabilities of selecting each neighboring group

    selected_group_idx = rand_selection(nbr_group_prob)           # selection of a neighboring group

    nbr_node_arr = incidence_mat[:, selected_group_idx]
    nbr_node_exc_arr = nbr_node_arr.copy()
    nbr_node_exc_arr[update_node_idx] = np.float_(0)
    nbr_node_prob = nbr_node_exc_arr.reshape(nodesnum, 1) / np.sum(nbr_node_exc_arr)         # probabilities of selecting each neighbor for comparison

    selected_node_idx = rand_selection(nbr_node_prob)           # selection of a role model

    selected_node_arr = np.zeros((nodesnum, 1), dtype=np.float_)
    selected_node_arr[update_node_idx, 0] = 1
    selected_node_arr[selected_node_idx, 0] = 1
    selected_node_fit = selected_node_arr * individual_fitness(incidence_mat, strategy_arr, delta_para, r_factor)
    selected_node_prob = selected_node_fit / np.sum(selected_node_fit)

    final_selected_node_idx = rand_selection(selected_node_prob)       # change or maintain

    strategy_arr[update_node_idx, 0] = strategy_arr[final_selected_node_idx, 0]           # realization of an HPC strategy update
    
    return strategy_arr


@jit(nopython=True)
def db_update(incidence_mat, strategy_arr, delta_para, r_factor):

    """
    Update the strategy acoording to the DB update mechanism

    Args:
        incidence_mat(numpy.array(numpy.float_)): the incidence matrix of the given hypergraph
        strategy_arr(numpy.array(numpy.float_)): the individual strategy array
        selection_stren(numpy.float_): the strength of selection
        pgg_factor(numpy.float_): the synergy factor of the public goods game

    Returns:
        numpy.array(numpy.float_): the updated individual strategy array
    """

    nodesnum = incidence_mat.shape[0]

    adjacency_mat = incidence_mat @ incidence_mat.T
    for i in range(adjacency_mat.shape[0]):
        for j in range(adjacency_mat.shape[1]):
            if adjacency_mat[i, j] != 0:
                adjacency_mat[i, j] = np.float_(1)

    update_node_idx = np.random.randint(nodesnum)        # selection of a to-be-updated node

    nbr_node_arr = adjacency_mat[update_node_idx, :]
    nbr_node_fit = nbr_node_arr.reshape(nodesnum, 1) * \
        individual_fitness(incidence_mat, strategy_arr, delta_para, r_factor)        
    nbr_node_prob = nbr_node_fit / np.sum(nbr_node_fit)     # probabilities of selecting each neighbor

    selected_node_idx = rand_selection(nbr_node_prob)           # selection of a neighbor

    strategy_arr[update_node_idx, 0] = strategy_arr[selected_node_idx, 0]           # realization of a PC strategy update
    
    return strategy_arr


@jit(nopython=True)
def pc_update(incidence_mat, strategy_arr, delta_para, r_factor):

    """
    Update the strategy acoording to the PC update mechanism

    Args:
        incidence_mat(numpy.array(numpy.float_)): the incidence matrix of the given hypergraph
        strategy_arr(numpy.array(numpy.float_)): the individual strategy array
        selection_stren(numpy.float_): the strength of selection
        pgg_factor(numpy.float_): the synergy factor of the public goods game

    Returns:
        numpy.array(numpy.float_): the updated individual strategy array
    """

    nodesnum = incidence_mat.shape[0]

    adjacency_mat = incidence_mat @ incidence_mat.T
    for i in range(adjacency_mat.shape[0]):
        for j in range(adjacency_mat.shape[1]):
            if adjacency_mat[i, j] != 0:
                adjacency_mat[i, j] = np.float_(1)

    update_node_idx = np.random.randint(nodesnum)        # selection of a to-be-updated node

    nbr_node_arr = adjacency_mat[update_node_idx, :]
    nbr_node_prob = nbr_node_arr.reshape(nodesnum, 1) / np.sum(nbr_node_arr)        # probabilities of selecting each neighbor for comparison

    selected_node_idx = rand_selection(nbr_node_prob)           # selection of a role model

    selected_node_arr = np.zeros((nodesnum, 1), dtype=np.float_)
    selected_node_arr[update_node_idx, 0] = 1
    selected_node_arr[selected_node_idx, 0] = 1
    selected_node_fit = selected_node_arr * individual_fitness(incidence_mat, strategy_arr, delta_para, r_factor)
    selected_node_prob = selected_node_fit / np.sum(selected_node_fit)

    final_selected_node_idx = rand_selection(selected_node_prob)       # change or maintain

    strategy_arr[update_node_idx, 0] = strategy_arr[final_selected_node_idx, 0]           # realization of a PC strategy update
    
    return strategy_arr
