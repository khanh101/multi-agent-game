from typing import List, Dict, Tuple

import numpy as np
import scipy as sp
import scipy.optimize
import scipy.sparse


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


def minimal_sum_of_distances_controller(graph: np.ndarray, agent_list: List[int], goal_list: List[int]) -> List[List[int]]:
    '''
    :param graph: adjacency matrix
    :param agent_list: list of agents
    :param goal_list: list of goals
    :return: path from agents to goals
    '''
    # calculate distances between agents and goals
    indices = [*agent_list, *goal_list]
    dist, predecessor = bellman_ford(graph, indices)
    dist_adj = np.empty(shape=(len(agent_list), len(goal_list)), dtype=int)
    for h, a in enumerate(agent_list):
        for w, g in enumerate(goal_list):
            dist_adj[h, w] = dist[a][g]
    # assign agents to goals
    assignment = linear_sum_assignment(dist_adj)
    agent2goal: Dict[int, int] = {}
    for h, w in assignment:
        agent2goal[agent_list[h]] = goal_list[w]
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
