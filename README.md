# Mini-Courier Planner: Intelligent Logistics and Route Optimization System

**Course:** Design & Analysis of Algorithms (ETCCDA302) — Capstone Assignment  
**Programme:** B.Tech CSE & Specializations  
**Institution:** K.R. Mangalam University, Gurugram, Haryana  
**Faculty Evaluator:** Dr. Shweta Agarwal  
**Student Name:** Mohit Sharma  
**Roll Number / PRN:** 2501010091  
**Maximum Marks:** 100 Marks (Scaled down to 10 marks for final evaluation)  
**Course Outcomes (COs):** CO1, CO2, CO3, CO4 | **Bloom's Level:** L5 (Create / Evaluate)  
**Submission Mode:** Zosima Platform / GitHub Repository Link  

---

## 📌 Executive Summary

The **Mini-Courier Planner** is an integrated algorithmic solution to urban last-mile delivery challenges. Given an incoming pool of customer parcels with varying weights, urgency deadlines, and priorities, along with a realistic urban road network:
1. **Prioritizes** parcels using Divide-and-Conquer sorting algorithms (**Merge Sort** and **Quick Sort**).
2. **Optimizes vehicle box filling** under vehicle weight payload constraints ($W = 25.0\text{ kg}$) using **0/1 Knapsack Dynamic Programming**.
3. **Calculates all-pairs shortest paths** on an urban road network via **Dijkstra's Algorithm (Min-Heap)**.
4. **Constructs an efficient delivery tour** starting and ending at the Central Depot using **Nearest Neighbor TSP Approximation** coupled with **2-Opt Local Search Refinement**.
5. **Benchmarks system scalability** across input sizes from $N = 10$ to $N = 1000$ parcels, producing empirical performance tables, terminal ASCII plots, publication-grade SVG vector charts, and an interactive HTML report dashboard with **zero external dependencies**.

---

## 🚀 Quick Execution Guide

The program is implemented in pure Python (Python 3.8+) using standard libraries. It requires **no third-party dependencies** (no `pip install` required), guaranteeing clean execution on any offline evaluation sandbox or grading system (such as Zosima).

### Commands to Run:
```bash
# 1. Run the complete end-to-end 5-phase pipeline + scalability benchmark
python main.py --all

# 2. Run individual phases selectively:
python main.py --phase 1    # Phase 1: Problem Design & Road Graph Topology
python main.py --phase 2    # Phase 2: Sorting Comparison & 0/1 Knapsack DP Packing
python main.py --phase 3    # Phase 3: Dijkstra Shortest Paths & 2-Opt TSP Tour
python main.py --phase 4    # Phase 4: Performance Testing & Scalability Benchmarks

# 3. Run only the performance benchmarking suite
python main.py --benchmark
```

---

## 📂 Project Structure & Architecture

```
mini-courier-planner/
│
├── main.py                         # Interactive CLI entry point and full pipeline runner
├── config.py                       # Simulation parameters (vehicle payload, speed, thresholds)
├── README.md                       # Complete submission documentation & execution guide
│
├── algorithms/                     # Core algorithmic modules (CO1, CO2, CO3, CO4)
│   ├── __init__.py
│   ├── sorting.py                  # Merge Sort & Quick Sort with operation counters
│   ├── knapsack.py                 # 0/1 Knapsack DP with tabulation snippet & backtracking
│   ├── dijkstra.py                 # Dijkstra Single-Source & All-Pairs Shortest Path (Min-Heap)
│   └── tsp_solver.py               # Nearest Neighbor TSP Heuristic + 2-Opt Local Search
│
├── models/                         # Object-oriented domain data models
│   ├── __init__.py
│   ├── parcel.py                   # Parcel class (ID, weight, value, deadline, priority ratio)
│   ├── delivery_point.py           # DeliveryPoint node class (Cartesian coords, Euclidean metrics)
│   └── graph.py                    # Road Network Graph using Adjacency List representation
│
├── data/                           # Standardized test scenarios and generator
│   ├── __init__.py
│   ├── sample_data.py              # Realistic Gurugram NCR 10-node road network & 10 sample parcels
│   └── generator.py                # Synthetic dataset generator for scalable testing (N=10 to 1000)
│
├── benchmark/                      # Performance profiling & visual artifact generators
│   ├── __init__.py
│   ├── benchmark_runner.py         # Multi-size scalability profiler (N = 10, 50, 100, 250, 500, 1000)
│   ├── visualizer.py               # Terminal ASCII plots, SVG vector charts, and HTML dashboard
│   ├── runtime_chart.svg           # Generated publication-quality SVG scaling chart
│   └── benchmark_report.html       # Standalone interactive HTML dashboard
│
└── report/
    └── CAPSTONE_REPORT.md          # Comprehensive formal academic report with Viva Voce guide
```

