import numpy as np
from numba import jit


@jit(nopython=True)
def rand_selection(prob_arr):
    
    """
    choose an element according to a given probability distribution, which performs the same as "numpy.random.choice",
    since the function "numpy.random.choice" can not run under numba jit acceleration

    Args:
        prob_arr (numpy.array(numpy.float_)): the probability distribution array

    Returns:
        int: the selected element
    """
    
    prob = np.random.uniform(0, 1)

    cumulative_prob = np.float_(0)
    for idx in range(len(prob_arr)):
        cumulative_prob += prob_arr[idx, 0]
        if prob <= cumulative_prob:
            break

    return idx
