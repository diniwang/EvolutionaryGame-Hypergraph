import numpy as np
import random
import matplotlib.pyplot as plt
import networkx as nx
import math
import pylab

# Hypergraph
N = 50                      # Number of vertices
g = 6                       # Mean order
k = 6                       # Mean hyperdegree
L = int(N * k / g)          # Number of hyperedges

# Vertex list 
V = [n for n in range(N)]

# Hyperdegree sequence
while(True):
    
    BA = nx.barabasi_albert_graph(L, int(g/2))
    d = dict(nx.degree(BA))
    for i in range(L):
        if d[i] == 1:
            break
    if d[i] == 1:
        continue

    break

# Hyperedge list
while(True):

    E = []
    total_node = V * k

    for i in range(L):
        E.append([])

        for j in range(d[i]):
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
            b = [p for p in E[j] if p not in E[i]]
            if a == [] and b == []: 
                break
        if a == [] and b == []:
            break
    if a == [] and b == []:
        continue

    break

Nei_vertex = {i: [] for i in V}
Nei_vertex_1 = {i: [] for i in V}
for i in V:
    i_list = []
    for l in E:
        if i in l:
            i_list += l
        else:
            pass
    i_list = list(set(i_list))
    Nei_vertex_1[i] = i_list
    Nei_vertex[i] = [j for j in i_list if j != i]

At = np.zeros((N, N), dtype = int) 
for i in V:
    for j in Nei_vertex[i]:
        At[i][j] = 1

Ah = np.zeros((N, N), dtype = int) 
for i in V:
    for j in Nei_vertex_1[i]:
        Ah[i][j] = 1

Kt = At.sum(axis=1)
Kt = np.diag(Kt)

Kh = Ah.sum(axis=1)
Kh = np.diag(Kh)

Pit = (1/(Kt.trace())) * Kt

Pih = (1/(Kh.trace())) * Kh

Pt = np.linalg.inv(Kt) @ At

Ph = np.linalg.inv(Kh) @ Ah

Xt = 1/N * Pt + (1 - 1/N) * np.eye(N)

Xh = 1/N * Ph + (1 - 1/N) * np.eye(N)

tList = [i for i in range(1, 10 * N)]
errorList = []

for t in tList:

    a = np.trace(Pit @ np.linalg.matrix_power(Xt, t) @ Pt @ Pt @ Ph @ Ph @ np.linalg.matrix_power(Xt, t))
    b = np.trace(Pit @ np.linalg.matrix_power(Xt, 2*t) @ Pt @ Pt @ Ph @ Ph)
    
    error = abs((a - b)/b)
    errorList.append(error)

plt.plot(tList, [math.log(i, 10) for i in errorList], label = r'$\left\langle{g}\right\rangle = 10$, $\left\langle{k}\right\rangle = 10$')

plt.legend(fontsize=16)

pylab.xlim(0,500)

plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

plt.xlabel("time",fontsize=18)
plt.ylabel(r"log$(\sigma^{(2,2)}_G) $",fontsize=18)

plt.savefig('sigma_G-2-2.jpg',bbox_inches = 'tight',dpi=2000)