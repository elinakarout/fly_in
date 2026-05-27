from data import Network, Hub, Connection
import arcade
import math
import colorsys


class Drawer():
    def __init__(self, network: Network) -> None:
        self.hubs = network.hubs
        self.nb_drones = network.nb_drones
        self.connections = network.connections
        if self.nb_drones < 8:
            self.cell_size = self.nb_drones * 10
        elif self.nb_drones < 15:
            self.cell_size = self.nb_drones * 5
        else:
            self.cell_size = 70
        self.rows, self.y = self.get_rows(network)
        self.cols, self.x = self.get_cols(network)
        self.height = self.rows * self.cell_size
        self.width = self.cols * self.cell_size
        self.radius = 20
        if self.nb_drones < 10:
            self.extra_radius = 6
        else:
            self.extra_radius = 1
        self.title = "Fly In - ekarout"

    @staticmethod
    def get_rows(network: Network) -> tuple[int, int]:
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
        x = []
        for hub in network.hubs:
            x.append(hub.coord_x)
        if min(x) < 0:
            extra = 4 - min(x)
        else:
            extra = 4
        return (max(x) + extra, math.floor(extra / 2 + 0.5))

    def write_name(self, text, x, y, size):
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

    def map_coords(self):
        coordinates = {}
        for hub in self.hubs:
            x = (hub.coord_x + self.x) * self.cell_size
            y = (hub.coord_y + self.y) * self.cell_size
            coordinates[hub.name] = (x, y)
        return coordinates

    def draw_grid(self):
        for x in range(0, self.width + 1, self.cell_size):
            arcade.draw_line(x, 0, x, self.height, arcade.color.GRAY)
        for y in range(0, self.height + 1, self.cell_size):
            arcade.draw_line(0, y, self.width, y, arcade.color.GRAY)

    def draw_hubs(self):
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
                x , y , radius , color
            )
            self.write_name(hub.name, x, y, 10)

    def draw_connections(self):
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

    def draw_drones(self, x, y):
        points = [
            (x, y + 10),
            (x + 10, y),
            (x, y - 10),
            (x - 10, y),
        ]
        arcade.draw_polygon_filled(points, arcade.color.GRAY)
        self.write_name("D1", x, y, 5)

    def draw_map(self) -> None:
        arcade.open_window(self.width, self.height, self.title)
        arcade.set_background_color(arcade.color.BABY_BLUE)
        arcade.start_render()
        self.draw_grid()
        self.draw_connections()
        self.draw_hubs()
        self.draw_drones(self.x * self.cell_size, self.y * self.cell_size)
        arcade.finish_render()
        arcade.run()