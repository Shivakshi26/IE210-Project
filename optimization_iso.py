import gurobipy as gp
from gurobipy import GRB
import networkx as nx
import numpy as np


def graph_to_matrix(G):
    return nx.to_numpy_array(G)



def solve_isomorphism(C_graph, F_graph):
    C = graph_to_matrix(C_graph)
    F = graph_to_matrix(F_graph)

    n = C.shape[0]

    model = gp.Model("graph_isomorphism")


    P = model.addVars(n, n, vtype=GRB.BINARY, name="P")

    for i in range(n):
        model.addConstr(gp.quicksum(P[i, k] for k in range(n)) == 1)

    for k in range(n):
        model.addConstr(gp.quicksum(P[i, k] for i in range(n)) == 1)


    obj = gp.QuadExpr()

    for i in range(n):
        for j in range(n):
            if C[i, j] == 0:
                continue
            for k in range(n):
                for l in range(n):
                    if F[k, l] == 0:
                        continue
                    obj += C[i, j] * F[k, l] * P[i, k] * P[j, l]

    model.setObjective(obj, GRB.MAXIMIZE)

    model.setParam("OutputFlag", 1)
    model.optimize()


    if model.status == GRB.OPTIMAL:
        P_sol = np.zeros((n, n))
        for i in range(n):
            for k in range(n):
                P_sol[i, k] = P[i, k].X

        return P_sol, model.objVal
    else:
        return None, None