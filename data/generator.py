"""
Synthetic Data Generator for Scalability Testing
Phase 4 Performance Evaluation
"""
import random
import math
from typing import List, Tuple
from models.parcel import Parcel
from models.delivery_point import DeliveryPoint
from models.graph import RoadGraph


def generate_synthetic_scenario(
    num_parcels: int,
    num_nodes: int = 20,
    seed: int = 42
) -> Tuple[RoadGraph, List[Parcel]]:
    """
    Generates a reproducible connected urban graph and list of parcels.
    """
    random.seed(seed)
    graph = RoadGraph()

    # 1. Generate delivery nodes in a 15km x 15km city grid
    # Node 0 is Depot at center (0, 0)
    depot = DeliveryPoint(0, "Central Depot Hub", 0.0, 0.0, is_depot=True)
    graph.add_node(depot)

    for i in range(1, num_nodes):
        # Cluster nodes around city center
        radius = random.uniform(1.5, 12.0)
        angle = random.uniform(0, 2 * math.pi)
        x = round(radius * math.cos(angle), 2)
        y = round(radius * math.sin(angle), 2)
        graph.add_node(DeliveryPoint(i, f"Delivery Zone {i}", x, y))

    # 2. Build connected planar-like road network (Spanning Tree + extra edges)
    # Ensure graph is connected via Prim/Kruskal-like nearest connections
    all_nodes = list(graph.nodes.values())
    connected = {0}
    unconnected = set(range(1, num_nodes))

    # Connect all nodes to ensure no isolated vertices
    while unconnected:
        u = random.choice(list(connected))
        # Find nearest unconnected node to u
        v = min(unconnected, key=lambda node_idx: all_nodes[u].euclidean_distance_to(all_nodes[node_idx]))
        dist = round(all_nodes[u].euclidean_distance_to(all_nodes[v]) * random.uniform(1.1, 1.3), 2)
        graph.add_edge(u, v, dist)
        unconnected.remove(v)
        connected.add(v)

    # Add extra random shortcut road segments
    extra_edges = num_nodes * 2
    for _ in range(extra_edges):
        u = random.randint(0, num_nodes - 1)
        v = random.randint(0, num_nodes - 1)
        if u != v:
            existing = [nbr for nbr, _ in graph.get_neighbors(u)]
            if v not in existing:
                dist = round(all_nodes[u].euclidean_distance_to(all_nodes[v]) * random.uniform(1.1, 1.4), 2)
                graph.add_edge(u, v, dist)

    # 3. Generate parcels
    parcels: List[Parcel] = []
    descriptions = [
        "Electronics", "Medical Box", "Apparel", "Documents", "Groceries",
        "Home Appliances", "Books", "Auto Parts", "Perishables", "Hardware"
    ]

    for p_id in range(1, num_parcels + 1):
        dest = random.randint(1, num_nodes - 1)
        wt = round(random.uniform(0.5, 8.0), 1)
        val = random.randint(15, 150)
        due = round(random.uniform(1.0, 8.0), 1)
        desc = random.choice(descriptions)

        parcels.append(Parcel(
            parcel_id=f"SYN-{p_id:04d}",
            recipient_name=f"Customer {p_id}",
            destination_node_id=dest,
            weight_kg=wt,
            value=val,
            deadline_hour=due,
            description=desc
        ))

    return graph, parcels
