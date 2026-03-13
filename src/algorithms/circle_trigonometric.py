import math

from services.log_service import LogService

log = LogService()


def draw_circle_trigonometric(radius, origin_x=0, origin_y=0):
    log.header("CIRCUNFERÊNCIA - Trigonométrica")
    log.step(f"Raio: R = {radius}")
    log.step("Fórmula: x = R·cos(θ),  y = R·sin(θ)")
    log.separator()

    points = []
    logged = 0

    for grau in range(360):
        radiano = math.radians(grau)

        x_float = radius * math.cos(radiano)
        y_float = radius * math.sin(radiano)

        current_point = [round(x_float), round(y_float)]
        if origin_x != 0 or origin_y != 0:
            current_point = [current_point[0] + origin_x, current_point[1] + origin_y]

        if not points or current_point != points[-1]:
            points.append(current_point)

            # Loga primeiros 12 graus e alguns marcos (90°, 180°, 270°)
            if logged < 12 or grau in (90, 180, 270, 359):
                log.iteration(
                    f"θ={grau:>3}°: x = {radius}·cos({grau}°) = {x_float:>7.2f},  "
                    f"y = {radius}·sin({grau}°) = {y_float:>7.2f}  → Pixel({current_point[0]}, {current_point[1]})"
                )
                logged += 1
            elif logged == 12:
                log.iteration("...")
                logged += 1

    log.result(f"Total: {len(points)} pontos únicos gerados")
    log.separator()

    return points
