"""
Dijkstra's Algorithm for Shortest Path Computation
Phase 3 Assessment Component

Computes optimal shortest paths across the road network graph using a Min-Priority Queue (Binary Heap).
Supports:
1. Single-source shortest path with parent backtracking for route reconstruction.
2. All-pairs shortest path matrix generation for selected delivery locations.

Complexity:
  Time:  O((V + E) log V) with Min-Heap
  Space: O(V + E)
"""
import heapq
from typing import Dict, List, Tuple, Set
from models.graph import RoadGraph


def dijkstra_shortest_paths(graph: RoadGraph, source: int) -> Tuple[Dict[int, float], Dict[int, List[int]]]:
    """
    Executes Dijkstra's algorithm from a given source node.

    Returns:
      distances: mapping of node_id -> shortest distance from source (in km)
      paths: mapping of node_id -> full sequence of nodes along the shortest path
    """
    if source not in graph.nodes:
        raise ValueError(f"Source node {source} not present in road network graph.")

    # Distance dictionary initialized to infinity
    distances: Dict[int, float] = {node_id: float('inf') for node_id in graph.nodes}
    distances[source] = 0.0

    # Predecessor dictionary for path reconstruction
    predecessors: Dict[int, int] = {source: None}

    # Min-Heap priority queue: stores (distance, node_id)
    pq: List[Tuple[float, int]] = [(0.0, source)]
    visited: Set[int] = set()

    while pq:
        curr_dist, u = heapq.heappop(pq)

        if u in visited:
            continue
        visited.add(u)

        # Explore neighbors
        for v, weight in graph.get_neighbors(u):
            if v in visited:
                continue
            new_dist = curr_dist + weight
            if new_dist < distances[v]:
                distances[v] = round(new_dist, 2)
                predecessors[v] = u
                heapq.heappush(pq, (new_dist, v))

    # Reconstruct explicit path trajectories
    paths: Dict[int, List[int]] = {}
    for target in graph.nodes:
        if distances[target] == float('inf'):
            paths[target] = []
            continue

        curr = target
        path = []
        while curr is not None:
            path.append(curr)
            curr = predecessors.get(curr)
        path.reverse()
        paths[target] = path

    return distances, paths


def compute_all_pairs_distances(graph: RoadGraph, node_subset: List[int]) -> Tuple[Dict[Tuple[int, int], float], Dict[Tuple[int, int], List[int]]]:
    """
    Runs Dijkstra from each node in node_subset to build a complete pairwise distance matrix.
    Useful for feeding into the TSP route solver.
    """
    dist_matrix: Dict[Tuple[int, int], float] = {}
    detailed_paths: Dict[Tuple[int, int], List[int]] = {}

    for u in node_subset:
        dists, paths = dijkstra_shortest_paths(graph, u)
        for v in node_subset:
            dist_matrix[(u, v)] = dists[v]
            detailed_paths[(u, v)] = paths[v]

    return dist_matrix, detailed_paths
