import math
from math import cos, sin, radians
import numpy as np


def translate(x: np.float32, y: np.float32, z=0.0):
    translation = np.array([
        [1.0, 0.0, 0.0, x  ],
        [0.0, 1.0, 0.0, y  ],
        [0.0, 0.0, 1.0, z  ],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)

    return translation

def basic_rotation(angle: float):
    r = radians(angle)

    rotation = np.array([
        [cos(r), -sin(r), 0.0, 0.0],
        [sin(r),  cos(r), 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)

    return rotation

def basic_scaling(sx: np.float32, sy: np.float32, sz=0.0):
    scaling = np.array([
        [sx, 0.0, 0.0, 0.0],
        [0.0, sy, 0.0, 0.0],
        [0.0, 0.0, sz, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)

    return scaling