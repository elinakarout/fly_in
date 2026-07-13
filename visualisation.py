from data import Network
import arcade
import math


class Drawer(arcade.Window):
    """
    Drawer class, inherits from arcade.Window
    """
    def __init__(self, network: Network) -> None:
        self.network = network
        self.hubs = network.hubs
        self.nb_drones = network.nb_drones
        self.connections = network.connections
        if self.nb_drones < 8:
            self.cell_size = 80
        elif self.nb_drones < 10:
            self.cell_size = self.nb_drones * 10
        elif self.nb_drones < 15:
            self.cell_size = self.nb_drones * 5
        else:
            self.cell_size = 70
        self.rows, self.y = self.get_rows(network)
        self.cols, self.x = self.get_cols(network)
        height = self.rows * self.cell_size
        width = self.cols * self.cell_size
        super().__init__(width, height, "Fly In - ekarout")
        self.width = width
        self.height = height
        self.radius = 20
        if self.nb_drones < 10:
            self.extra_radius = 6
        else:
            self.extra_radius = 1
        self.speed = 200
        self.current_turn = 0
        self.turn_duration = 0.5
        self.turn_timer = 0.0
        self.turn_label = arcade.Text(
            "Turn: 0",
            20,
            self.height - 40,
            arcade.color.BLACK,
            20
        )
        self.drone_labels = self.get_drone_labels(self.network)
        arcade.set_background_color(arcade.color.BABY_BLUE)

    @staticmethod
    def get_drone_labels(network: Network) -> dict[int, arcade.Text]:
        """
        Returns all drone labels Text instances,
        to be used in the visualisation
        """
        drone_labels = {}
        for drone in network.drones:
            drone_labels[drone.id] = arcade.Text(
                f"D{drone.id}",
                0,
                0,
                arcade.color.BLACK,
                6,
                anchor_x="center",
                anchor_y="center"
            )
        return drone_labels

    @staticmethod
    def get_rows(network: Network) -> tuple[int, int]:
        """
        Get number of rows according to given map
        """
        y = []
        for hub in network.hubs:
            y.append(hub.coord_y)
        if min(y) < 0:
            extra = 4 - min(y)
        else:
            extra = 4
        return (max(y) + extra, math.floor(extra / 2 + 0.5))

    @staticmethod
    def get_cols(network: Network) -> tuple[int, int]:
        """
        Get number of cols according to given map
        """
        x = []
        for hub in network.hubs:
            x.append(hub.coord_x)
        if min(x) < 0:
            extra = 4 - min(x)
        else:
            extra = 4
        return (max(x) + extra, math.floor(extra / 2 + 0.5))

    def write_name(self, text: str, x: int, y: int, size: int) -> None:
        """
        Draws the name of each hub
        """
        label = arcade.Text(
            text,
            x,
            y,
            arcade.color.BLACK,
            font_size=size,
            anchor_x="center",
            anchor_y="center"
        )
        label.draw()

    def map_coords(self) -> dict[str, tuple[int, int]]:
        """
        Get the coordinates of the hubs on the grid
        """
        coordinates = {}
        for hub in self.hubs:
            x = (hub.coord_x + self.x) * self.cell_size
            y = (hub.coord_y + self.y) * self.cell_size
            coordinates[hub.name] = (x, y)
        return coordinates

    def draw_grid(self) -> None:
        """
        Draw grid lines
        """
        for x in range(0, self.width + 1, self.cell_size):
            arcade.draw_line(x, 0, x, self.height, arcade.color.GRAY)
        for y in range(0, self.height + 1, self.cell_size):
            arcade.draw_line(0, y, self.width, y, arcade.color.GRAY)

    def draw_hubs(self) -> None:
        """
        Draw each hub with its name and color
        """
        for hub in self.hubs:
            x = (hub.coord_x + self.x) * self.cell_size
            y = (hub.coord_y + self.y) * self.cell_size
            if (hub.color == "none" or hub.color == "rainbow"):
                color = arcade.color.WHITE
            elif (hub.color == "darkred"):
                color = arcade.color.DARK_RED
            else:
                color = getattr(arcade.color, hub.color.upper())
            radius = self.radius + (hub.max_drones * self.extra_radius)
            arcade.draw_circle_filled(
                x, y, radius, color
            )
            self.write_name(hub.name, x, y, 7)

    def draw_connections(self) -> None:
        """
        Draws the connecting line between hubs
        """
        coordinates = self.map_coords()
        for connection in self.connections:
            p1 = coordinates[connection.hubs[0]]
            p2 = coordinates[connection.hubs[1]]
            arcade.draw_line(
                p1[0], p1[1],
                p2[0], p2[1],
                arcade.color.BLACK,
                3
            )

    def draw_drones(self) -> None:
        """
        Draw each drone and its label, while keeping the location relative
        to the timer, to be later able to animate them
        """
        progress = self.turn_timer / self.turn_duration
        for drone in self.network.drones:
            grid_x: float
            grid_y: float
            if self.current_turn >= len(drone.path) - 1:
                grid_x, grid_y = drone.path[-1]
            else:
                start_x, start_y = drone.path[self.current_turn]
                end_x, end_y = drone.path[self.current_turn + 1]
                grid_x = start_x + (end_x - start_x) * progress
                grid_y = start_y + (end_y - start_y) * progress
            if drone.id % 2:
                extra = + 4
            else:
                extra = - 4
            x = (grid_x + self.x) * self.cell_size + extra
            y = (grid_y + self.y) * self.cell_size + extra
            points = [
                (x, y + 10),
                (x + 10, y),
                (x, y - 10),
                (x - 10, y),
            ]
            arcade.draw_polygon_filled(
                points,
                arcade.color.GRAY
            )
            arcade.draw_polygon_outline(
                points,
                arcade.color.BLACK,
                2
            )
            label = self.drone_labels[drone.id]
            label.x = x
            label.y = y
            label.draw()

    def on_update(self, delta_time: float) -> None:
        """
        Updates the timer for drone animatiom, and adds a
        turn counter. Automatically calls itself during simulation
        """
        self.turn_timer += delta_time
        if (
            self.turn_timer >= self.turn_duration
            and self.current_turn < len(self.network.drones[0].path) - 1
        ):
            self.turn_timer = 0
            self.current_turn += 1
            self.turn_label.text = f"Turn: {self.current_turn}"

    def on_draw(self) -> None:
        """
        Calls all the drawers
        """
        self.clear()
        self.draw_grid()
        self.draw_connections()
        self.draw_hubs()
        self.draw_drones()
        self.turn_label.draw()
