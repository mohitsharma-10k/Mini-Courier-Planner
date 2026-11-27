"""
Delivery Point Model
Represents physical locations (Depot hub, customer delivery addresses).
"""
from dataclasses import dataclass
import math


@dataclass
class DeliveryPoint:
    node_id: int
    name: str
    x_coord: float           # Cartesian X coordinate (km)
    y_coord: float           # Cartesian Y coordinate (km)
    is_depot: bool = False

    def euclidean_distance_to(self, other: "DeliveryPoint") -> float:
        """Calculates straight-line geometric distance between two points."""
        return math.hypot(self.x_coord - other.x_coord, self.y_coord - other.y_coord)

    def __repr__(self) -> str:
        role = "DEPOT" if self.is_depot else "CUSTOMER"
        return f"[{self.node_id}] {self.name} ({role}) @ ({self.x_coord:.1f}, {self.y_coord:.1f})"
