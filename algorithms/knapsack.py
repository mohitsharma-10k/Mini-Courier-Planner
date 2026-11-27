"""
Dynamic Programming: 0/1 Knapsack Algorithm for Parcel Packing
Phase 2 Assessment Component

Solves the optimal box filling problem:
Given a fleet vehicle with capacity W (kg), and a list of N parcels each having
weight w_i (converted to integer discrete units, e.g. 100g = 0.1kg) and priority/value v_i.
Find the subset of parcels that maximizes total value without exceeding capacity W.
"""
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass
from models.parcel import Parcel


@dataclass
class KnapsackResult:
    selected_parcels: List[Parcel]
    total_weight_kg: float
    total_value: int
    capacity_limit_kg: float
    capacity_utilization_pct: float
    dp_table: List[List[int]]           # Full DP matrix for submission evidence
    num_items_considered: int
    num_weight_states: int


def knapsack_01_dp(parcels: List[Parcel], capacity_kg: float, unit_scale: int = 10) -> KnapsackResult:
    """
    Computes optimal 0/1 Knapsack parcel selection using bottom-up tabulation.

    Recurrence relation:
      dp[i][w] = dp[i-1][w]                                    if w_i > w
      dp[i][w] = max(dp[i-1][w], dp[i-1][w - w_i] + v_i)        if w_i <= w

    Complexity:
      Time Complexity:  O(N * W) where N = len(parcels), W = capacity_units
      Space Complexity: O(N * W) for table with full backtracking evidence
    """
    n = len(parcels)
    W = int(round(capacity_kg * unit_scale))

    # Convert parcel weights to integer units
    weights = [int(round(p.weight_kg * unit_scale)) for p in parcels]
    values = [p.value for p in parcels]

    # Initialize DP table (n + 1) x (W + 1) with 0
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    # Bottom-up Tabulation
    for i in range(1, n + 1):
        wt_i = weights[i - 1]
        val_i = values[i - 1]
        for w in range(W + 1):
            if wt_i <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - wt_i] + val_i)
            else:
                dp[i][w] = dp[i - 1][w]

    # Optimal max value achieved
    max_value = dp[n][W]

    # Backtracking to reconstruct selected parcels
    selected_parcels: List[Parcel] = []
    curr_w = W
    for i in range(n, 0, -1):
        # If value differs from the cell above it, item i was included
        if dp[i][curr_w] != dp[i - 1][curr_w]:
            selected_parcels.append(parcels[i - 1])
            curr_w -= weights[i - 1]

    # Reverse to preserve original prioritised order
    selected_parcels.reverse()

    total_weight = sum(p.weight_kg for p in selected_parcels)
    total_weight = round(total_weight, 2)
    utilization = (total_weight / capacity_kg * 100.0) if capacity_kg > 0 else 0.0

    return KnapsackResult(
        selected_parcels=selected_parcels,
        total_weight_kg=total_weight,
        total_value=max_value,
        capacity_limit_kg=capacity_kg,
        capacity_utilization_pct=round(utilization, 2),
        dp_table=dp,
        num_items_considered=n,
        num_weight_states=W + 1
    )


def format_dp_table_snippet(result: KnapsackResult, max_rows: int = 10, max_cols: int = 15) -> str:
    """
    Renders an ASCII snippet of the DP matrix for report evidence and grading.
    """
    dp = result.dp_table
    rows = min(len(dp), max_rows + 1)
    cols = min(len(dp[0]), max_cols + 1)

    lines = []
    lines.append("DP Table Snippet: dp[item_idx][capacity_units]")
    
    # Header
    header = "Item \\ W |" + "".join(f"{w:5d}" for w in range(cols))
    lines.append(header)
    lines.append("-" * len(header))

    for i in range(rows):
        row_str = f"  i={i:<4d}|" + "".join(f"{dp[i][w]:5d}" for w in range(cols))
        lines.append(row_str)

    if len(dp) > rows or len(dp[0]) > cols:
        lines.append(f"... (Table continues up to {len(dp)-1} items and {len(dp[0])-1} capacity units)")

    return "\n".join(lines)
