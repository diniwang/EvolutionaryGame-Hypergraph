import random
import networkx as nx

## Setting
NSet = 1000
gSet = 10
kSet = 10
LSeq = int(NSet * kSet / gSet)

alpha = 0.9

VSeq = [i for i in range(NSet)]

p = [i ** (- alpha) for i in range(1, NSet+1)] 

ESeq = []
for l in range(LSeq):
    edge = random.choices([i for i in range(NSet)], weights=p, k=gSet)
    if edge not in ESeq:
        ESeq.append(edge)

VSeq = []
for l in ESeq:
    VSeq += l
VSeq = list(set(VSeq))

Nei_dict = {i : [ESeq.index(e) for e in ESeq if i in e] for i in VSeq}

gList = [len(Nei_dict[i]) for i in VSeq if len(Nei_dict[i]) >1]

LRow = int(len(gList))

VRow = [i for i in range(NSet)]

# Hyperedge list
while(True):

    ERow = []
    total_node = VRow * kSet

    for i in range(LRow):
        ERow.append([])

        while(len(total_node) < gList[i]):
            print(1)
            total_node.append(random.choice(VRow))

        for j in range(gList[i]):
            ERow[i].append(random.choice(total_node))

            # The same hyperedge cannot contain the same vertex.
            while(len(set(ERow[i])) != len(ERow[i])): 
                ERow[i][j] = random.choice(total_node)

        # Remove the selected vertexes.
        for jj in ERow[i]:                                    
            total_node.remove(jj)


    # Each hyperedge cannot be identical.
    for i in range(LRow):
        for j in range(i+1,LRow):
            a = [p for p in ERow[i] if p not in ERow[j]]
            if a == []: 
                break
        if a == []:
            break
    if a == []:
        continue

    break
    
VRow = []
for l in ERow:
    VRow += l
VRow = list(set(VRow))

Nei_vertex = {i: [] for i in VRow}
for i in VRow:
    i_list = []
    for l in ERow:
        if i in l:
            i_list += l
    i_nodup = list(set(i_list))
    i_nodup.remove(i)
    Nei_vertex[i] = i_nodup

## Max-component
# Generate a graph
HG = nx.Graph()

# Add vertexes
HG.add_nodes_from(VRow)

# Add edges
edge = []
for i in VRow:
    edge += list(zip([i] * len(Nei_vertex), Nei_vertex[i]))
HG.add_edges_from(edge)

# Obtain all the connected subgraphs.
components = nx.connected_components(HG)
 
# Obtain the max compoment of the connected subgraphs.
max_component = max(components, key=len)

VCompo = list(max_component)
ECompo = [l for l in ERow if set(l).issubset(set(VCompo))]

## Reorder
V = list(range(len(VCompo)))
N = int(len(V))

E = [[VCompo.index(i) for i in e] for e in ECompo]
L = int(len(E))

# Each vertex and its neighbor hyperedges constitude the dictionary.
Nei_dict = {i: [] for i in V}
for l in range(L):
    for i in E[l]:
        Nei_dict[i].append(l)

## Output the generated hypergraph
print('Vertices: ', V)
print('Hyperedges: ', E)

