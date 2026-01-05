from dataclasses import dataclass

@dataclass
class ViewportWindowDTO:
    x_min: float
    y_min: float
    x_max: float
    y_max: float

world_bounds = ViewportWindowDTO(
    x_min = -2000.0,
    y_min = -2000.0,
    x_min =  2000.0,
    y_min =  2000.0
)