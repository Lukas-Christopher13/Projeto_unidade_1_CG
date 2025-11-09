import math

from src.algorithms.octant import draw_octant

def draw_circle_polynomial(radius):
    points = []

    x = 0
    y = float(radius)

    k = 0
    while x <= y:
        current_point = (x, round(y))
        points.append(current_point)
        x += 1
        if radius**2 - x**2 >= 0:
            y = math.sqrt(radius**2 - x**2)
        else:
            break
        k += 1

    return draw_octant(points)
