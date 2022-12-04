import numpy as np

def mat_to_list(mat):
    adj_list = {}

    for i in range(len(mat)):
        i_neighbors = {}
        for j in range(len(mat[i])):
            if (mat[i][j] != 0):
                i_neighbors[j] = mat[i][j]

        adj_list[i] = i_neighbors

    return adj_list