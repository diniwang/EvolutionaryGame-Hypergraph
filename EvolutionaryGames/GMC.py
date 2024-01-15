import numpy as np
import random

# Selection strength
delta = 0.025

# Test & interaction
TestNum = 50000               # Number of tests
ContectNum = 1000000          # Number of interactions

# Game parameters
r = 3.0000                    # Enhancement factor
c = 1                         # Cost
b = r * c                     # Benefit

# Hypergraph
V = [0,1,2,3,4,5,6,7,8,9]                           # Vertex set
E = [[0,1,2],[1,2,3,4],[4,5],[5,6,7,8],[8,9,4]]     # Hyperedge set
W = [2,1,3,1,0.5]                                   # Hyperedge weights

N = int(len(V))                             # Number of vertices
L = int(len(E))                             # Number of hyperedges

Nei_dict = {i : [E.index(e) for e in E if i in e] for i in V}   # Neighboring hyperedges


# Compute a fitness
def Compute_fitness(position, stra_list, benefit, cost):

    """
    Compute the given vertex's fitness

    Args:
        position (int): the given vertex
        stra_list (list): strategy list
        benefit (float): benefit of PGG
        cost (float): cost of PGG

    Returns:
       float: the given vertex's fitness
    """

    # The given vertex's fitness in each hyperedge constitude the list.
    payoff = []
    payoff_wei = 0

    for e in Nei_dict[position]:   

        # Compute the given vertex's fitness in one hyperedge.
        edge_payoff = 0  
        for j in E[e]:
            edge_payoff += stra_list[j] * benefit
        edge_payoff = edge_payoff / len(E[e]) - stra_list[position] * cost
        payoff.append(edge_payoff * W[e])
        payoff_wei += W[e]

    # Compute the mean fitness.     
    fitness = 1 + delta * sum(payoff) / payoff_wei

    return fitness



# Number of successes that all of the vertexes reach the strategy C.
success = 0

# Repeat parallel tests
for t in range(TestNum):

    # Initialize the strategy list -- select at random with uniform probability a vertex as strategy C.
    strategy = [0] * N
    strategy[random.choice(V)] = 1

    # Cyclic interaction
    for con in range(ContectNum):

        # Asynchronous update
        i = random.choice(V)
            
        # The mean fitness of each hyperedge containing the selected vertex constitudes the list.
        fit_edge_lst = []
        for e in Nei_dict[i]:
            fit_edge = np.mean([Compute_fitness(ii, strategy, b, c) for ii in E[e]] )
            fit_edge_lst.append(fit_edge * W[e])
        fit_sum = sum(fit_edge_lst)

        # Probability of selecting each hyperedge
        fit_prob = [f/fit_sum for f in fit_edge_lst]
        for ii in range(1, len(fit_prob)):
            fit_prob[ii] += fit_prob[ii-1]

        # Select the hyperedge
        rand01 = random.random()
        for ii in range(len(fit_prob)):
            if rand01 < fit_prob[ii]:
                selected_l = Nei_dict[i][ii]
                fit_total = fit_edge_lst[ii] * len(E[selected_l]) / W[selected_l]
                break
            
        # Select the vertex
        possible_v = [x for x in E[selected_l] if x != i]
        selected_v = random.choice(possible_v)

        # Update the strategy
        strategy[i] = strategy[selected_v]
        
        # Homogenous state or not
        if sum(strategy) == 0:
            break
        if sum(strategy) == N:
            success += 1
            break

# Succeess rate
Success_rate = success / TestNum
print(Success_rate)