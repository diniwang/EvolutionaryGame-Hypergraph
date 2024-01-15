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

        # Select the hyperedge
        weigh = [W[e] for e in Nei_dict[i]]
        selected_l = random.choices(Nei_dict[i], weigh)[0]

        # Probability of selecting the strategy C
        fitness_C = 0
        fitness_total = 0
        for ii in E[selected_l]:
            fitness_C += Compute_fitness(ii, strategy, b, c) * strategy[ii]
            fitness_total += Compute_fitness(ii, strategy, b, c)
        tran = fitness_C / fitness_total

        # Update the strategy
        rand02 = random.random()
        if rand02 < tran:
            strategy[i] = 1
        else:
            strategy[i] = 0

        # Homogenous state or not
        if sum(strategy) == 0:
            break
        if sum(strategy) == N:
            success += 1
            break

# Succeess rate
Success_rate = success / TestNum
print(Success_rate)