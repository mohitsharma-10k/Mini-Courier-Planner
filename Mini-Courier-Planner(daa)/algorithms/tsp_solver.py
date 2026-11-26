"""
Traveling Salesperson Problem (TSP) Route Planner
Phase 3 Assessment Component

Constructs an efficient delivery tour visiting all selected customer locations:
1. Nearest Neighbor Heuristic - Greedy O(K^2) approximation
2. 2-Opt Local Search - Iterative edge-swap tour refinement
"""
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class RouteLeg:
    from_node: int
    to_node: int
    distance_km: float
    road_path: List[int]
    cumulative_distance_km: float


@dataclass
class TSPTourResult:
    initial_tour: List[int]
    initial_distance_km: float
    refined_tour: List[int]
    refined_distance_km: float
    savings_km: float
    legs: List[RouteLeg]
    total_stops: int
    estimated_travel_time_min: float


def _calculate_tour_distance(tour: List[int], dist_matrix: Dict[Tuple[int, int], float]) -> float:
    """Calculates total closed circuit distance of a tour."""
    total = 0.0
    for i in range(len(tour) - 1):
        u, v = tour[i], tour[i + 1]
        total += dist_matrix.get((u, v), float('inf'))
    return round(total, 2)


def solve_tsp_nearest_neighbor(
    depot_node: int,
    customer_nodes: List[int],
    dist_matrix: Dict[Tuple[int, int], float]
) -> List[int]:
    """
    Constructs a delivery tour using the Nearest Neighbor (NN) approximation algorithm.
    Starts at depot_node, greedily visits the closest unvisited customer, and returns to depot.

    Time Complexity: O(K^2) where K is number of delivery locations.
    """
    unvisited = set(customer_nodes)
    if depot_node in unvisited:
        unvisited.remove(depot_node)

    current = depot_node
    tour = [depot_node]

    while unvisited:
        # Find nearest unvisited customer
        nearest_node = None
        min_dist = float('inf')

        for candidate in unvisited:
            d = dist_matrix.get((current, candidate), float('inf'))
            if d < min_dist:
                min_dist = d
                nearest_node = candidate

        if nearest_node is None:
            # Graph disconnected fallback
            nearest_node = list(unvisited)[0]

        tour.append(nearest_node)
        unvisited.remove(nearest_node)
        current = nearest_node

    # Complete the loop back to depot
    tour.append(depot_node)
    return tour


def refine_tour_2opt(
    tour: List[int],
    dist_matrix: Dict[Tuple[int, int], float],
    max_iterations: int = 500
) -> Tuple[List[int], float]:
    """
    Applies 2-Opt local search heuristic to untangle crossing paths in the tour.
    Iteratively reverses tour segments whenever doing so shortens the total tour distance.

    Time Complexity: O(iterations * K^2)
    """
    best_tour = list(tour)
    best_dist = _calculate_tour_distance(best_tour, dist_matrix)
    improved = True
    iteration = 0

    while improved and iteration < max_iterations:
        improved = False
        iteration += 1

        # Check all pairs of non-adjacent edges (i, i+1) and (j, j+1)
        for i in range(1, len(best_tour) - 2):
            for j in range(i + 1, len(best_tour) - 1):
                # Current edges: (tour[i-1], tour[i]) and (tour[j], tour[j+1])
                # Proposed edges: (tour[i-1], tour[j]) and (tour[i], tour[j+1])
                a, b = best_tour[i - 1], best_tour[i]
                c, d = best_tour[j], best_tour[j + 1]

                current_cost = dist_matrix.get((a, b), float('inf')) + dist_matrix.get((c, d), float('inf'))
                proposed_cost = dist_matrix.get((a, c), float('inf')) + dist_matrix.get((b, d), float('inf'))

                if proposed_cost < current_cost - 1e-4:
                    # Reverse segment between i and j
                    best_tour[i:j + 1] = reversed(best_tour[i:j + 1])
                    best_dist = _calculate_tour_distance(best_tour, dist_matrix)
                    improved = True
                    break
            if improved:
                break

    return best_tour, best_dist


def build_complete_delivery_itinerary(
    depot_node: int,
    customer_nodes: List[int],
    dist_matrix: Dict[Tuple[int, int], float],
    detailed_paths: Dict[Tuple[int, int], List[int]],
    average_speed_kmh: float = 30.0
) -> TSPTourResult:
    """
    Executes Nearest Neighbor TSP + 2-Opt refinement and maps out complete turn-by-turn road legs.
    """
    # 1. Nearest Neighbor
    initial_tour = solve_tsp_nearest_neighbor(depot_node, customer_nodes, dist_matrix)
    initial_dist = _calculate_tour_distance(initial_tour, dist_matrix)

    # 2. 2-Opt Refinement
    refined_tour, refined_dist = refine_tour_2opt(initial_tour, dist_matrix)
    savings = round(initial_dist - refined_dist, 2)

    # 3. Build Detailed Road Route Legs
    legs: List[RouteLeg] = []
    cum_dist = 0.0

    for i in range(len(refined_tour) - 1):
        u, v = refined_tour[i], refined_tour[i + 1]
        leg_dist = dist_matrix.get((u, v), 0.0)
        road_path = detailed_paths.get((u, v), [u, v])
        cum_dist = round(cum_dist + leg_dist, 2)

        legs.append(RouteLeg(
            from_node=u,
            to_node=v,
            distance_km=leg_dist,
            road_path=road_path,
            cumulative_distance_km=cum_dist
        ))

    # Travel time estimate (minutes) + 5 minutes service per stop
    travel_time_hours = refined_dist / average_speed_kmh if average_speed_kmh > 0 else 0
    total_time_min = round(travel_time_hours * 60.0 + len(customer_nodes) * 5.0, 1)

    return TSPTourResult(
        initial_tour=initial_tour,
        initial_distance_km=initial_dist,
        refined_tour=refined_tour,
        refined_distance_km=refined_dist,
        savings_km=savings,
        legs=legs,
        total_stops=len(customer_nodes),
        estimated_travel_time_min=total_time_min
    )
