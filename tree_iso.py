def tree_canonical_form(G):
    #AHU algo for trees

    def encode(node, parent):
        labels = []
        for nei in G.neighbors(node):
            if nei != parent:
                labels.append(encode(nei, node))
        labels.sort()
        return "(" + "".join(labels) + ")"

    forms = [encode(v, None) for v in G.nodes()]
    return min(forms)


def are_trees_isomorphic(T1, T2):
    return tree_canonical_form(T1) == tree_canonical_form(T2)