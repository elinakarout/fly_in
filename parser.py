from validator import Network, Hub, Connection


def read_file(file_name: str) -> list[str]:
    try:
        with open(file_name, "r") as fd:
            content = fd.readlines()
        return (content)
    except FileNotFoundError:
        raise FileNotFoundError(f"{file_name} does not exist")


def create_hub(value: str, function: str) -> Hub:
    values = value.strip().split(" ", 3)
    if (len(values) < 3):
        raise ValueError("Hub format should be: <name> <x> <y> [metadata]!")
    name = values[0]
    x = int(values[1])
    y = int(values[2])
    # print(values[3])
    if (
        len(values) > 3
        and values[3].startswith("[")
        and values[3].endswith("]")
    ):
        metadata = {
            key: value
            for key, value in (
                item.split("=", 1)
                for item in values[3][1:-1].split()
            )
        }
        zone_type = metadata.get("zone", "normal")
        color = metadata.get("color", "none")
        max_drones = int(metadata.get("max_drones", 1))
    else:
        zone_type = "normal"
        color = "none"
        max_drones = 1
    return Hub(
        function=function,
        name=name,
        coord_x=x,
        coord_y=y,
        zone_type=zone_type,
        color=color,
        max_drones=max_drones
        )


def create_connection(value: str) -> Connection:
    values = value.strip().split("-", 2)
    if (len(values) < 2):
        raise ValueError(
            "Connection format should be: "
            "<name1>-<name2> [metadata]!"
            )
    if ('[' in values[1]):
        new_values = values[1].strip().split('[', 2)
        hubs = tuple([values[0], new_values[0]])
        if (new_values[1].strip().endswith(']')):
            metadata = {
                key: value
                for key, value in [new_values[1][:-1].strip().split("=")]
                }
            max_link_capacity = int(metadata["max_link_capacity"])
    else:
        hubs = tuple([values[0], values[1]])
        max_link_capacity = 1
    return Connection(
        hubs=hubs,
        max_link_capacity=max_link_capacity
        )


def set_network(file_name: str) -> Network:
    file_content = (read_file(file_name))
    i = 0
    while file_content[i].startswith("#") or not file_content[i].strip():
        i += 1
    if not file_content[i].startswith("nb_drones:"):
        raise ValueError("First line must start with 'nb_drones:'")
    nb_drones = 0
    hubs = []
    connections = []
    for line in file_content:
        if not line.startswith('#') and line.strip():
            key = line.strip().split(":", 2)
            if key[0] == "nb_drones":
                nb_drones = int(key[1])
            elif key[0] == "start_hub":
                hubs.append(create_hub(key[1], "start_hub"))
            elif key[0] == "end_hub":
                hubs.append(create_hub(key[1], "end_hub"))
            elif key[0] == "hub":
                hubs.append(create_hub(key[1], "hub"))
            elif key[0] == "connection":
                connections.append(create_connection(key[1]))
    return Network(
        nb_drones=nb_drones,
        hubs=hubs,
        connections=connections
        )
