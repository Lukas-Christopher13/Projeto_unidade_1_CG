from dataclasses import dataclass

@dataclass
class WorldWindowDTO:
    x_min: float
    y_min: float
    x_max: float
    y_max: float

world_bounds = WorldWindowDTO(
    x_min = -1000.0,
    y_min = -1000.0,
    x_min =  1000.0,
    y_min =  1000.0
)