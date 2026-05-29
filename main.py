from parser import set_network
from algorithm import Algorithm
# from pydantic import ValidationError
from visualisation import Drawer
import sys
from pprint import pprint
import arcade


def main() -> None:
    if len(sys.argv) != 2:
        print("Please specify the path of the text file!")
        return
    network = set_network(sys.argv[1])
    algo = Algorithm(network)
    algo.solve_map()
    drawer = Drawer(network)
    arcade.run()
    for drone in network.drones:
        pprint(drone.path)


if __name__ == "__main__":
    # try:
    #     main()
    # except ValidationError as e:
    #     print(e.errors()[0]["msg"])
    # except Exception as e:
    #     print(e)
    main()
