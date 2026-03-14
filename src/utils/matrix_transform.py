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

def rotation(angle: float, tx, ty, tz=0.0):
    vertex = translate(tx, ty, tz)
    vertex = vertex @ basic_rotation(angle)
    vertex = vertex @ translate(-tx, -ty, -tz)
    return vertex

def basic_rotation(angle: float):
    r = radians(angle)

    rotation = np.array([
        [cos(r), -sin(r), 0.0, 0.0],
        [sin(r),  cos(r), 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)

    return rotation

def roation_x_axis(angle: float):
    r = radians(angle)

    return np.array([
        [1.0,  0.0,     0.0,    0.0],
        [0.0,  cos(r), -sin(r), 0.0],
        [0.0,  sin(r),  cos(r), 0.0],
        [0.0,  0.0,     0.0,    1.0]
    ], dtype=np.float32)

def roation_y_axis(angle: float):
    r = radians(angle)

    return np.array([
        [ cos(r), 0.0, sin(r), 0.0],
        [ 0.0,    1.0, 0.0,    0.0],
        [-sin(r), 0.0, cos(r), 0.0],
        [ 0.0,    0.0, 0.0,    1.0]
    ], dtype=np.float32)

def scaling(sx, sy, tx, ty, sz=0.0, tz=0.0):    
    vertex = translate(tx, ty, tz)
    vertex = vertex @ basic_scaling(sx, sy, sz)
    vertex = vertex @ translate(-tx, -ty, -tz)

    return vertex
   
    
def basic_scaling(sx: np.float32, sy: np.float32, sz=1.0):
    scaling = np.array([
        [sx, 0.0, 0.0, 0.0],
        [0.0, sy, 0.0, 0.0],
        [0.0, 0.0, sz, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)

    return scaling

def reflection_x():
    return np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0,-1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)


def reflection_y():
    return np.array([
        [-1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)


def reflection_origin():
    return np.array([
        [-1.0, 0.0, 0.0, 0.0],
        [0.0,-1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)

def reflection_xy():
    return np.array([
        [0.0, 1.0, 0.0, 0.0],
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)

def reflection_3d_xy():
    return np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, -1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)

def reflection_3d_yz():
    return np.array([
        [-1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)

def reflection_3d_xz():
    return np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, -1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)

def share(shx, shy, tx, ty, shz=0.0, tz=0.0):
    vertex = translate(tx, ty, tz)
    vertex = vertex @ basic_share(shx, shy)
    vertex = vertex @ translate(-tx, -ty, -tz)

    return vertex

def share_x(shy, shz):
    return np.array([
        [1.0, 0.0, 0.0, 0.0],
        [shy, 1.0, 0.0, 0.0],
        [shz, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)

def share_y(shx, shz):
    return np.array([
        [1.0, shx, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, shz, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)

def share_z(shx, shy):
    return np.array([
        [1.0, 0.0, shx, 0.0],
        [0.0, 1.0, shy, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)
    

def basic_share(shx=0.0, shy=0.0):
    return np.array([
        [1.0, shx, 0.0, 0.0],
        [shy, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)

def aplay_transformation(vertex, steps: list):
    print(vertex)
    for i in steps:
        vertex = vertex @ i.T
        print(vertex)
    return vertex
