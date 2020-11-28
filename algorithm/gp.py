from typing import List, Tuple, Any, Callable, Dict, Optional

import numpy as np

from algorithm.util import shortest_path, graph_partitioning, linear_sum_assignment, assignment_to_path


def graph_partitioning_controller(graph: np.ndarray, agent_list: List[int], goal_list: List[int]) -> List[List[int]]:
    assignment, predecessor = graph_partitioning_assignment(graph, agent_list, goal_list)
    return assignment_to_path(agent_list, predecessor, assignment)


def graph_partitioning_assignment(graph: np.ndarray, agent_list: List[int], goal_list: List[int]) -> Tuple[
    List[Tuple[int, int]], Optional[Dict[int, np.ndarray]]]:
    if len(agent_list) == 0 or len(goal_list) == 0:
        return [], None

    # calculate distances between agents and goals
    indices = [*agent_list, *goal_list]
    dist, predecessor = shortest_path(graph, indices)

    def nearest(dist: np.ndarray, indices: List[int]) -> int:
        idx = None
        minimal = float("inf")
        for i in indices:
            if dist[i] < minimal:
                idx = i
                minimal = dist[i]
        return idx

    # one agent, find nearest goal
    if len(agent_list) == 1:
        a = agent_list[0]
        g = nearest(dist[a], goal_list)
        return [(a, g)], predecessor
    # more agents than goals, convert to msoc
    if len(goal_list) < len(agent_list):
        # msoc
        ag_dist_adj = np.empty(shape=(len(agent_list), len(goal_list)), dtype=float)
        for h, a in enumerate(agent_list):
            for w, g in enumerate(goal_list):
                ag_dist_adj[h, w] = dist[a][g]
        # assign agents to goals
        assignment_reduced = linear_sum_assignment(ag_dist_adj)
        assignment = [(agent_list[h], goal_list[w]) for h, w in assignment_reduced]
        return assignment, predecessor

    # otherwise, partition the graph and assign each partition to an agent
    inv_goal_dist = np.empty(shape=(len(goal_list), len(goal_list)), dtype=float)
    for h, g_h in enumerate(goal_list):
        for w, g_w in enumerate(goal_list):
            d = dist[g_h][g_w]
            if d == 0: d = 1.0
            inv_goal_dist[h, w] = 1 / d

    comm_reduced_list = graph_partitioning(inv_goal_dist, k=len(agent_list))
    comm_list: List[List[int]] = []
    for comm_reduced in comm_reduced_list:
        comm_list.append([goal_list[i] for i in comm_reduced])

    ac_dist = np.empty(shape=(len(agent_list), len(comm_list)), dtype=float)
    for i_a, a in enumerate(agent_list):
        for i_c, comm in enumerate(comm_list):
            least_dist = float("inf")
            for g in comm:
                if dist[a][g] < least_dist:
                    least_dist = dist[a][g]
            ac_dist[i_a, i_c] = least_dist

    comm_reduced_assignment = linear_sum_assignment(ac_dist)
    comm_assignment: List[Tuple[int, List[int]]] = []
    for i_a, i_c in comm_reduced_assignment:
        comm_assignment.append((agent_list[i_a], comm_list[i_c]))

    assignment: List[Tuple[int, int]] = []
    for a, comm in comm_assignment:
        g = nearest(dist[a], comm)
        assignment.append((a, g))
    return assignment, predecessor
