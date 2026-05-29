from data import Network, Zone_type, Zone_function
import heapq


class Algorithm:
    def __init__(self, network: Network) -> None:
        self.network = network
        self.graph = self.compute_graph(network)

    def get_coordinates(self):
        coordinates = {}
        for hub in self.network.hubs:
            coordinates[hub.name] = (hub.coord_x, hub.coord_y)
        return coordinates

    @staticmethod
    def find_zone_type(network: Network, zone_name: str) -> Zone_type:
        for hub in network.hubs:
            if hub.name == zone_name:
                return hub.zone_type
        return Zone_type.NORMAL

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
    def get_next_hub(
        came_from: dict[str, str],
        start: str,
        goal: str
    ) -> str:
        path: list[str] = []
        current = goal
        if start == goal:
            return start
        while True:
            if current == start:
                return path[-1]
            path.append(current)
            current = came_from[current]

    def dijkistra(
        self, start: str,
        goal: str,
        full_hubs: list[str]
    ) -> str:
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
                return self.get_next_hub(came_from, start, goal)
            closed_set.add(current)
            neighbors = self.graph[current]
            for name, cost in neighbors:
                if name in closed_set:
                    continue
                if name in full_hubs:
                    continue
                tentative_g = g_score[current] + cost
                if tentative_g < g_score.get(name, float("inf")):
                    came_from[name] = current
                    g_score[name] = tentative_g
                    heapq.heappush(open_set, (tentative_g, counter, name))
                    counter += 1
        return self.get_next_hub(came_from, start, current)

    def drones_arrived(self, end: str) -> bool:
        drones = self.network.drones
        for i in range(self.network.nb_drones):
            if drones[i].current_hub != end:
                return False
        return True

    def get_max_drones(self, name: str) -> int:
        hubs = self.network.hubs
        for hub in hubs:
            if hub.name == name:
                return hub.max_drones
        return 1

    def get_full_hubs(self, start: str) -> list[str]:
        drones = self.network.drones
        occupied = []
        full_hubs = []
        for i in range(self.network.nb_drones):
            if drones[i].current_hub != start:
                occupied.append(drones[i].current_hub)
        counts: dict[str, int] = {}
        for hub in occupied:
            if hub in counts:
                counts[hub] += 1
            else:
                counts[hub] = 1
        for hub, count in counts.items():
            max_drones = self.get_max_drones(hub)
            if count == max_drones:
                full_hubs.append(hub)
        return full_hubs

    def get_full_connections(self, start: str) -> list[str]:
        drones = self.network.drones
        occupied = []
        full_hubs = []
        for i in range(self.network.nb_drones):
            if drones[i].current_hub != start:
                occupied.append(drones[i].current_hub)
        counts: dict[str, int] = {}
        for hub in occupied:
            if hub in counts:
                counts[hub] += 1
            else:
                counts[hub] = 1
        for hub, count in counts.items():
            max_drones = self.get_max_drones(hub)
            if count == max_drones:
                full_hubs.append(hub)
        return full_hubs

    def run_drone(self, i: int, start: str, end: str) -> None:
        drone = self.network.drones[i]
        coordinates = self.get_coordinates()
        drone.t += 1
        if drone.wait_turn > 0:
            drone.wait_turn -= 1
            drone.path.append(coordinates[drone.current_hub])
            return
        if drone.current_hub != end:
            full_hubs = self.get_full_hubs(start)
            if drone.current_hub != start:
                full_hubs.append(start)
            next_hub = self.dijkistra(drone.current_hub, end, full_hubs)
            drone.current_hub = next_hub
            if (self.find_zone_type(self.network, next_hub) == Zone_type.RESTRICTED):
                drone.wait_turn = 1
        drone.path.append(coordinates[drone.current_hub])
        # print(f"Drone {drone.id}: {drone.current_hub}")

    def solve_map(self) -> None:
        for hub in self.network.hubs:
            if hub.function == Zone_function.START:
                start = hub.name
            elif hub.function == Zone_function.END:
                end = hub.name
        drones = self.network.drones
        coordinates = self.get_coordinates()
        # print(f"t = {drones[0].t}")
        for i in range(self.network.nb_drones):
            # print(f"Drone {drones[i].id}: {drones[i].current_hub}")
            drones[i].path.append(coordinates[drones[i].current_hub])
            drones[i].t += 1
        while not self.drones_arrived(end):
            # print(f"t = {drones[0].t}")
            for i in range(self.network.nb_drones):
                self.run_drone(i, start, end)
