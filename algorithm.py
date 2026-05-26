from data import Network, Zone_type, Zone_function
import heapq


class Solver:
    """Class to solve the maze"""
    def __init__(self, network: Network) -> None:
        self.network = network
        self.graph = self.compute_graph(network)

    @staticmethod
    def compute_graph(network: Network) -> dict[str, list[tuple[str, float]]]:
        names = []
        graph = {}
        for hub in network.hubs:
            if hub.zone_type == Zone_type.NORMAL:
                cost = 1.0
            elif hub.zone_type == Zone_type.RESTRICTED:
                cost = 2.0
            elif hub.zone_type == Zone_type.PRIORITY:
                cost = 0.5
            else:
                cost = float("inf")
            names.append((hub.name, cost))
        options: list[tuple[str, float]] = []
        for name, _ in names:
            for connection in network.connections:
                name1, name2 = connection.hubs
                if name1 == name:
                    options.extend(
                        (name, cost)
                        for name, cost in names
                        if name == name2
                        )
                elif name2 == name:
                    options.extend(
                        (name, cost)
                        for name, cost in names
                        if name == name1
                        )
            graph[name] = options
            options = []
        return graph

    @staticmethod
    def get_path(
        came_from: dict[str, str],
        start: str,
        goal: str
    ) -> list[str]:
        path = []
        current = goal
        while True:
            path.append(current)
            if current == start:
                return path[::-1]
            current = came_from[current]

    def solve(
        self, start: str,
        goal: str
    ) -> list[str]:
        """dijkistra path finding algorithm"""
        open_set: list[tuple[float, int, str]] = []
        came_from: dict[str, str] = {}
        closed_set = set()
        g_score = {start: 0.0}
        counter = 0
        heapq.heappush(
            open_set,
            (g_score[start], counter, start)
        )
        counter += 1
        while open_set:
            _, _, current = heapq.heappop(open_set)
            if current in closed_set:
                continue
            if current == goal:
                return self.get_path(came_from, start, goal)
            closed_set.add(current)
            neighbors = self.graph[current]
            for name, cost in neighbors:
                if name in closed_set:
                    continue
                tentative_g = g_score[current] + cost
                if tentative_g < g_score.get(name, float("inf")):
                    came_from[name] = current
                    g_score[name] = tentative_g
                    heapq.heappush(open_set, (tentative_g, counter, name))
                    counter += 1
        return self.get_path(came_from, start, goal)

    def solve_map(self) -> list[str]:
        for hub in self.network.hubs:
            if hub.function == Zone_function.START:
                start = hub.name
            elif hub.function == Zone_function.END:
                end = hub.name
        return self.solve(start, end)
