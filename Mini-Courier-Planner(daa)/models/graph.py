"""
Road Graph Data Model
Represents the city's road network using an Adjacency List.
Supports bidirectional road segments with traffic/distance weights.
"""
from typing import Dict, List, Tuple
from .delivery_point import DeliveryPoint


class RoadGraph:
    def __init__(self):
        self.nodes: Dict[int, DeliveryPoint] = {}
        # adjacency list: node_id -> list of (neighbor_id, distance_km)
        self.adj_list: Dict[int, List[Tuple[int, float]]] = {}

    def add_node(self, node: DeliveryPoint):
        self.nodes[node.node_id] = node
        if node.node_id not in self.adj_list:
            self.adj_list[node.node_id] = []

    def add_edge(self, u: int, v: int, distance_km: float, bidirectional: bool = True):
        if u not in self.nodes or v not in self.nodes:
            raise ValueError(f"Nodes {u} and {v} must be added to graph before adding edge.")
        
        self.adj_list[u].append((v, round(distance_km, 2)))
        if bidirectional:
            self.adj_list[v].append((u, round(distance_km, 2)))

    def get_neighbors(self, u: int) -> List[Tuple[int, float]]:
        return self.adj_list.get(u, [])

    @property
    def total_nodes(self) -> int:
        return len(self.nodes)

    @property
    def total_edges(self) -> int:
        # Undirected graph edge count
        count = sum(len(edges) for edges in self.adj_list.values())
        return count // 2

    def display_summary(self):
        print(f"Road Network Graph: {self.total_nodes} locations, {self.total_edges} bidirectional road segments.")
