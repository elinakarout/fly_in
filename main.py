from parser import set_network
from data import Network, Zone_type
from algorithm import Solver
from pydantic import ValidationError
import sys
from pprint import pprint


def main() -> None:
    if len(sys.argv) != 2:
        print("Please specify the path of the text file!")
        return
    network = set_network(sys.argv[1])
    algo = Solver(network)
    print(algo.solve_map())

if __name__ == "__main__":
    # try:
    #     main()
    # except ValidationError as e:
    #     print(e.errors()[0]["msg"])
    # except Exception as e:
    #     print(e)
    main()
