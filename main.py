from parser import set_network
from algorithm import Algorithm
from pydantic import ValidationError
from visualisation import Drawer
import sys
# from pprint import pprint


def main() -> None:
    if len(sys.argv) != 2:
        print("Please specify the path of the text file!")
        return
    network = set_network(sys.argv[1])
    drawer = Drawer(network)
    drawer.draw_map()
    # algo = Algorithm(network)
    # algo.solve_map()



if __name__ == "__main__":
    # try:
    #     main()
    # except ValidationError as e:
    #     print(e.errors()[0]["msg"])
    # except Exception as e:
    #     print(e)
    main()
