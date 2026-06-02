from data import Network, Zone_type, Zone_function, Drone
import heapq
from pprint import pprint



class Algorithm:
    def __init__(self, network: Network) -> None:
        self.network = network
        self.graph = self.compute_graph(network)
        self.coordinates = self.get_coordinates(network)
        self.hubs_capacity = self.get_hubs_capacity(network)
        self.connections_capacity = self.get_connections_capacity(network)
        self.distances = self.compute_distances()
    
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
    def get_coordinates(network: Network):
        coordinates = {}
        for hub in network.hubs:
            coordinates[hub.name] = (hub.coord_x, hub.coord_y)
        return coordinates

    @staticmethod
    def get_hubs_capacity(network: Network):
        capacity = {}
        for hub in network.hubs:
            if hub.function == Zone_function.START:
                capacity[hub.name] = 0
            else:
                capacity[hub.name] = hub.max_drones
        return capacity
    
    @staticmethod
    def get_connections_capacity(network: Network):
        capacity = {}
        for connection in network.connections:
            capacity[connection.hubs] = connection.max_link_capacity
        return capacity

    @staticmethod
    def get_path(came_from: dict[tuple[int, int], tuple[int, int]],
                start: tuple[int, int], goal: tuple[int, int]) -> list[str]:
        """Find the path from came_from dict"""
        path = []
        current = goal
        while current != start:
            prev = came_from[current]
            path.append(prev)
            current = prev
        return path

    def dijkistra(self, start: str, goal: str) -> list[str]:
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
        return []
    
    def check_restricted(self, to_check: str) -> bool:
        for hub in self.network.hubs:
            if hub.name == to_check:
                return hub.zone_type == Zone_type.RESTRICTED
        return False

    def check_priority(self, to_check: str) -> bool:
        for hub in self.network.hubs:
            if hub.name == to_check:
                return hub.zone_type == Zone_type.PRIORITY
        return False

    def get_cost(self, path: list[str]):
        all_costs = {}
        for hub in self.network.hubs:
            if hub.zone_type == Zone_type.NORMAL:
                cost = 1.0
            elif hub.zone_type == Zone_type.RESTRICTED:
                cost = 2.0
            elif hub.zone_type == Zone_type.PRIORITY:
                cost = 0.5
            else:
                cost = float("inf")
            all_costs[hub.name] = cost
        total_cost = 0.0
        for node in path:
            total_cost += all_costs[node]
        return total_cost

    def compute_distances(self):
        distances = {}
        for hub in self.network.hubs:
            if hub.function == Zone_function.START:
                start = hub.name
            elif hub.function == Zone_function.END:
                end = hub.name
        for node in self.graph:
            if node == end:
                distances_node = 0
            path = self.dijkistra(end, node)
            distances[node] = self.get_cost(path)
        if distances[start] == 0:
            raise ValueError("The map is unsolvable")
        return distances

    def check_hub_change(self, src: str, target: str) -> bool:
        if self.hubs_capacity[target] == 0:
            return False
        if (src == target):
            return True
        connection = tuple(sorted((src, target)))
        if self.connections_capacity[connection] == 0:
            return False
        return True

    def change_hub(self, src: str, target: str) -> None:
        if not self.check_hub_change(src, target):
            return
        self.hubs_capacity[target] -= 1
        self.hubs_capacity[src] += 1
        if (src != target):
            connection = tuple(sorted((src, target)))
            self.connections_capacity[connection] -= 1
    
    def check_best_option(self, drone: Drone, end: str) -> str:
        options = [option for option, cost in self.graph[drone.current_hub]]
        best_option = drone.current_hub
        best_cost = self.distances[drone.current_hub] + 1
        for option in options:
            if (
                option == end
                and self.check_hub_change(drone.current_hub, option)
            ):
                best_cost = 0
                best_option = option
            elif (
                self.check_priority(option)
                and self.check_hub_change(drone.current_hub, option)
                and option != drone.current_hub
                and option != drone.previous_hub
            ):
                print(f"Turn {drone.t}:")
                print(f"{drone.id}: curr: {drone.current_hub} prev: {drone.previous_hub} option {option}")
                best_cost = self.distances[option] - 0.5
                best_option = option
            elif(
                self.distances[option] < best_cost
                and self.check_hub_change(drone.current_hub, option)
            ):
                best_option = option
                best_cost = self.distances[option]
        self.change_hub(drone.current_hub, best_option)
        return best_option

    def run_drones(self, end) -> None:
        done = []
        for i in range(self.network.nb_drones):
            drone = self.network.drones[i]
            if drone.wait_turn > 0:
                drone.t += 1
                drone.previous_hub = None
                drone.path.append(self.coordinates[drone.current_hub])
                drone.used_connection = None
                drone.wait_turn -= 1
                done.append(i)
        for i in range(self.network.nb_drones):
            if i in done:
                continue
            drone = self.network.drones[i]
            drone.t += 1
            if drone.current_hub != end:
                new_hub = self.check_best_option(drone, end)
                drone.previous_hub = drone.current_hub
                drone.current_hub = new_hub
            if drone.current_hub == drone.previous_hub:
                drone.used_connection = None
            else:
                used_connection = tuple(sorted((drone.previous_hub, drone.current_hub)))
            if self.check_restricted(drone.current_hub):
                drone.wait_turn += 1
            drone.path.append(self.coordinates[drone.current_hub])
            done.append(i)
    
    def simulation_done(self, end: str) -> bool:
        drones = self.network.drones
        for i in range(self.network.nb_drones):
            if drones[i].current_hub != end:
                return False
            if drones[i].wait_turn > 0:
                return False
        return True

    def simulation(self):
        for hub in self.network.hubs:
            if hub.function == Zone_function.START:
                start = hub.name
            elif hub.function == Zone_function.END:
                end = hub.name
        for drone in self.network.drones:
            drone.path.append(self.coordinates[start])
        while not self.simulation_done(end):
            self.run_drones(end)
            self.connections_capacity = self.get_connections_capacity(self.network)


# graph=
# {'goal': [('path_a', 1.0), ('path_b', 1.0)],
#  'junction': [('start', 1.0), ('path_a', 1.0), ('path_b', 1.0)],
#  'path_a': [('junction', 1.0), ('goal', 1.0)],
#  'path_b': [('junction', 1.0), ('goal', 1.0)],
#  'start': [('junction', 1.0)]}



# distances=
# {'junction': 2.0, 'path_a': 1.0, 'path_b': 1.0, 'start': 3.0}