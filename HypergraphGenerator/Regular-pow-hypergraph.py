import numpy as np
import networkx as nx
import random

# Setting
N = 100                        # Number of vertexes
gSet = 6                       # Order
kSet = 6                       # Mean hyperdegree
L = int(N * kSet / gSet)       # Number of hyperedges

# Vertex list
V = [n for n in range(N)]

# Hyperdegree sequence
while(True):

    BA = nx.barabasi_albert_graph(N, int(kSet/2))
    kDict = dict(nx.degree(BA))
    kList = [value for value in kDict.values()]
    kMin = min(kList)

    if kMin == 0:
        continue
    else:
        break
 
# Compute the average hyperdegree
kAvg = np.mean(kList)
print("Average hyperdegree: ", kAvg)

# Order sequence
gList = [gSet] * L

# Hyperedge list
while(True):

    E = []
    total_node = []
    for nn in range(N):
        total_node += [nn] * kList[nn]

    for i in range(L):
        E.append([])

        while(len(total_node) < gSet):
            total_node.append(random.choice(V))

        for j in range(gSet):
            E[i].append(random.choice(total_node))

            # The same hyperedge cannot contain the same vertex.
            while(len(set(E[i])) != len(E[i])): 
                E[i][j] = random.choice(total_node)

        # Remove the selected vertexes.
        for jj in E[i]:                                    
            total_node.remove(jj)

    # Each hyperedge cannot be identical.
    for i in range(L):
        for j in range(i+1,L):
            a = [p for p in E[i] if p not in E[j]]
            if a == []: 
                break
        if a == []:
            break
    if a == []:
        continue

    break

# Each vertex and its neighbor hyperedges constitude the dictionary.
Nei_dict = {i: [] for i in V}
for l in range(L):
    for i in E[l]:
        Nei_dict[i].append(l)


# Output the generated hypergraph.
print(V)
print(E)