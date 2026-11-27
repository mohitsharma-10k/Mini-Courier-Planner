# Mini-Courier Planner

An Integrated Parcel Selection and Delivery Route Planning System  
**Design and Analysis of Algorithms — Capstone Project**

---

### Project & Submission Details

- **Student Name:** Mohit Sharma
- **Roll Number:** 2501010091
- **Programme / Section:** B.Tech CSE Core (Section D)
- **University:** K.R. Mangalam University
- **Faculty In-Charge:** Ruchika Bhakhar


---

## 1. Project Overview

**Mini-Courier Planner** is a Python application that integrates sorting, dynamic programming, graph algorithms, and approximation techniques to solve last-mile courier delivery planning. 

Given a pool of customer parcels, a vehicle payload capacity ($W = 25\text{ kg}$), and a road network:
1. **Parcel Prioritization:** Ranks incoming parcels using comparison-based sorting based on priority score, delivery deadline, and unique ID.
2. **Vehicle Load Selection:** Selects the maximum-value feasible subset of parcels that fits strictly within the cargo capacity using **0/1 Knapsack Dynamic Programming**.
3. **Shortest Path Computation:** Calculates exact shortest paths and distances across the road network from the central depot using **Dijkstra's Algorithm** with a binary min-heap.
4. **Delivery Tour Construction:** Generates an efficient delivery route visiting all selected customer destinations and returning to the depot using the **Nearest-Neighbor TSP Heuristic** and **2-Opt local search refinement**.
5. **Runtime Benchmarking:** Profiles algorithm scaling from $N = 10$ to $N = 1000$ parcels with automated ASCII charts, SVG charts, and interactive HTML dashboards.

The application relies strictly on Python standard libraries and requires **zero external packages**.

---

## 2. Quick Execution Guide

Run commands from the project root directory:

```bash
# 1. Run the complete end-to-end delivery pipeline
python main.py --all

# 2. Run individual pipeline stages:
python main.py --phase 1    # Problem formulation & road graph topology
python main.py --phase 2    # Parcel sorting & 0/1 Knapsack DP packing
python main.py --phase 3    # Dijkstra shortest paths & TSP tour construction
python main.py --phase 4    # Performance testing & scalability benchmarks

# 3. Run only the performance benchmarking suite
python main.py --benchmark
```

---

## 3. Project Architecture

```
Mini-Courier-Planner(daa)/
│
├── main.py                         # CLI entry point and pipeline runner
├── config.py                       # Simulation parameters (vehicle payload, speed)
├── README.md                       # Project documentation and execution guide
│
├── algorithms/                     # Core algorithmic implementations
│   ├── sorting.py                  # Merge Sort & Quick Sort with operation counters
│   ├── knapsack.py                 # 0/1 Knapsack DP with tabulation & backtracking
│   ├── dijkstra.py                 # Dijkstra shortest paths using min-heap priority queue
│   └── tsp_solver.py               # Nearest Neighbor TSP Heuristic + 2-Opt local search
│
├── models/                         # Object-oriented domain models
│   ├── parcel.py                   # Parcel entity (ID, weight, value, deadline, priority)
│   ├── delivery_point.py           # Delivery point graph node (coordinates, metadata)
│   └── graph.py                    # Road network graph using Adjacency List
│
├── data/                           # Datasets and generator
│   ├── sample_data.py              # Sample 10-node road graph & 10 sample parcels
│   └── generator.py                # Synthetic dataset generator (N = 10 to 1000)
│
├── benchmark/                      # Performance evaluation & visualizations
│   ├── benchmark_runner.py         # Empirical runtime benchmarking across dataset scales
│   ├── visualizer.py               # Terminal ASCII plots, SVG charts, and HTML dashboard
│   ├── runtime_chart.svg           # Scalable vector graphics scaling chart
│   └── benchmark_report.html       # Interactive HTML dashboard
│
└── report/
    ├── CAPSTONE_REPORT.md          # Comprehensive formal academic report
    ├── report.html                 # Complete printable publication-style report
    └── MINI_COURIER_PLANNER_REPORT.pdf # Full 17-page compiled PDF report
```

---

## 4. Algorithmic Components & Complexity

| Component | Algorithmic Technique | Time Complexity | Space Complexity | Rationale |
|:---|:---|:---:|:---:|:---|
| **Prioritization** | Comparison Sorting (Merge / Quick Sort) | $O(N \log N)$ | $O(N)$ | Produces a deterministic, urgency-ordered delivery queue. |
| **Package Selection** | 0/1 Knapsack Dynamic Programming | $O(N \cdot W)$ | $O(N \cdot W)$ | Guarantees global maximum value within vehicle payload capacity limit. |
| **Distance Computation** | Dijkstra's Algorithm (Min-Heap) | $O((V + E) \log V)$ | $O(V + E)$ | Exact shortest road paths for non-negative road segments. |
| **Delivery Tour** | Nearest Neighbor TSP + 2-Opt | $O(K^2)$ | $O(K)$ | Fast polynomial-time tour approximation for NP-hard TSP routing. |

---

## 5. Sample Execution Output

```text
================================================================================
   K.R. MANGALAM UNIVERSITY - SCHOOL OF ENGINEERING & TECHNOLOGY
   CAPSTONE ASSIGNMENT: MINI-COURIER PLANNER (ETCCDA302: DAA)
   Student: Mohit Sharma | Roll No: 2501010091 | Faculty: Ruchika Bhakhar
   Programme / Section: B.Tech CSE Core (Section D)
   Integrated Algorithm System: Sorting | Knapsack DP | Dijkstra | TSP
================================================================================

1. PROBLEM DESIGN:
   Total Nodes: 10 (Depot: Node 0, Customers: Nodes 1-9) | Total Edges: 15
   Vehicle Cargo Payload: 25.0 kg | Urban Travel Speed: 30 km/h

2. PARCEL PRIORITIZATION & BOX FILLING:
   - Merge Sort: 23 comparisons, 34 assignments
   - 0/1 Knapsack DP: Selected 6 optimal parcels (P108, P103, P101, P106, P104, P110)
   - Total Weight Loaded: 24.70 kg / 25.0 kg (98.8% capacity utilization)
   - Maximum Value Accumulated: 505 points

3. ROUTE PLANNING & TSP TOUR:
   - Dijkstra Shortest Paths computed from Depot (Node 0) to all customer stops.
   - Tour Sequence: Depot (0) -> Sohna Road (4) -> South City I (8) -> Golf Course (3) -> Cyber City (1) -> Udyog Vihar (6) -> Depot (0)
   - Total Tour Distance: 25.50 km
   - Estimated Delivery & Service Duration: 76.0 minutes (46.0 min driving + 30.0 min service)

4. BENCHMARK SUMMARY (N = 10 to 1000):
   Scaled smoothly from 0.52 ms (N=10) to 35.86 ms (N=1000).
   Exported benchmark/runtime_chart.svg and benchmark/benchmark_report.html.
```

---

## 6. Generated Reports

- **Formal Academic Report (Markdown):** [report/CAPSTONE_REPORT.md](report/CAPSTONE_REPORT.md)
- **Interactive Printable Report (HTML):** [report/report.html](report/report.html)
- **Compiled PDF Report:** [report/MINI_COURIER_PLANNER_REPORT.pdf](report/MINI_COURIER_PLANNER_REPORT.pdf)
- **Scalability Vector Chart:** [benchmark/runtime_chart.svg](benchmark/runtime_chart.svg)
- **Benchmark Dashboard:** [benchmark/benchmark_report.html](benchmark/benchmark_report.html)
