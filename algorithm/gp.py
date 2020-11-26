from typing import List, Tuple, Any, Callable, Dict, Optional

import numpy as np

from algorithm.util import bellman_ford, spectral_clustering, linear_sum_assignment, assignment_to_path


def graph_partitioning(graph: np.ndarray, agent_list: List[int], goal_list: List[int]) -> List[List[int]]:
    assignment, predecessor = graph_partitioning_assignment(graph, agent_list, goal_list)
    return assignment_to_path(agent_list, predecessor, assignment)


def graph_partitioning_assignment(graph: np.ndarray, agent_list: List[int], goal_list: List[int]) -> Tuple[List[Tuple[int, int]], Optional[Dict[int, np.ndarray]]]:
    if len(agent_list) == 0 or len(goal_list) == 0:
        return [], None



    # calculate distances between agents and goals
    indices = [*agent_list, *goal_list]
    dist, predecessor = bellman_ford(graph, indices)

    if len(indices) > 2:
        inv_dist_reduced = np.zeros(shape=(len(indices), len(indices)), dtype=float)
        for h in range(len(indices)):
            for w in range(len(indices)):
                if dist[indices[h]][indices[w]] != 0:
                    inv_dist_reduced[h, w] = 1 / dist[indices[h]][indices[w]]
                else:
                    inv_dist_reduced[h, w] = 1.0

        comm1_reduced, comm2_reduced = spectral_clustering(inv_dist_reduced, k=2)
        comm1 = [indices[i] for i in comm1_reduced]
        comm2 = [indices[i] for i in comm2_reduced]
        # verify cut: at least one partition has 2 types of node
        def exists(seq: List[Any], cond: Callable[[Any], bool]) -> bool:
            for elem in seq:
                if cond(elem):
                    return True
            return False

        def filter(seq: List[Any], cond: Callable[[Any], bool]) -> Tuple[List[Any], List[Any]]:
            true = []
            false = []
            for elem in seq:
                if cond(elem):
                    true.append(elem)
                else:
                    false.append(elem)
            return true, false


        if exists(comm1, lambda elem: elem in agent_list) and exists(comm1, lambda elem: elem in goal_list) and exists(comm2, lambda elem: elem in agent_list) and exists(comm2, lambda elem: elem in goal_list):
            # bi-partition
            comm1_agent_list, comm1_goal_list = filter(comm1, lambda elem: elem in agent_list)
            comm2_agent_list, comm2_goal_list = filter(comm2, lambda elem: elem in agent_list)
            assignment1, _ = graph_partitioning_assignment(graph, comm1_agent_list, comm1_goal_list)
            assignment2, _ = graph_partitioning_assignment(graph, comm2_agent_list, comm2_goal_list)
            return [*assignment1, *assignment2], predecessor

    bipartite_dist_adj = np.empty(shape=(len(agent_list), len(goal_list)), dtype=int)
    for h, a in enumerate(agent_list):
        for w, g in enumerate(goal_list):
            bipartite_dist_adj[h, w] = dist[a][g]
    assignment_reduced = linear_sum_assignment(bipartite_dist_adj)
    assignment = [(agent_list[h], goal_list[w]) for h, w in assignment_reduced]
    return assignment, predecessor


