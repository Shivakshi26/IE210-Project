import networkx as nx

def recover_partitions(G):
    G_comp = nx.complement(G)
    components = list(nx.connected_components(G_comp))

    group1 = set()
    group2 = set()

    for comp in components:
        temp1 = group1 | comp
        if valid_tree_partition(G, temp1, group2):
            group1 = temp1
        else:
            temp2 = group2 | comp
            if valid_tree_partition(G, group1, temp2):
                group2 = temp2
            else:
                return None, None

    return list(group1), list(group2)


def valid_tree_partition(G, g1, g2):
    sub1 = G.subgraph(g1)
    sub2 = G.subgraph(g2)

    return is_tree(sub1) and is_tree(sub2)


def is_tree(G):
    return nx.is_connected(G) and len(G.edges()) == len(G.nodes()) - 1