import numpy as np
from numba import jit


@jit(nopython=True)
def individual_fitness(incidence_mat, strategy_arr, delta_para, r_factor):

    """
    Compute the fitness of all the individuals

    Args:
        incidence_mat (numpy.array(numpy.float_)): the incidence matrix of the given hypergraph
        strategy_arr (numpy.array(numpy.float_)): the individual strategy array
        selection_stren (numpy.float_): the strength of selection
        pgg_factor (numpy.float_): the synergy factor of the public goods game

    Returns:
        numpy.array(numpy.float_): the individual fitness array
    """

    hyperdegree_seq = incidence_mat.sum(axis=1)
    hyperdegree_inv = 1 / hyperdegree_seq
    hyperdegree_invmat = np.diag(hyperdegree_inv)

    individual_payoff_arr = r_factor * hyperdegree_invmat @ incidence_mat @ \
        incidence_mat.T @ strategy_arr - strategy_arr       # individual payoffs

    individual_fitness_arr = np.ones((incidence_mat.shape[0], 1), dtype=np.float_) + \
        delta_para * individual_payoff_arr         # individual fitnesses

    return individual_fitness_arr


@jit(nopython=True)
def group_fitness(incidence_mat, strategy_arr, delta_para, r_factor):

    """
    Compute the fitness of all the groups

    Args:
        incidence_mat (numpy.array(numpy.float_)): the incidence matrix of the given hypergraph
        strategy_arr (numpy.array(numpy.float_)): the individual strategy array
        selection_stren (numpy.float_): the strength of selection
        pgg_factor (numpy.float_): the synergy factor of the public goods game

    Returns:
        numpy.array(numpy.float_): the group fitness array
    """

    order_seq = incidence_mat.sum(axis=0)
    order_inv = 1 / order_seq
    order_invmat = np.diag(order_inv)

    group_fitness_arr = order_invmat @ incidence_mat.T @ \
          individual_fitness(incidence_mat, strategy_arr, delta_para, r_factor)

    return group_fitness_arr


@jit(nopython=True)
def group_exc_fitness(incidence_mat, strategy_arr, delta_para, r_factor, node_exc_idx):

    """
    Compute the fitness of all the groups excluding the given node

    Args:
        incidence_mat (numpy.array(numpy.float_)): the incidence matrix of the given hypergraph
        strategy_arr (numpy.array(numpy.float_)): the individual strategy array
        selection_stren (numpy.float_): the strength of selection
        pgg_factor (numpy.float_): the synergy factor of the public goods game
        node_exc_idx (numpy.int_): the index of the node that is excluded in the group fitness computation
        
    Returns:
        numpy.array(numpy.float_): the group fitness array with the certain node excluded
    """

    incidence_exc_mat = incidence_mat.copy()
    incidence_exc_mat[node_exc_idx, :] = 0           # incidence matrix excluding the given node

    order_exc_seq = incidence_exc_mat.sum(axis=0)
    order_exc_inv = 1 / order_exc_seq
    order_exc_invmat = np.diag(order_exc_inv)          # order matrix excluding the given node

    group_exc_fitness_array = order_exc_invmat @ incidence_exc_mat.T @ \
        individual_fitness(incidence_mat, strategy_arr, delta_para, r_factor)

    return group_exc_fitness_array