---

## 📋 Detailed Walkthrough of Assignment Phases

### Phase 1: Courier Problem Design and Planning (20 Marks)
- **Problem Formulation:**
  - One central distribution warehouse (Depot situated at Node 0) serves customer delivery zones across the city.
  - A fleet vehicle has strict maximum cargo capacity: $W = 25.0\text{ kg}$.
  - Shift time constraint: $T_{\max} = 8.0\text{ hours}$ at an average urban speed of $30\text{ km/h}$.
- **Data Model Specifications:**
  - **Parcel Attributes:** `parcel_id`, `recipient_name`, `destination_node_id`, `weight_kg`, `value`, `deadline_hour`, and `priority_ratio`.
  - **Composite Priority Metric:**
    $$\text{Priority Ratio} = \frac{\text{Value}}{\max(0.5, \text{Deadline}) \cdot \max(0.1, \text{Weight})}$$
  - **Graph Representation:** Weighted undirected graph stored as an **Adjacency List** ($O(V + E)$ space complexity), reflecting sparse real-world city road layouts.
- **Urban Map Layout (Gurugram NCR Delivery Hub):**
  - Node 0: Central Courier Hub (Depot)
  - Nodes 1–9: Cyber City, Sector 29, Golf Course Road, Sohna Road, MG Road, Udyog Vihar, Ambience Mall, South City I, and K.R. Mangalam Campus Zone.

---

### Phase 2: Package Prioritization and Box Filling (20 Marks)
- **Sorting Algorithms Implemented:**
  1. **Merge Sort:** Divide-and-Conquer paradigm. Guarantees $O(N \log N)$ worst-case time, stable sorting (preserves original order for identical priorities), and requires $O(N)$ auxiliary memory.
  2. **Quick Sort:** In-place partitioning with Median-of-Three pivot selection to prevent worst-case $O(N^2)$ on pre-sorted data.
- **Empirical Operations Count ($N = 10$ Parcels):**
  - Merge Sort: 23 comparisons, 34 element assignments.
  - Quick Sort: 28 comparisons, 16 element swaps.
- **0/1 Knapsack Dynamic Programming Formulation:**
  - Recurrence relation for table $DP[i][w]$ (maximum value using first $i$ items with capacity $w$):
    $$DP[i][w] = \begin{cases} 
    DP[i-1][w] & \text{if } w_i > w \\ 
    \max(DP[i-1][w], \; DP[i-1][w - w_i] + v_i) & \text{if } w_i \le w 
    \end{cases}$$
- **Submission Evidence (DP Table Snippet):**
  ```text
  DP Table Snippet: dp[item_idx][capacity_units]
  Item \ W |    0    1    2    3    4    5    6    7    8    9   10   11   12
  ---------------------------------------------------------------------------
    i=0   |    0    0    0    0    0    0    0    0    0    0    0    0    0
    i=1   |    0    0    0    0    0    0    0    0    0    0    0    0    0
    i=2   |    0    0    0    0    0    0    0    0    0    0    0    0    0
    i=3   |    0    0    0    0    0    0    0    0    0    0    0    0    0
    ... (Table continues up to 10 items and 250 capacity units)
  ```
- **Optimal Packing Results:**
  - Selected 6 parcels: `P108`, `P103` (Urgent Medical Supplies), `P101`, `P106`, `P104`, and `P110`.
  - Total Packed Weight: **$24.70\text{ kg} / 25.0\text{ kg}$ ($98.8\%$ capacity utilized)**.
  - Total Accumulated Value: **$505\text{ points}$**.

---

