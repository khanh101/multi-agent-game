from typing import List, Dict, Tuple

import numpy as np
import scipy as sp
import scipy.sparse
import scipy.optimize


def bellman_ford(adj: np.ndarray, indices: List[int]) -> Tuple[Dict[int, np.ndarray], Dict[int, np.ndarray]]:
    '''
    bellman ford algorithm
    :param adj: adjacency matrix
    :param indices: indices of nodes used to calculate distances
    :return dist: dist[i][j]: distance from node (i) to node (j) (i: row, j col)
    :return predecessor:    predecessor[j][i] : first node to move from node (i) to node (j) (i: row, j: col)
                            if predecessor[j][i] == i: two nodes are neighbour
    '''
    dist_reduced, predecessor_reduced = sp.sparse.csgraph.bellman_ford(
        csgraph=adj,
        directed=False,
        indices=indices,
        return_predecessors=True,
        unweighted=True,
    )
    # dist[i, j]: distance from indices[i] to j
    # predecessor[i, j]: path from indices[i] to j
    dist: Dict[int, np.ndarray] = {}
    predecessor: Dict[int, np.ndarray] = {}
    for i, idx in enumerate(indices):
        dist[idx] = dist_reduced[i]
        predecessor[idx] = predecessor_reduced[i]
    return dist, predecessor


def linear_sum_assignment(cost_matrix: np.ndarray) -> List[Tuple[int, int]]:
    '''
    see scipy.optimize.linear_sum_assignment
    :param cost_matrix:
    :return:
    '''
    row, col = sp.optimize.linear_sum_assignment(cost_matrix=cost_matrix, maximize=False)
    assignment: List[Tuple[int, int]] = [(row[i], col[i]) for i in range(len(row))]
    return assignment
