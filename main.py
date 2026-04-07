import networkx as nx
from partition import recover_partitions
from tree_iso import are_trees_isomorphic
from utils import graph_join
from optimization_iso import solve_isomorphism
import numpy as np


def check_join_tree_isomorphism(C, F):
    # graph isomorphism check on given grpahs
    if not nx.is_isomorphic(C, F):
        print("Graphs are NOT isomorphic")
        return False

    print("Graphs are isomorphic")

    # recover partitions
    A_nodes, B_nodes = recover_partitions(C)
    D_nodes, E_nodes = recover_partitions(F)

    if A_nodes is None or D_nodes is None:
        print("Partition recovery failed")
        return False

    # extract subgraphs
    A = C.subgraph(A_nodes).copy()
    B = C.subgraph(B_nodes).copy()
    D = F.subgraph(D_nodes).copy()
    E = F.subgraph(E_nodes).copy()

    # tree isomorphism on partitions
    case1 = are_trees_isomorphic(A, D) and are_trees_isomorphic(B, E)
    case2 = are_trees_isomorphic(A, E) and are_trees_isomorphic(B, D)

    if case1 or case2:
        print("Sub-isomorphism verified")
        return True
    else:
        print("Sub-isomorphism NOT verified")
        return False

def check_partition_mapping(A, B, D, E, perm):
    map_A = set(perm[i] for i in A)
    map_B = set(perm[i] for i in B)

    if map_A.issubset(D) and map_B.issubset(E):
        return "A→D, B→E"
    elif map_A.issubset(E) and map_B.issubset(D):
        return "A→E, B→D"
    else:
        return "Mixed (FAIL)"
    



#test
if __name__ == "__main__":
    # Example trees
    A = nx.path_graph(5)
    B = nx.star_graph(4)

    D = nx.path_graph(5)
    E = nx.star_graph(4)

    # Build joins
    C = graph_join(A, B)
    F = graph_join(D, E)

    result = check_join_tree_isomorphism(C, F)
    print("Final Result:", result)

    # P, score = solve_isomorphism(C, F)

    # print("Matching score:", score)
    # print("Permutation matrix:\n", P)

    

