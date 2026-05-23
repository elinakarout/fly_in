from parser import set_network
from pydantic import ValidationError
import sys


def main() -> None:
    if len(sys.argv) != 2:
        print("Please specify the path of the text file!")
        return
    network = set_network(sys.argv[1])
    print("nb_drones:", network.nb_drones)
    print("HUBS:")
    for hub in network.hubs:
        print(f"name: '{hub.name}'")
        print("function:", hub.function)
        print("x:", hub.coord_x)
        print("y:", hub.coord_y)
        print("type:", hub.zone_type)
        print("color:", hub.color)
        print("max_drones:", hub.max_drones)
        print()
    print("Connections:")
    for connection in network.connections:
        print("hubs:", connection.hubs)
        print("max capacity:", connection.max_link_capacity)


if __name__ == "__main__":
    try:
        main()
    except ValidationError as e:
        print(e.errors()[0]["msg"])
    except Exception as e:
        print(e)
