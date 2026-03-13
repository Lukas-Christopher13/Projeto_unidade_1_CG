from src.algorithms.octant import draw_octant
from services.log_service import LogService

log = LogService()


def draw_circleMP(radius, origin_x=0, origin_y=0):
    log.header("CIRCUNFERÊNCIA - Ponto Médio")
    log.step(f"Raio: R = {radius}")

    points = []

    x = 0
    y = radius
    d = 1 - radius

    log.step(f"1. d₀ = 1 - R = 1 - {radius} = {d}")
    log.separator()

    points.append((x, y))
    log.iteration(f"k=0: x={x}  y={y}  d={d}  → ({x}, {y})")

    k = 1
    while y > x:
        old_d = d
        if d < 0:
            d += 2 * x + 3
            decision = f"d<0 → d += 2·{x}+3 = {d}"
        else:
            d += 2 * (x - y) + 5
            decision = f"d≥0 → d += 2·({x}-{y})+5 = {d}, y--"
            y -= 1
        x += 1
        points.append((x, y))

        if k <= 15:
            log.iteration(f"k={k}: {decision}  → ({x}, {y})")
        elif k == 16:
            log.iteration("...")
        k += 1

    octant_points = draw_octant(points)
    if origin_x != 0 or origin_y != 0:
        octant_points = [[x + origin_x, y + origin_y] for x, y in octant_points]
    log.result(f"Pontos no 1º octante: {len(points)}")
    log.result(f"Total (8 octantes): {len(octant_points)} pontos")
    log.separator()

    return octant_points
