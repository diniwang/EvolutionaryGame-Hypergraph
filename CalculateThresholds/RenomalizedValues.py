import numpy as np

# Hypergraph
V = [0,1,2,3,4,5,6,7,8,9]                           # Vertex set
E = [[0,1,2],[1,2,3,4],[4,5],[5,6,7,8],[8,9,4]]     # Hyperedge set

N = int(len(V))                             # Number of vertices
L = int(len(E))                             # Number of hyperedges

# Incidence matrix : B
B = np.zeros((N, L), dtype = int) 
for e in range(L):
    for i in E[e]:
        B[i][e] = 1

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
At = B @ np.linalg.inv(Gt) @ B.T
for i in range(N):
    At[i][i] = 0

# Adjacent matrix with self-loops
Ah = B @ np.linalg.inv(G) @ B.T

# Trasition probability matrix without self-loops : \widetilde{P}
Pt = np.linalg.inv(K) @ At

# Trasition probability matrix with self-loops : \widehat{P}
Ph = np.linalg.inv(K) @ Ah

Pg = np.linalg.inv(K) @ B @ B.T


# Theoretical value of HDB
R_hdb = ((Pi @ (np.eye(N) + Pt)).trace() - 2 * (Pi @ Pi).trace()) / ((Pi @ (Pg + Pt @ Pg)).trace() - 2 * (Pi @ Pg @ Pi).sum())
print("R_hdb:", R_hdb)

# Theoretical value of HIM
R_him = ((Pi @ (np.eye(N) + Ph)).trace() - 2 * (Pi @ Pi).trace()) / ((Pi @ (Pg + Ph @ Pg)).trace() - 2 * (Pi @ Pg @ Pi).sum())
print("R_him:", R_him)

# Theoretical value of HPC
R_hpc = ((Pi @ np.eye(N)).trace() - (Pi @ Pi).trace()) / ((Pi @ Pg).trace() - (Pi @ Pg @ Pi).sum())
print("R_hpc:", R_hpc)

# Theoretical value of GIC
R_gic = ((Pi @ np.eye(N)).trace() - (Pi @ Pi).trace()) / ((Pi @ Pg).trace() - (Pi @ Pg @ Pi).sum())
print("R_gic:", R_gic)

# Theoretical value of GMC
R_gmc = ((Pi @ Ph).trace() - (Pi @ Pi).trace()) / ((Pi @ Ph @ Pg).trace() - (Pi @ Pg @ Pi).sum())
print("R_gmc:", R_gmc)