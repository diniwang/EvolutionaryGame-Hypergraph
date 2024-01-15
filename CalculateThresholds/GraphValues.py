import numpy as np

# Hypergraph
V = [0,1,2,3,4,5,6,7,8,9]                           # Vertex set
E = [[0,1,2],[1,2,3,4],[4,5],[5,6,7,8],[8,9,4]]     # Hyperedge set

N = int(len(V))                             # Number of vertices
L = int(len(E))                             # Number of hyperedges

# Neighboring vertices
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

# Adjacent matrix without self-loops
GAt = np.zeros((N, N), dtype = int) 
for i in V:
    for j in Nei_vertex[i]:
        GAt[i][j] = 1

# Adjacent matrix with self-loops
GAh = np.zeros((N, N), dtype = int) 
for i in V:
    for j in Nei_vertex_1[i]:
        GAh[i][j] = 1

# Degree matrix without self-loops
GKt = GAt.sum(axis=1)
GKt = np.diag(GKt)

# Degree matrix with self-loops
GKh = GAh.sum(axis=1)
GKh = np.diag(GKh)

# Stational distribution without self-loops
GPit = (1/(GKt.trace())) * GKt

# Stational distribution with self-loops
GPih = (1/(GKh.trace())) * GKh

# Trasition probability matrix without self-loops
GPt = np.linalg.inv(GKt) @ GAt

# Trasition probability matrix with self-loops 
GPh = np.linalg.inv(GKh) @ GAh


# Theoretical value of DB
rG_db = ((GPit @ (np.eye(N) + GPt)).trace() - 2 * (GPit @ GPit).trace()) / ((GPit @ (GPh @ GPh + GPt @ GPh @ GPh)).trace() - 2 * (GPit @ GPh @ GPh @ GPit).sum())
print("rG_db = ", rG_db)

# Theoretical value of IM
rG_im = ((GPih @ (np.eye(N) + GPh)).trace() - 2 * (GPih @ GPih).trace()) / ((GPih @ (GPh @ GPh + GPh @ GPh @ GPh)).trace() - 2 * (GPih @ GPih).trace())
print("rG_im = ", rG_im)

# Theoretical value of PC
rG_pc = ((GPit @ np.eye(N)).trace() - (GPit @ GPit).trace()) / ((GPit @ GPh @ GPh).trace() - (GPit @ GPh @ GPh @ GPit).sum())
print("rG_pc = ", rG_pc)