### Phase 3: Route Maker and Graph Processing (20 Marks)
- **Shortest Path Computation (Dijkstra's Algorithm):**
  - Uses a Binary Min-Heap Priority Queue (`heapq`).
  - Time Complexity: $O((V + E) \log V)$ per source node.
  - Computes all-pairs shortest distances between the Depot and all customer nodes holding loaded parcels.
- **Traveling Salesperson Problem (TSP) Tour Formulation:**
  1. **Nearest-Neighbor (NN) Approximation:**
     - Starts at Depot (Node 0), iteratively visits the closest unvisited delivery node, and returns to Depot.
     - Greedy $O(K^2)$ time complexity for $K$ delivery locations.
     - Initial Tour: `0 -> 4 -> 8 -> 3 -> 1 -> 6 -> 0` ($25.50\text{ km}$).
  2. **2-Opt Local Search Heuristic:**
     - Iteratively tests pairwise edge swaps to untangle crossing paths and guarantee local tour optimality.
     - Final Tour Sequence: `Depot (0) -> Sohna Road (4) -> South City I (8) -> Golf Course (3) -> Cyber City (1) -> Udyog Vihar (6) -> Depot (0)`.
     - Final Tour Distance: **$25.50\text{ km}$**.
     - Estimated Delivery & Service Duration: **$76.0\text{ minutes}$** (well within the 8-hour shift ceiling).

---

### Phase 4: Performance Testing and Scalability Benchmark (20 Marks)
The system was benchmarked across multi-scale synthetic datasets scaling from $N = 10$ to $N = 1000$ parcels across expanding road graphs:

| Dataset Size ($N$) | Road Nodes ($V$) | Merge Sort (ms) | Quick Sort (ms) | 0/1 Knapsack DP (ms) | Dijkstra (ms) | TSP (NN+2Opt) (ms) | Total Pipeline (ms) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **10** | 10 | 0.045 ms | 0.034 ms | 0.255 ms | 0.174 ms | 0.045 ms | **0.520 ms** |
| **50** | 10 | 0.151 ms | 0.104 ms | 1.314 ms | 0.162 ms | 0.043 ms | **1.671 ms** |
| **100** | 10 | 0.248 ms | 0.174 ms | 2.281 ms | 0.172 ms | 0.093 ms | **2.794 ms** |
| **250** | 25 | 0.718 ms | 0.685 ms | 5.764 ms | 0.792 ms | 0.137 ms | **7.412 ms** |
| **500** | 50 | 1.641 ms | 1.055 ms | 11.495 ms | 2.681 ms | 1.342 ms | **17.159 ms** |
| **1000** | 50 | 3.838 ms | 2.493 ms | 24.936 ms | 6.145 ms | 0.938 ms | **35.857 ms** |

#### Terminal ASCII Benchmark Chart Output:
```text
===========================================================================
  PERFORMANCE BENCHMARK CHART: Total Pipeline Execution Time (ms)
===========================================================================
  N=10    | ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ |    0.520 ms
  N=50    | █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ |    1.671 ms
  N=100   | ███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ |    2.794 ms
  N=250   | ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ |    7.412 ms
  N=500   | ███████████████████░░░░░░░░░░░░░░░░░░░░░ |   17.159 ms
  N=1000  | ████████████████████████████████████████ |   35.857 ms
===========================================================================
```

#### Generated Visual Artifacts:
- **Scalable Vector Graphic (SVG):** `benchmark/runtime_chart.svg`
- **Interactive HTML Report Dashboard:** `benchmark/benchmark_report.html`

---

### Phase 5: Demonstration & Viva Voce Preparation Guide (20 Marks)

#### Viva Question 1: What is the time and space complexity of each component in your pipeline?
> **Answer:**
> - **Merge Sort:** $O(N \log N)$ time in all cases (worst, average, best), $O(N)$ auxiliary space.
> - **0/1 Knapsack DP:** $O(N \cdot W)$ time and $O(N \cdot W)$ space (pseudo-polynomial), where $N$ is the number of parcels and $W$ is the discrete vehicle capacity units.
> - **Dijkstra's Algorithm:** $O((V + E) \log V)$ time using a binary min-heap, $O(V)$ space for distance and predecessor tables.
> - **Nearest-Neighbor TSP + 2-Opt:** Nearest Neighbor takes $O(K^2)$ where $K$ is the number of delivery stops. 2-Opt local search refinement takes $O(\text{iterations} \cdot K^2)$ time and $O(K)$ space.

#### Viva Question 2: Why cannot we use the Greedy Fractional Knapsack approach for courier parcels?
> **Answer:**
> The Greedy strategy (sorting by value-to-weight ratio $v_i / w_i$) works only when items can be divided into fractions (Fractional Knapsack). In courier delivery, packages cannot be physically partitioned; a parcel is either loaded in full or left for a later trip (0/1 constraint). Greedy selection can leave unutilized capacity gaps that prevent loading higher-value combinations, leading to suboptimal solutions. Dynamic Programming explores overlapping subproblems and guarantees global optimality.

#### Viva Question 3: Why is 0/1 Knapsack called a "pseudo-polynomial" algorithm?
> **Answer:**
> An algorithm is strictly polynomial if its running time is bounded by a polynomial in the length of the input in *bits*. For capacity $W$, the number of bits required to store $W$ is $\beta = \lceil \log_2(W) \rceil$. Therefore, $W = 2^\beta$. Since the runtime $O(N \cdot W) = O(N \cdot 2^\beta)$ is exponential with respect to the input bit-length $\beta$, it is classified as pseudo-polynomial.

#### Viva Question 4: Why was Dijkstra's algorithm chosen over Bellman-Ford or Floyd-Warshall?
> **Answer:**
> Real-world road distances are strictly non-negative ($\omega(u, v) > 0$). Bellman-Ford ($O(V \cdot E)$) is designed to handle negative edge weights, which never occur in physical maps. Floyd-Warshall ($O(V^3)$) computes shortest paths between every pair of vertices in the whole network, whereas we only need shortest paths between the Depot and the small subset of customer nodes $K \ll V$ receiving parcels. Running Dijkstra $K$ times with a Min-Heap takes $O(K(V + E)\log V)$, which is vastly faster on sparse graphs.

---

## 💻 Sample Program Output Trace

```text
================================================================================
   K.R. MANGALAM UNIVERSITY - SCHOOL OF ENGINEERING & TECHNOLOGY
   CAPSTONE ASSIGNMENT: MINI-COURIER PLANNER (ETCCDA302: DAA)
   Integrated Algorithm System: Sorting | Knapsack DP | Dijkstra | TSP
================================================================================

PHASE 1: COURIER PROBLEM DESIGN AND PLANNING
Total Nodes: 10 (Depot: Node 0, Customers: Nodes 1-9) | Total Edges: 15
Vehicle Capacity Limit: 25.0 kg | Urban Speed: 30 km/h

PHASE 2: PACKAGE PRIORITIZATION AND BOX FILLING
Merge Sort: 23 comparisons, 34 assignments
0/1 Knapsack DP: Loaded 6 parcels | Total Weight: 24.70 kg (98.8% utilized) | Total Value: 505

PHASE 3: ROUTE MAKER AND GRAPH PROCESSING
Shortest Paths computed from Depot (Node 0) to all customer stops.
Nearest-Neighbor Tour : 0 -> 4 -> 8 -> 3 -> 1 -> 6 -> 0 (25.50 km)
2-Opt Refined Tour    : 0 -> 4 -> 8 -> 3 -> 1 -> 6 -> 0 (25.50 km, Verified Locally Optimal)
Estimated Trip Time   : 76.0 minutes (46.0 min driving + 30.0 min customer service)

PHASE 4: PERFORMANCE BENCHMARKING (N = 10 to 1000)
Completed execution across 6 scales in 82.73 ms.
Exported runtime_chart.svg and benchmark_report.html successfully.
```

---

## 👨‍💻 Submission Verification Checklist

- [x] Implemented in Python with clean, modular, and readable code.
- [x] Phase 1: Problem design, parcel schema, and adjacency graph format documented.
- [x] Phase 2: Priority sorting (Merge Sort) and 0/1 Knapsack DP packing implemented with DP table evidence.
- [x] Phase 3: Customer graph, Dijkstra shortest paths, and TSP route planner with 2-Opt local search implemented.
- [x] Phase 4: Small and large synthetic datasets evaluated ($N=10$ to $1000$), runtime recorded, and SVG/HTML charts generated.
- [x] Phase 5: Complete documentation, output traces, complexity proofs, and Viva Voce questions provided.
- [x] Zero third-party dependencies required; runs offline on Zosima.
