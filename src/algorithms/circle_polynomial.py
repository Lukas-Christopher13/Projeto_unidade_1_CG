import math

from src.algorithms.octant import draw_octant
from services.log_service import LogService

log = LogService()


def draw_circle_polynomial(radius):
    log.header("CIRCUNFERÊNCIA - Polinomial")
    log.step(f"Raio: R = {radius}")
    log.step(f"Fórmula: y = √(R² - x²)")
    log.separator()

    points = []

    x = 0
    y = float(radius)

    k = 0
    while x <= y:
        current_point = (x, round(y))
        points.append(current_point)

        r2_x2 = radius**2 - x**2
        if k <= 15:
            log.iteration(f"k={k}: x={x}  y = √({radius}² - {x}²) = √({r2_x2}) = {y:.2f}  → ({x}, {round(y)})")
        elif k == 16:
            log.iteration("...")

        x += 1
        if radius**2 - x**2 >= 0:
            y = math.sqrt(radius**2 - x**2)
        else:
            break
        k += 1

    octant_points = draw_octant(points)
    log.result(f"Pontos no 1º octante: {len(points)}")
    log.result(f"Total (8 octantes): {len(octant_points)} pontos")
    log.separator()

    return octant_points
