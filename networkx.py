import gurobipy as gp
from gurobipy import GRB
import numpy as np

def graph_isomorphism(A, B, time_limit=60):
    n = A.shape[0]

    model = gp.Model("GI_fast")
    # model.setParam('TimeLimit', time_limit)


    # Variables

    X = model.addVars(n, n, vtype=GRB.BINARY, name="X")

    # Permutation constraints
    for i in range(n):
        model.addConstr(gp.quicksum(X[i, j] for j in range(n)) == 1)

    for j in range(n):
        model.addConstr(gp.quicksum(X[i, j] for i in range(n)) == 1)

    # Degree pruning (to find subgraphs)
    degA = np.sum(A, axis=1)
    degB = np.sum(B, axis=1)

    for i in range(n):
        for j in range(n):
            if degA[i] != degB[j]:
                model.addConstr(X[i, j] == 0)

    # Edge consistency constraints

    edges_A = [(i,k) for i in range(n) for k in range(n) if A[i,k] == 1 and i < k]
    non_edges_A = [(i,k) for i in range(n) for k in range(n) if A[i,k] == 0 and i < k]
    edges_B = [(j,l) for j in range(n) for l in range(n) if B[j,l] == 1 and j < l]
    non_edges_B = [(j,l) for j in range(n) for l in range(n) if B[j,l] == 0 and j < l]

    #edge to edge
    for i in range(n):
        for k in range(n):
            if A[i, k] == 1:
                for j in range(n):
                    for l in range(n):
                        if B[j, l] == 0:
                            model.addConstr(X[i, j] + X[k, l] <= 1)
    #non edge to edge
    for i in range(n):
        for k in range(n):
            if A[i, k] == 0 and i != k:
                for j in range(n):
                    for l in range(n):
                        if B[j, l] == 1:
                            model.addConstr(X[i, j] + X[k, l] <= 1)
                            

    # Symmetry breaking

    if degA[0] == degB[0]:
        model.addConstr(X[0, 0] == 1)


    model.setObjective(0, GRB.MINIMIZE)
    model.optimize()

    if model.status == GRB.OPTIMAL:
        X_sol = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                X_sol[i, j] = X[i, j].x
        return True, X_sol

    return False, None


A = np.array([
    [0,1,1,0,0],
    [1,0,0,0,0],
    [1,0,0,1,1],
    [0,0,1,0,0],
    [0,0,1,0,0]
])

B = np.array([
    [0,0,1,0,0],
    [0,0,0,0,1],
    [1,0,0,1,1],
    [0,0,1,0,0],
    [0,1,1,0,0]
])

iso, obj = graph_isomorphism(A, B)

print("Isomorphic:", iso)
print("Permutation matrix:", obj)
