from pydantic import BaseModel, Field, model_validator
from pydantic_core import PydanticCustomError
from typing import Self
from enum import Enum


class Zone_function(Enum):
    """
    Enum class for Zone function:
    Start hub, End hub, and normal hub
    """
    START = "start_hub"
    END = "end_hub"
    NORMAL = "hub"


class Zone_type(Enum):
    """
    Enum class for Zone type Metadata
    """
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Hub(BaseModel):
    """
    Hub BaseModel class, with all the required and default values
    """
    function: Zone_function
    name: str
    coord_x: int
    coord_y: int
    zone_type: Zone_type = Field(default=Zone_type.NORMAL)
    color: str = Field(default="none")
    max_drones: int = Field(default=1)

    @model_validator(mode="after")
    def hub_validation(self) -> Self:
        """
        Validating the name of the hub:
        Raises PydanticCustomError in case of dash '-' symbol in Hub name
        """
        if '-' in self.name:
            raise PydanticCustomError(
                "ValueError",
                f"in hub {self.name}: name cannot contain dashes '-'"
            )
        return self


class Connection(BaseModel):
    """
    Connection BaseModel class, with all the required and default values
    """
    hubs: tuple[str, str]
    max_link_capacity: int = Field(default=1)


class Drone(BaseModel):
    """
    Drone BaseModel class, with all the values
    required for the simulation
    """
    id: int
    t: int
    current_hub: str
    previous_hub: str | None = Field(default=None)
    path: list[tuple[float, float]]
    used_connection: tuple[str, str] | None = Field(default=None)
    wait_turn: int
    done: bool = Field(default=False)


class Network(BaseModel):
    """
    Network BaseModel class, containing the nb of drones,
    a list of the Hub instances, a list of the Connection instances,
    and a list of the Drone instances
    """
    nb_drones: int
    drones: list[Drone]
    hubs: list[Hub]
    connections: list[Connection]

    @model_validator(mode="after")
    def hub_validation(self) -> Self:
        """
        Validating the hubs in the network:
        Making sure nb of drones is positif
        Making sure there is exactly 1 start hub and 1 end hub,
        """
        if self.nb_drones <= 0:
            raise PydanticCustomError(
                "ValueError",
                "nb_drone is required and should be a positif int"
            )
        start = 0
        end = 0
        for hub in self.hubs:
            if hub.function == Zone_function.START:
                hub.max_drones = self.nb_drones
                start += 1
            if hub.function == Zone_function.END:
                end += 1
        if start == 0:
            raise PydanticCustomError(
                "ValueError",
                "There should be a start hub!"
            )
        if start > 1:
            raise PydanticCustomError(
                "ValueError",
                "There should be only one start hub!"
            )
        if end == 0:
            raise PydanticCustomError(
                "ValueError",
                "There should be an end hub!"
            )
        if end > 1:
            raise PydanticCustomError(
                "ValueError",
                "There should be only one end hub!"
            )
        return self

    @model_validator(mode="after")
    def connection_validation(self) -> Self:
        """
        Validating the hubs in the network:
        Making sure each name is an existing hub,
        And no duplicate connections
        """
        for connection in self.connections:
            for name in connection.hubs:
                if not any(
                    hub.name.strip() == name.strip()
                    for hub in self.hubs
                ):
                    raise PydanticCustomError(
                        "ValueError",
                        f"{name} is not a hub name"
                    )
        seen = set()
        for connection in self.connections:
            a, b = connection.hubs
            pair = tuple(sorted((a, b)))
            if pair in seen:
                raise PydanticCustomError(
                    "ValueError",
                    f"Duplicate connection: {a}-{b}"
                )
            seen.add(pair)
        return self
