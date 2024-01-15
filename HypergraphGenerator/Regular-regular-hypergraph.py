import random

# Setting
N = 100                            # Number of vertexes
gSet = 6                           # Order
kSet = 6                           # Hyperdegree
L = int(N * kSet / gSet)           # Number of hyperedges

# Vertex list
V = [n for n in range(N)]

# Hyperedegree sequence
while(True):

    E = []
    total_node = V * kSet

    for i in range(L):
        E.append([])

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