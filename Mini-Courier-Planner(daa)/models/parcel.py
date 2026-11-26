"""
Parcel Data Model
Represents a package to be delivered in the courier system.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Parcel:
    parcel_id: str
    recipient_name: str
    destination_node_id: int
    weight_kg: float          # Weight in kg (e.g. 2.5)
    value: int                # Value / Utility / Revenue / Priority Score (integer for Knapsack DP)
    deadline_hour: float      # Required delivery deadline (hours from shift start, e.g. 3.5)
    description: str = ""

    @property
    def weight_units(self) -> int:
        """
        Integer representation of weight (in 100g = 0.1kg hectograms)
        Used for exact 0/1 Knapsack Dynamic Programming table indexing.
        """
        return int(round(self.weight_kg * 10))

    @property
    def value_density(self) -> float:
        """Value per kilogram ratio (useful for greedy heuristics)."""
        return self.value / self.weight_kg if self.weight_kg > 0 else 0.0

    @property
    def priority_ratio(self) -> float:
        """
        Calculates composite priority score:
        Higher value and earlier deadline produce higher priority.
        Priority = Value / (Deadline * Weight)
        """
        safe_deadline = max(0.5, self.deadline_hour)
        safe_weight = max(0.1, self.weight_kg)
        return self.value / (safe_deadline * safe_weight)

    def to_dict(self):
        return {
            "ID": self.parcel_id,
            "Recipient": self.recipient_name,
            "DestNode": self.destination_node_id,
            "Weight(kg)": self.weight_kg,
            "Value": self.value,
            "Deadline(h)": self.deadline_hour,
            "PriorityRatio": round(self.priority_ratio, 2),
            "Desc": self.description
        }

    def __repr__(self) -> str:
        return (f"Parcel({self.parcel_id}, Dest:{self.destination_node_id}, "
                f"Wt:{self.weight_kg}kg, Val:{self.value}, "
                f"Due:{self.deadline_hour}h, Ratio:{self.priority_ratio:.2f})")
