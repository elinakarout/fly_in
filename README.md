_This project has been created as part of the 42 curriculum by ekarout_

# Fly_In

## Description

Fly_In is a graph-based drone routing and simulation system developed as part of the 42 curriculum.  
Its goal is to simulate and optimize the movement of multiple drones through a constrained network of hubs and connections.

Each hub represents a node in a directed weighted graph, and each connection represents a possible path between hubs.  
The system must compute valid routes while respecting constraints such as hub capacity, link capacity, and dynamic occupancy during simulation.

The project focuses on:
- Efficient path computation in constrained graphs  
- Multi-agent (multi-drone) simulation  
- Real-time constraint handling (capacity and congestion)  
- Turn-based execution of movement  
- Visual representation of the simulation state  

---

## Instructions

### Installation

Clone the repository:
```bash
git clone git@vogsphere.42beirut.com:vogsphere/intra-uuid-91c09e60-5819-4f41-a8a7-29c016580a20-7432156-ekarout
cd fly_in
```
Create a virtual environment and activate it:
```bash
python3 -m venv fly_in
source fly_in/bin/activate
# Check if you're inside the venv:
which python
```

Install dependencies:
```bash
make install
```

### Execution

Run the simulation with makefile:
```bash
make run MAP=EASY1 # translates to maps/easy/01_linear_path.txt

make run MAP=EASY2 # translates to maps/easy/02_simple_fork.txt

make run MAP=EASY3 # translates to maps/easy/03_basic_capacity.txt

make run MAP=MEDIUM1 # translates to /maps/medium/01_dead_end_trap.txt

make run MAP=MEDIUM2 # translates to /maps/medium/02_circular_loop.txt

make run MAP=MEDIUM3 # translates to /maps/medium/03_priority_puzzle.txt

make run MAP=HARD1 # translates to /maps/hard/01_maze_nightmare.txt

make run MAP=HARD2 # translates to /maps/hard/02_capacity_hell.txt

make run MAP=HARD3 # translates to /maps/hard/03_ultimate_challenge.txt

make run MAP=CHALLENGER # translates to maps/challenger/01_the_impossible_dream.txt
```

Run the simulation without makefile:
```bash
python3 main.py <PATH_TO_FILE>
```

---

## Algorithm Choices & Implementation Strategy

### Graph Representation
The network is modeled as a graph:
- Nodes represent hubs
- Edges represent connections between hubs

An adjacency list structure is used for efficient traversal and updates.

---
### Pathfinding (Core Logic)
The routing system is based on **Dijkstra’s algorithm**, used to compute shortest paths from a source hub to a destination hub.

However, the classical algorithm is extended with constraint-aware logic:

#### Hub Capacity Constraint
Each hub has a maximum drone capacity.  
Before committing to a path or moving a drone, the algorithm checks whether the destination hub has available capacity.

If a hub is full, it is treated as temporarily unavailable during path selection.

---

#### Link Capacity Constraint
Each connection between hubs has a maximum throughput capacity.  
The algorithm ensures that no more drones than allowed traverse a link at the same time step.

If a link is saturated, it is skipped during neighbor exploration
---

#### No Backtracking / Dead-End Handling
If a drone reaches a state where:
- No forward move satisfies constraints, and
- No alternative valid path exists,

then the drone remains at its current hub for that turn.

This prevents invalid oscillations and ensures stability in congested scenarios.

---

### Multi-Drone Simulation Model
The simulation runs in discrete time steps (“turns”):

1. Each drone evaluates or updates its path
2. Movement decisions are computed based on current graph state
3. Capacity constraints are validated globally
4. All valid movements are executed simultaneously per turn

This ensures deterministic behavior and avoids ordering bias between drones.

---

### Optimization Strategy
- Graph preprocessing to reduce repeated computations  
- Reuse of computed shortest paths when valid  
- Early termination when destination is reached  
- Avoiding unnecessary recomputation unless constraints change 


## Visual Representation

The project includes a real-time visualization system for debugging and user experience.

### Features
- Hubs displayed as nodes in a coordinate space  
- Connections rendered as edges between hubs  
- Drones represented as moving entities along edges  
- Real-time updates per simulation turn  
- Turn counter displayed on screen  
- Labels for drones (e.g., D1, D2, etc.)  
- Visual feedback of congestion and movement flow  

### User Experience Improvements
- Makes pathfinding behavior observable  
- Helps identify bottlenecks and constraint violations  
- Provides intuitive understanding of multi-agent interactions  
- Enhances debugging of routing and simulation logic  

---

## Resources

### References
- Dijkstra, E. W. (1959). Shortest Path Algorithm  
- https://cp-algorithms.com/graph/dijkstra.html  
- https://docs.python.org/3/library/typing.html  

### AI Usage
AI assistance was used for:
- Debugging Python type issues (e.g., static typing and mypy errors)  
- Structuring documentation in a clear format  
- Improving explanations of simulation decisions  

All AI-generated suggestions were reviewed and adapted to match the actual implementation.

---

## Notes
- The simulation is deterministic under identical inputs  
- Performance depends on graph size and number of active drones  
- Future improvements may include advanced flow algorithms or heuristic routing enhancements  
