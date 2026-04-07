import networkx as nx


def graph_join(G1, G2):
    G = nx.disjoint_union(G1, G2)

    n1 = len(G1.nodes())
    n2 = len(G2.nodes())

    for u in range(n1):
        for v in range(n1, n1 + n2):
            G.add_edge(u, v)

    return G