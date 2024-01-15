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

# Each vertex and its neighbor hyperedges constitude the dictionary.
Nei_dict = {i: [] for i in V}
for l in range(L):
    for i in E[l]:
        Nei_dict[i].append(l)

# Incidence matrix : B
B = np.zeros((N, L), dtype = int) 
for e in range(L):
    for i in E[e]:
        B[i][e] = 1

# Transposition of incidence matrix : B^{T}
B_T = B.T

# Hyperdegree matrix : K
K = B.sum(axis=1)
K = np.diag(K)

# Stational distribution : Pi
Pi = (1/(K.trace()))* K

# Order matrix without self-loops: \widetilde{G}
Gt = B.sum(axis=0) - 1
Gt = np.diag(Gt)

# Order matrix with self-loops: G
G = B.sum(axis=0)
G = np.diag(G)

# Adjacent matrix without self-loops
At = B @ np.linalg.inv(Gt) @ B_T
for i in range(N):
    At[i][i] = 0

# Adjacent matrix with self-loops
Ah = B @ np.linalg.inv(G) @ B_T

# Trasition probability matrix without self-loops : \widetilde{P}
Pt = np.mat(np.linalg.inv(K) @ At)

# Trasition probability matrix with self-loops : \widehat{P}
Ph = np.mat(np.linalg.inv(K) @ Ah)

Xt = 1/N * Pt + (1 - 1/N) * np.eye(N)

Xh = 1/N * Ph + (1 - 1/N) * np.eye(N)

tList = [i for i in range(1,10 * N)]
errorList = []

for t in tList:

    a = np.trace(Pi @ np.linalg.matrix_power(Xt, t) @ Pt @ Pt @ Ph @ np.linalg.matrix_power(Xt, t))
    b = np.trace(Pi @ np.linalg.matrix_power(Xt, 2*t) @ Pt @ Pt @ Ph)
    
    error = abs((a - b)/b)
    errorList.append(error)

plt.plot(tList, [math.log(i, 10) for i in errorList], label = r'$\left\langle{g}\right\rangle = 6$, $\left\langle{k}\right\rangle = 6$')

plt.legend(fontsize=16)

pylab.xlim(0,500)

plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

plt.xlabel("time",fontsize=18)
plt.ylabel(r"log$(\sigma^{(2,1)}) $",fontsize=18)

plt.savefig('sigma-2-1.jpg',bbox_inches = 'tight',dpi=2000)