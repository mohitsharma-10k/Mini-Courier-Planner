# CAPSTONE ASSIGNMENT REPORT
## MINI-COURIER PLANNER: INTELLIGENT LOGISTICS & ROUTE OPTIMIZATION SYSTEM
- **Course**: Design & Analysis of Algorithms (ETCCDA302)
- **Programme**: B.Tech CSE core 
- **Faculty In-Charge**: Dr. Shweta Agarwal
- **Student Name**: Mohit Sharma
- **Roll Number**: 2501010091


---

## TABLE OF CONTENTS
1. [Executive Summary & System Architecture](#1-executive-summary--system-architecture)
2. [Phase 1: Courier Problem Design and Planning (20 Marks)](#2-phase-1-courier-problem-design-and-planning)
3. [Phase 2: Package Prioritization and Box Filling (20 Marks)](#3-phase-2-package-prioritization-and-box-filling)
4. [Phase 3: Route Maker and Graph Processing (20 Marks)](#4-phase-3-route-maker-and-graph-processing)
5. [Phase 4: Performance Testing and Scalability Benchmark (20 Marks)](#5-phase-4-performance-testing-and-scalability-benchmark)
6. [Phase 5: Demonstration, Optimization Analysis & Viva Voce Preparation (20 Marks)](#6-phase-5-demonstration-optimization-analysis--viva-voce-preparation)

---

## 1. EXECUTIVE SUMMARY & SYSTEM ARCHITECTURE

The **Mini-Courier Planner** is an integrated software system designed to automate last-mile delivery operations for an urban logistics company. In urban parcel delivery, courier companies face two fundamental NP-hard and combinatorial optimization challenges simultaneously:
1. **The Vehicle Loading / Box Filling Problem**: Which parcels should be loaded onto a courier delivery van given a strict maximum cargo weight limit ($W$ kg) such that the combined business value, utility, and urgency of delivered packages is maximized?
2. **The Delivery Routing Problem**: In what order should the selected customer locations be visited starting from and returning to the Central Hub (Depot) so that the total travel distance and transit duration are minimized?

### Integrated Pipeline Workflow
```
[ Incoming Parcels Pool ]
          │
          ▼
[ Phase 2A: Priority Sorting ]  ──> Merge Sort / Quick Sort: O(N log N)
          │
          ▼
[ Phase 2B: Vehicle Packing ]   ──> 0/1 Knapsack Dynamic Programming: O(N · W)
          │
     (Selected Subset)
          │
          ▼
[ Phase 3A: Shortest Paths ]    ──> Dijkstra's Algorithm (Min-Heap): O((V + E) log V)
          │
  (All-Pairs Distance Matrix)
          │
          ▼
[ Phase 3B: Route Optimization ]──> Nearest Neighbor Heuristic + 2-Opt Refinement: O(K²)
          │
          ▼
[ Final Turn-by-Turn Delivery Itinerary & Runtime Scaling Analytics ]
```

---

## 2. PHASE 1: COURIER PROBLEM DESIGN AND PLANNING

### 2.1 Problem Definition & Mathematical Constraints
Let the courier delivery depot be situated at node $0$. A set of $N$ incoming customer parcels $\mathcal{P} = \{p_1, p_2, \dots, p_N\}$ arrives at the hub.
Each parcel $p_i$ is characterized by the tuple:
$$p_i = \langle \text{id}_i, \text{recipient}_i, \text{dest}_i, w_i, v_i, d_i \rangle$$
Where:
- $\text{dest}_i \in \mathcal{V}$: Designated delivery node on the city road graph.
- $w_i \in \mathbb{R}^+$: Weight of the parcel in kilograms ($kg$).
- $v_i \in \mathbb{Z}^+$: Priority / revenue / utility score.
- $d_i \in \mathbb{R}^+$: Delivery deadline (hours from shift commencement).

**Vehicle Constraints:**
- Delivery vehicle maximum cargo payload: $W = 25.0\text{ kg}$.
- Fleet operational shift limit: $T_{\max} = 8.0\text{ hours}$.
- Average urban speed: $v_{\text{avg}} = 30\text{ km/h}$.

### 2.2 Composite Priority Metric Formulation
To prevent delayed high-value packages, a composite urgency ratio is formulated:
$$\text{Priority Ratio}(p_i) = \frac{v_i}{\max(0.5, d_i) \cdot \max(0.1, w_i)}$$
This favors parcels with high value, tight deadlines, and lightweight profiles.

### 2.3 Road Network Graph Representation
The city road network is modeled as a weighted undirected graph $G = (\mathcal{V}, \mathcal{E}, \omega)$, where:
- $\mathcal{V}$: Set of physical locations (Depot + Customer delivery nodes).
- $\mathcal{E}$: Set of bidirectional road segments.
- $\omega(u, v)$: Shortest physical road distance between $u$ and $v$ in kilometers.

An **Adjacency List** data structure is chosen over an Adjacency Matrix because urban road networks are sparse ($|\mathcal{E}| \ll |\mathcal{V}|^2$), providing:
- Space Complexity: $O(V + E)$ compared to $O(V^2)$ for matrix.
- Dijkstra Neighbor Traversal: $O(E)$ total edge relaxations instead of $O(V^2)$.

---

## 3. PHASE 2: PACKAGE PRIORITIZATION AND BOX FILLING

### 3.1 Sorting Algorithms Implementation & Comparison
Two distinct sorting paradigms were implemented and evaluated to rank parcels:
1. **Merge Sort**: Divide-and-Conquer paradigm. Guarantees $O(N \log N)$ worst-case time complexity, stable ordering, with $O(N)$ auxiliary memory.
2. **Quick Sort**: Partitioning with Median-of-Three pivot selection to avoid worst-case $O(N^2)$ on pre-sorted inputs. In-place memory $O(\log N)$.

#### Empirical Operations Count (Sample N = 10 Parcels):
- **Merge Sort**: 23 comparisons, 34 element assignments.
- **Quick Sort**: 28 comparisons, 16 element swaps.

*Conclusion*: Merge Sort provides strict deterministic timing guarantees crucial for real-time logistics schedules.

### 3.2 0/1 Knapsack Dynamic Programming
Parcels cannot be divided (0/1 constraint). The optimal selection is formulated as:
$$\text{Maximize } \sum_{i \in \mathcal{S}} v_i \quad \text{subject to} \quad \sum_{i \in \mathcal{S}} w_i \le W$$

#### Recurrence Relation:
Let $DP[i][w]$ represent the maximum value achievable considering the first $i$ parcels with available capacity $w$:
$$DP[i][w] = \begin{cases} 
DP[i-1][w] & \text{if } w_i > w \\ 
\max\left(DP[i-1][w], \; DP[i-1][w - w_i] + v_i\right) & \text{if } w_i \le w 
\end{cases}$$
Base Case: $DP[0][w] = 0$ for all $w \in [0, W]$, and $DP[i][0] = 0$.

#### Evidence: 0/1 Knapsack DP Table Snippet
Below is the actual DP table snippet generated by `algorithms/knapsack.py` for capacity discrete steps (hectograms = 0.1 kg):

```text
Item \ W |    0    1    2    3    4    5    6    7    8    9   10   11
----------------------------------------------------------------------
  i=0    |    0    0    0    0    0    0    0    0    0    0    0    0
  i=1    |    0    0    0    0    0    0    0    0    0    0    0    0
  i=2    |    0    0    0    0    0    0    0    0    0    0    0    0
  i=3    |    0    0    0    0    0    0    0    0    0    0    0    0
  i=4    |    0    0    0    0    0    0    0    0    0    0    0    0
  i=5    |    0    0    0    0    0    0    0    0    0    0    0    0
  ... (Full table computed up to i=10 items and W=250 capacity units)
```

#### Backtracking Reconstruction Output:
From the pool of 10 incoming parcels, the DP engine selected **6 parcels**:
- `P108`: Neha Gupta (Node 8, Wt: 1.5kg, Val: 60)
- `P103`: Rohit Malhotra (Node 3, Wt: 6.0kg, Val: 120) - Urgent Medical Supplies
- `P101`: Aakash Sharma (Node 1, Wt: 3.5kg, Val: 75)
- `P106`: Ananya Rao (Node 6, Wt: 5.5kg, Val: 95)
- `P104`: Sneha Kapoor (Node 4, Wt: 4.2kg, Val: 85)
- `P110`: Pooja Mehta (Node 3, Wt: 4.0kg, Val: 70)

**Packing Metrics**:
- **Total Selected Weight**: $24.70\text{ kg} \le 25.0\text{ kg}$
- **Cargo Utilization**: **$98.8\%$**
- **Total Value Accumulated**: **$505\text{ points}$**

---

## 4. PHASE 3: ROUTE MAKER AND GRAPH PROCESSING

### 4.1 Dijkstra's Shortest Path Algorithm
To route between locations across the real road network, Dijkstra's algorithm with a binary min-heap priority queue was implemented.

#### Complexity:
- Time: $O((V + E) \log V)$
- Space: $O(V)$ for distance and predecessor tables.

#### Shortest Path Tree from Central Depot (Node 0):
| Target Node | Destination Zone | Shortest Dist (km) | Exact Road Path Trajectory |
|---|---|---|---|
| Node 1 | Cyber City Tower A | 5.4 km | Depot(0) $\to$ MG Road(5) $\to$ Cyber City(1) |
| Node 3 | Golf Course Road | 7.3 km | Depot(0) $\to$ Sector 29(2) $\to$ Golf Course(3) |
| Node 4 | Sohna Road Hub | 4.2 km | Depot(0) $\to$ Sohna Road(4) [Direct link] |
| Node 6 | Udyog Vihar Ph-IV | 7.5 km | Depot(0) $\to$ MG Road(5) $\to$ Cyber City(1) $\to$ Udyog Vihar(6) |
| Node 8 | South City I Colony | 7.0 km | Depot(0) $\to$ Sector 29(2) $\to$ South City I(8) |

### 4.2 TSP Delivery Tour Generation
Using the pairwise distance matrix from Dijkstra, the delivery tour visits all customer destinations and returns to Depot.

1. **Nearest Neighbor (NN) Approximation**:
   - Greedy strategy: From current vertex, visit closest unvisited customer.
   - Initial Tour: `0 -> 4 -> 8 -> 3 -> 1 -> 6 -> 0`
   - Initial Tour Distance: **$25.50\text{ km}$**

2. **2-Opt Local Search Heuristic**:
   - Iteratively inspects pairs of edges $(u_1, v_1)$ and $(u_2, v_2)$ to determine if reversing the segment reduces distance.
   - Verified local optimality: Current sequence `0 -> 4 -> 8 -> 3 -> 1 -> 6 -> 0` is already locally optimal with **$25.50\text{ km}$**.
   - Estimated Delivery & Service Duration: **$76.0\text{ minutes}$** (under the 8-hour shift ceiling).

---

## 5. PHASE 4: PERFORMANCE TESTING AND SCALABILITY BENCHMARK

To satisfy the requirements of testing with larger datasets, the system was subjected to an automated benchmark scaling from $N = 10$ to $N = 1000$ parcels on road networks scaling up to 50 nodes.

### 5.1 Empirical Runtime Results Table
| Input Size (N) | Road Nodes (V) | MergeSort (ms) | QuickSort (ms) | 0/1 Knapsack DP (ms) | Dijkstra (ms) | TSP NN+2Opt (ms) | Total Time (ms) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **10** | 10 | 0.045 ms | 0.034 ms | 0.255 ms | 0.174 ms | 0.045 ms | **0.520 ms** |
| **50** | 10 | 0.151 ms | 0.104 ms | 1.314 ms | 0.162 ms | 0.043 ms | **1.671 ms** |
| **100** | 10 | 0.248 ms | 0.174 ms | 2.281 ms | 0.172 ms | 0.093 ms | **2.794 ms** |
| **250** | 25 | 0.718 ms | 0.685 ms | 5.764 ms | 0.792 ms | 0.137 ms | **7.412 ms** |
| **500** | 50 | 1.641 ms | 1.055 ms | 11.495 ms | 2.681 ms | 1.342 ms | **17.159 ms** |
| **1000** | 50 | 3.838 ms | 2.493 ms | 24.936 ms | 6.145 ms | 0.938 ms | **35.857 ms** |

### 5.2 Algorithmic Scalability Analysis
1. **Sorting Scalability**: Both Merge Sort and Quick Sort exhibit empirical $O(N \log N)$ behavior. For $N=1000$, execution completes in under $4\text{ ms}$.
2. **Knapsack DP Scalability**: With capacity $W$ fixed at $250$ units, runtime grows strictly linearly with item count $N$ ($O(N \cdot W)$ pseudo-polynomial). At $N=1000$, DP takes $\approx 25\text{ ms}$.
3. **Graph Algorithms**: Dijkstra scales at $O(K \cdot (V + E)\log V)$ where $K$ is the number of distinct delivery stops. Min-heap keeps lookups lightning fast ($< 7\text{ ms}$ for 50 nodes).

---

## 6. PHASE 5: DEMONSTRATION, OPTIMIZATION ANALYSIS 

### 6.1 Future Optimization Strategies
1. **Branch and Bound for 0/1 Knapsack**: For very large capacity scales ($W > 10^6$), a Branch-and-Bound algorithm pruned with fractional knapsack upper bounds avoids large memory footprints.
2. **A* Search for Road Graphs**: Replace standard Dijkstra with $A^*$ Search using Euclidean distance heuristic $h(u, v) = \|(x_u, y_u) - (x_v, y_v)\|_2$ to direct shortest path explorations towards destinations.
3. **Genetic Algorithms / Simulated Annealing**: For fleet sizes with multiple delivery vans (Capacitated Vehicle Routing Problem - CVRP).

---
---
*Report Prepared for ETCCDA302 Capstone Evaluation | K.R. Mangalam University*
