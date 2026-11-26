"""
System Configuration & Constants for Mini-Courier Planner
ETCCDA302: Design & Analysis of Algorithms Capstone
K.R. Mangalam University
"""

# Default Vehicle Constraints
DEFAULT_VEHICLE_CAPACITY_KG = 25.0  # Maximum weight capacity in kg
DEFAULT_TIME_WINDOW_HOURS = 8.0     # Delivery shift duration in hours
AVERAGE_VEHICLE_SPEED_KMH = 30.0    # Urban delivery average speed in km/h

# Algorithm Configuration
SORTING_ALGORITHMS = ["mergesort", "quicksort"]
DEFAULT_SORT_METRIC = "priority_ratio"  # Options: 'priority', 'deadline', 'priority_ratio'

# Benchmarking Settings
BENCHMARK_SIZES = [10, 50, 100, 250, 500, 1000]
BENCHMARK_REPETITIONS = 5

# Formatting
TERMINAL_WIDTH = 80
