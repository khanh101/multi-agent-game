from typing import List, Dict, Tuple, Set

import numpy as np
import scipy as sp
import scipy.optimize
import scipy.sparse
from sklearn.cluster import SpectralClustering


def shortest_path(adj: np.ndarray, indices: List[int]) -> Tuple[Dict[int, np.ndarray], Dict[int, np.ndarray]]:
    '''
    shortest path algorithm
    :param adj: adjacency matrix
    :param indices: indices of nodes used to calculate distances
    :return dist: dist[i][j]: distance from node (i) to node (j) (i: row, j col)
    :return predecessor:    predecessor[j][i] : first node to move from node (i) to node (j) (i: row, j: col)
                            if predecessor[j][i] == i: two nodes are neighbour
    '''
    dist_reduced, predecessor_reduced = sp.sparse.csgraph.shortest_path(
        method="D", # Dijkstra
        csgraph=adj,
        directed=True,
        indices=indices,
        return_predecessors=True,
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

def spectral_clustering(adj: np.ndarray, k: int = 2) -> List[Set[int]]:
    clustering = SpectralClustering(n_clusters=k, affinity="precomputed").fit(adj)
    label = list(clustering.labels_)
    comm: List[Set[int]] = []
    for l in set(label):
        c = []
        for node in range(len(label)):
            if label[node] == l:
                c.append(node)
        comm.append(set(c))
    return comm

def assignment_to_path(agent_list: List[int], predecessor: Dict[int, np.ndarray], assignment: List[Tuple[int, int]]) -> List[List[int]]:
    agent2goal: Dict[int, int] = {}
    for a, g in assignment:
        agent2goal[a] = g
    # find next position of agents
    next_agent_path: List[List[int]] = [[a] for a in agent_list]
    for i, a in enumerate(agent_list):
        g = agent2goal.get(a, None)
        if g is None:  # agent does not need to move
            continue
        current_a = a
        while True:
            next_a = predecessor[g][current_a]
            if next_a == -9999:  # goal found
                break
            next_agent_path[i].append(next_a)
            current_a = next_a
    return next_agent_path
