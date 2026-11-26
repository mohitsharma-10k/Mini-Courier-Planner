"""
Sorting Algorithms Implementation:
1. Merge Sort (Divide & Conquer) - O(n log n) Guaranteed Time, O(n) Auxiliary Space
2. Quick Sort (Divide & Conquer with Median-of-Three Partitioning) - O(n log n) Average, O(n^2) Worst

Implements parcel prioritization by:
- 'deadline': Earliest Delivery Deadline first (Ascending)
- 'priority': Highest Value / Priority score first (Descending)
- 'priority_ratio': Highest Urgency-Value Ratio first (Descending)
"""
from typing import List, Callable, Tuple
import copy
from dataclasses import dataclass
from models.parcel import Parcel


@dataclass
class SortMetrics:
    comparisons: int = 0
    swaps_or_assignments: int = 0
    time_taken_ms: float = 0.0


def _get_key_extractor(metric: str) -> Callable[[Parcel], float]:
    """Returns a lambda extracting key based on sorting metric."""
    if metric == "deadline":
        # Earliest deadline first (Ascending)
        return lambda p: p.deadline_hour
    elif metric == "priority":
        # Highest value first (Descending, so negate for standard ascending sorter)
        return lambda p: -float(p.value)
    elif metric == "priority_ratio":
        # Highest priority ratio first (Descending)
        return lambda p: -p.priority_ratio
    elif metric == "weight":
        return lambda p: p.weight_kg
    else:
        raise ValueError(f"Unknown metric '{metric}'. Expected 'deadline', 'priority', or 'priority_ratio'.")


# ==========================================
# 1. MERGE SORT IMPLEMENTATION
# ==========================================
def merge_sort_parcels(parcels: List[Parcel], metric: str = "priority_ratio") -> Tuple[List[Parcel], SortMetrics]:
    """
    Sorts a list of Parcels using Divide-and-Conquer Merge Sort.
    Stable sort with O(n log n) time complexity.
    """
    metrics = SortMetrics()
    key_func = _get_key_extractor(metric)
    arr = copy.copy(parcels)

    def _merge_sort_recursive(items: List[Parcel]) -> List[Parcel]:
        if len(items) <= 1:
            return items

        mid = len(items) // 2
        left_half = _merge_sort_recursive(items[:mid])
        right_half = _merge_sort_recursive(items[mid:])

        return _merge(left_half, right_half)

    def _merge(left: List[Parcel], right: List[Parcel]) -> List[Parcel]:
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            metrics.comparisons += 1
            if key_func(left[i]) <= key_func(right[j]):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
            metrics.swaps_or_assignments += 1

        while i < len(left):
            merged.append(left[i])
            i += 1
            metrics.swaps_or_assignments += 1

        while j < len(right):
            merged.append(right[j])
            j += 1
            metrics.swaps_or_assignments += 1

        return merged

    sorted_list = _merge_sort_recursive(arr)
    return sorted_list, metrics


# ==========================================
# 2. QUICK SORT IMPLEMENTATION
# ==========================================
def quick_sort_parcels(parcels: List[Parcel], metric: str = "priority_ratio") -> Tuple[List[Parcel], SortMetrics]:
    """
    Sorts a list of Parcels using In-Place Quick Sort with Median-of-Three pivot selection.
    Average O(n log n) time complexity.
    """
    metrics = SortMetrics()
    key_func = _get_key_extractor(metric)
    arr = copy.copy(parcels)

    def _median_of_three(low: int, high: int):
        mid = (low + high) // 2
        # Sort low, mid, high
        if key_func(arr[low]) > key_func(arr[mid]):
            arr[low], arr[mid] = arr[mid], arr[low]
            metrics.swaps_or_assignments += 1
        metrics.comparisons += 1

        if key_func(arr[low]) > key_func(arr[high]):
            arr[low], arr[high] = arr[high], arr[low]
            metrics.swaps_or_assignments += 1
        metrics.comparisons += 1

        if key_func(arr[mid]) > key_func(arr[high]):
            arr[mid], arr[high] = arr[high], arr[mid]
            metrics.swaps_or_assignments += 1
        metrics.comparisons += 1

        # Place pivot at high - 1
        arr[mid], arr[high - 1] = arr[high - 1], arr[mid]
        metrics.swaps_or_assignments += 1
        return high - 1

    def _partition(low: int, high: int) -> int:
        if high - low >= 3:
            pivot_idx = _median_of_three(low, high)
            pivot_val = key_func(arr[pivot_idx])
            i = low
            j = high - 1
            while True:
                i += 1
                while key_func(arr[i]) < pivot_val:
                    metrics.comparisons += 1
                    i += 1
                metrics.comparisons += 1

                j -= 1
                while key_func(arr[j]) > pivot_val:
                    metrics.comparisons += 1
                    j -= 1
                metrics.comparisons += 1

                if i >= j:
                    break
                arr[i], arr[j] = arr[j], arr[i]
                metrics.swaps_or_assignments += 1

            arr[i], arr[high - 1] = arr[high - 1], arr[i]
            metrics.swaps_or_assignments += 1
            return i
        else:
            # Simple Lomuto partitioning for small subarrays
            pivot = key_func(arr[high])
            i = low - 1
            for j in range(low, high):
                metrics.comparisons += 1
                if key_func(arr[j]) <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    metrics.swaps_or_assignments += 1
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            metrics.swaps_or_assignments += 1
            return i + 1

    def _quick_sort_recursive(low: int, high: int):
        if low < high:
            p_idx = _partition(low, high)
            _quick_sort_recursive(low, p_idx - 1)
            _quick_sort_recursive(p_idx + 1, high)

    if arr:
        _quick_sort_recursive(0, len(arr) - 1)

    return arr, metrics
