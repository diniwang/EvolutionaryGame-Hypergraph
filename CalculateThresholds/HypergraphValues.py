import numpy as np

# Hypergraph
V = [0,1,2,3,4,5,6,7,8,9]                           # Vertex set
E = [[0,1,2],[1,2,3,4],[4,5],[5,6,7,8],[8,9,4]]     # Hyperedge set
W = [2,1,3,1,0.5]                                   # Hyperedge weights

N = int(len(V))                             # Number of vertices
L = int(len(E))                             # Number of hyperedges

# Incidence matrix
B = np.zeros((N, L), dtype = int) 
for e in range(L):
    for i in E[e]:
        B[i][e] += 1

# Hyperdegree
K = np.array(W) @ B.T
k_1st = np.mean(K)
k_2rd = np.mean(K * K)
print('k_1st = ', k_1st)
print('k_2rd = ', k_2rd)

# Order without self-loops
Gt = B.sum(axis=0) - 1

# Order with self-loops
G = B.sum(axis=0)
g_1st = (np.array(W) @ G.T) / sum(W)
print('g_1st = ', g_1st)

# Trasition probability matrix without self-loops
Pt = np.diag(1 / K) @ B @ np.diag(W) @ np.diag(1 / Gt) @ B.T
for i in range(N):
    Pt[i][i] = 0

# Trasition probability matrix with self-loops
Ph = np.diag(1 / K) @ B @ np.diag(W) @ np.diag(1 / G) @ B.T

# Theoretical value of HDB
r_hdb = (N * k_1st * k_1st / k_2rd - 2) / (N * k_1st * k_1st / k_2rd / g_1st + k_1st / k_2rd * (np.diag(K) @ Pt @ Ph).trace() - 2)
print("r_hdb:", r_hdb)


# Theoretical value of HIM
r_him = (N * k_1st * k_1st / k_2rd + N * k_1st * k_1st / k_2rd / g_1st - 2) / (N * k_1st * k_1st / k_2rd / g_1st + k_1st / k_2rd * (np.diag(K) @ Ph @ Ph).trace() - 2)
print("r_him:", r_him)


# Theoretical value of HPC
r_hpc = (N * k_1st * k_1st / k_2rd - 1) / (N * k_1st * k_1st / k_2rd / g_1st - 1)
print("r_hpc:", r_hpc)


# Theoretical value of GIM
r_gic = (N * k_1st * k_1st / k_2rd - 1) / (N * k_1st * k_1st / k_2rd / g_1st - 1)
print("r_gic:", r_gic)


# Theoretical value of GMC
r_gmc = (N * k_1st * k_1st / k_2rd / g_1st - 1) / (k_1st / k_2rd * (np.diag(K) @ Ph @ Ph).trace() - 1)
print("r_gmc:", r_gmc)