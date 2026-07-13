> *This project was created as part of the 42 curriculum by **ekarout***

<div align="center">

# 🚁 Fly_In

**A graph-based drone routing and simulation system**

*Part of the 42 Curriculum*

---

</div>

## Description

**Fly_In** simulates and optimizes the movement of multiple drones through a constrained network of hubs and connections.

Each **hub** is a node in a directed weighted graph. Each **connection** is a possible path between hubs. The system computes valid routes while respecting real-time constraints — hub capacity, link throughput, and dynamic occupancy across simulation turns.

### What it focuses on

- 🗺️ **Efficient path computation** in constrained graphs
- 🤖 **Multi-agent simulation** with simultaneous drone movement
- ⚡ **Real-time constraint handling** — capacity and congestion
- 🔄 **Turn-based execution** with deterministic behavior
- 🖥️ **Visual representation** of the full simulation state

---

## Instructions

### 1. Clone the repository

```bash
git clone git@vogsphere.42beirut.com:vogsphere/intra-uuid-91c09e60-5819-4f41-a8a7-29c016580a20-7432156-ekarout
cd fly_in
```

### 3. Install dependencies

```bash
make install
```

---

## Running the Simulation

### With Make (recommended)

```bash
make run MAP=<MAP_NAME>
```

| Map Name | File Path |
|---|---|
| `EASY1` | `maps/easy/01_linear_path.txt` |
| `EASY2` | `maps/easy/02_simple_fork.txt` |
| `EASY3` | `maps/easy/03_basic_capacity.txt` |
| `MEDIUM1` | `maps/medium/01_dead_end_trap.txt` |
| `MEDIUM2` | `maps/medium/02_circular_loop.txt` |
| `MEDIUM3` | `maps/medium/03_priority_puzzle.txt` |
| `HARD1` | `maps/hard/01_maze_nightmare.txt` |
| `HARD2` | `maps/hard/02_capacity_hell.txt` |
| `HARD3` | `maps/hard/03_ultimate_challenge.txt` |
| `CHALLENGER` | `maps/challenger/01_the_impossible_dream.txt` |

### Without Make

```bash
uv run main.py <PATH_TO_FILE>
```

---

## Algorithm & Design

### Graph Representation

The network is modeled as a directed weighted graph:

- **Nodes** → hubs
- **Edges** → connections between hubs

An **adjacency list** structure is used for efficient traversal and state updates.

---

### Pathfinding

Routing is built on **Dijkstra's algorithm**, extended with constraint-aware logic:

#### Hub Capacity
Each hub has a maximum drone capacity. Before committing to a path, the algorithm checks available capacity. Hubs at capacity are treated as temporarily unavailable.

#### Link Capacity
Each connection has a maximum throughput. If a link is saturated for the current time step, it is skipped during neighbor exploration.

#### Dead-End Handling
If a drone has no valid forward move — and no alternative path satisfies constraints — it remains in place for that turn. This prevents invalid oscillations and ensures stability under congestion.

---

### Multi-Drone Simulation

The simulation runs in discrete **turns**:

1. Each drone evaluates or updates its path
2. Movement decisions are computed against the current graph state
3. Capacity constraints are validated globally
4. All valid movements execute simultaneously

This guarantees deterministic behavior and eliminates ordering bias between drones.

---

### Optimization

- Graph preprocessing to reduce repeated computation
- Reuse of computed shortest paths when still valid
- Early termination upon reaching destination
- Recomputation only triggered when constraints change

---

## Visualization

The project includes a real-time visualization system for debugging and observability.

| Feature | Description |
|---|---|
| 🔵 Nodes | Hubs displayed at their coordinate positions |
| ➡️ Edges | Connections rendered between hubs |
| 🚁 Drones | Moving entities labeled D1, D2, etc. |
| 🔢 Turn Counter | Current simulation step shown on screen |

The visualizer makes pathfinding behavior observable, helps identify bottlenecks, and provides intuitive insight into multi-agent interactions.

---

## Example input

Text file exemple: map.txt at the root

Run:
```bash
python3 main.py map.txt
```

Expected output:
```bash
D1-corridorA D2-hub-roof1 
D1-tunnelB D2-roof1 D3-corridorA 
D1-goal D2-roof2 D3-tunnelB D4-corridorA D5-hub-roof1 
D2-goal D3-goal D4-tunnelB D5-roof1 
D4-goal D5-roof2 
D5-goal 

Total turns: 6!
```

Each line represents a turn, in the format _D\<ID\>-\<zone\>, or D\<ID\>-\<connection\>_

- D\<ID\> refers to the unique drone identifier (e.g., D1, D2).
- \<zone\> is the name of the destination zone.
- \<connection\> is the name of the connection toward a restricted zone.

An arcade window will also start, providing a visual graph representation of drone movements on the map.

---

## Notes

- The simulation is **deterministic** under identical inputs
- Performance scales with graph size and number of active drones
- Future improvements may include advanced flow algorithms or heuristic routing enhancements

---

## Resources

- Dijkstra, E. W. (1959). *A note on two problems in connexion with graphs*
- [cp-algorithms.com — Dijkstra's Algorithm](https://cp-algorithms.com/graph/dijkstra.html)
- [Python `typing` module docs](https://docs.python.org/3/library/typing.html)

### AI Usage

AI assistance was used for debugging Python type issues (static typing and mypy errors), structuring documentation, and explaning visualisation libarry (Arcade). All suggestions were reviewed and adapted to match the actual implementation.