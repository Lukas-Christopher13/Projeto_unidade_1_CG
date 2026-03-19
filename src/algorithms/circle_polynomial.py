import math

from services.log_service import LogService

log = LogService()


def draw_circle_polynomial(radius, origin_x=0, origin_y=0):
    radius_int = int(round(abs(radius)))

    log.header("CIRCUNFERÊNCIA - Polinomial")
    log.step(f"Raio informado: R = {radius}")
    log.step(f"Raio usado para rasterização: R = {radius_int}")
    log.step("Fórmula: y = ±√(R² - x²)")
    log.step(f"Varredura completa: x de {-radius_int} até {radius_int}")
    log.separator()

    points = []
    logged = 0

    for x in range(-radius_int, radius_int + 1):
        value_inside_sqrt = radius_int**2 - x**2
        if value_inside_sqrt < 0:
            continue

        y_float = math.sqrt(value_inside_sqrt)
        y_rounded = round(y_float)

        top_point = [x, y_rounded]
        bottom_point = [x, -y_rounded]

        if origin_x != 0 or origin_y != 0:
            top_point = [top_point[0] + origin_x, top_point[1] + origin_y]
            bottom_point = [bottom_point[0] + origin_x, bottom_point[1] + origin_y]

        points.append(top_point)
        if y_rounded != 0:
            points.append(bottom_point)

        if logged < 16:
            log.iteration(
                f"x={x}: y = ±√({radius_int}² - {x}²) = ±√({value_inside_sqrt}) = ±{y_float:.2f}  "
                f"→ ({top_point[0]}, {top_point[1]})"
                + (f" e ({bottom_point[0]}, {bottom_point[1]})" if y_rounded != 0 else "")
            )
            logged += 1
        elif logged == 16:
            log.iteration("...")
            logged += 1

    log.result(f"Total: {len(points)} pontos gerados")
    log.separator()

    return points
