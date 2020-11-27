from typing import List, Dict
import numpy as np

from algorithm.util import shortest_path, linear_sum_assignment, assignment_to_path


def minimal_sum_of_costs(graph: np.ndarray, agent_list: List[int], goal_list: List[int]) -> List[List[int]]:
    '''
    :param graph: adjacency matrix
    :param agent_list: list of agents
    :param goal_list: list of goals
    :return: path from agents to goals
    '''
    # calculate distances between agents and goals
    indices = [*agent_list, *goal_list]
    dist, predecessor = shortest_path(graph, indices)
    ag_dist_adj = np.empty(shape=(len(agent_list), len(goal_list)), dtype=float)
    for h, a in enumerate(agent_list):
        for w, g in enumerate(goal_list):
            ag_dist_adj[h, w] = dist[a][g]
    # assign agents to goals
    assignment_reduced = linear_sum_assignment(ag_dist_adj)
    assignment = [(agent_list[h], goal_list[w]) for h, w in assignment_reduced]
    return assignment_to_path(agent_list, predecessor, assignment)
