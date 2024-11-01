from hypergraphx import Hypergraph
from hypergraphx.utils.cc import largest_component

# Process the raw higher-order network datasets and extract the higher-order 
# sub-networks or partial higher-order networks.


def mapping_hypergraph(hypergraph):

    """
    Map the nodes of the hypergraph to integers in [0, n_nodes), and adjust the hyperedges accordingly.
    
    Parameters
    ----------
    H : Hypergraph
        The input hypergraph with arbitrary node labels.
    
    Returns
    -------
    Hypergraph
        A new hypergraph with nodes relabeled from 0 to N-1.
    """
    
    new_lable_map = hypergraph.get_mapping()
    new_edge_lst = [tuple(new_lable_map.transform(edge)) for edge in hypergraph.get_edges()]

    return Hypergraph(new_edge_lst)


def from_data_to_hyperedge(dataset_name):

    ## Read the node data.
    file_node = open(f"./raw_datasets/{dataset_name}/{dataset_name}-nverts.txt", "r")
    node = file_node.readlines()
    node = [int(i.strip('\n')) for i in node]

    ## Read the hyperedge data.
    file_hyperedge = open(f"./raw_datasets/{dataset_name}/{dataset_name}-simplices.txt", "r")
    hyperedge = file_hyperedge.readlines()
    hyperedge = [int(i.strip('\n')) for i in hyperedge]

    ## Obtain the raw hyperedge list.
    hyperedge_lst = []
    j = 0
    for i in node:
        j += i
        hyperedge_lst.append(hyperedge[j : j + i])

    hyperedge_lst = [tuple(set(l)) for l in hyperedge_lst if len(set(l)) >= 2]
    hyperedge_lst = list(set(hyperedge_lst))

    return hyperedge_lst


def generate_largest_component(hypergraph):

    node_cc_lst = largest_component(hypergraph)
    hypergraph_cc = hypergraph.subhypergraph(node_cc_lst)
    hypergraph_cc_map = mapping_hypergraph(hypergraph_cc)

    return hypergraph_cc_map


def generate_parthypergraph(node_start_idx, node_end_idx, hyperedge_info):

    node_select_pre = [i for i in range(node_start_idx, node_end_idx)]

    # Select the hyperedges if its nodes belong to the list 'node_select_pre'.
    hyperedge_select = [edge for edge in hyperedge_info if all(value in node_select_pre for value in edge)]

    hypergraph_select = Hypergraph(hyperedge_select)
    hypergraph_select_map = mapping_hypergraph(hypergraph_select)

    return hypergraph_select_map


def generate_subthypergraph(node_start_idx, node_end_idx, hyperedge_info):

    node_select_pre = [i for i in range(node_start_idx, node_end_idx)]

    # Select the hyperedges if its nodes belong to the initial node list.
    hyperedge_select = []
    for edge in hyperedge_info:
        new_edge = list(filter(lambda x: x in node_select_pre, edge))
        if len(new_edge) >= 2:
            hyperedge_select.append(new_edge)

    hypergraph_select = Hypergraph(hyperedge_select)
    hypergraph_select_map = mapping_hypergraph(hypergraph_select)
    
    return hypergraph_select_map


if __name__ == "__main__":

    # dataset = "coauth-DBLP"
    # dataset = "contact-high-school"
    dataset = "congress-bills"
    # dataset = "threads-math-sx"
    # dataset = "email-Eu"

    hyperedge_list = from_data_to_hyperedge(dataset)

    # Set the start and end of the node interval.
    node_start = 0
    node_end = 100
    if dataset in ("coauth-DBLP", "contact-high-scholl", "congress-bills"):
        H_generated = generate_parthypergraph(node_start, node_end, hyperedge_list)
    elif dataset in ("email-Eu", "threads-math-sx"):
        H_generated = generate_subthypergraph(node_start, node_end, hyperedge_list)

    H_cc = generate_largest_component(H_generated)
    print(f"Processed {dataset}:", H_cc)

    file = open(f"./cleaned_datasets/demo-hyperedges.txt",'w')

    for edge in H_cc.get_edges():
        edge = str(edge).replace('(','').replace(')','') + '\n'
        file.write(edge)

    file.close()
