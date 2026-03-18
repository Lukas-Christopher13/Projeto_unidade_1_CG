from services.log_service import LogService

log = LogService()


def draw_ellipse_midpoint(rx, ry, xc=0, yc=0, log_step=20):
    points = []

    log.header("ELIPSE — MIDPOINT")
    log.step("Parâmetros:")
    log.info(f"Centro = ({xc}, {yc})")
    log.info(f"rx = {rx} | ry = {ry}")
    log.separator()

    x = 0
    y = ry

    rx2 = rx * rx
    ry2 = ry * ry
    two_rx2 = 2 * rx2
    two_ry2 = 2 * ry2

    log.step("Constantes:")
    log.info(f"rx²={rx2} | ry²={ry2}")
    log.info(f"2rx²={two_rx2} | 2ry²={two_ry2}")
    log.separator()

    #Região 1
    p1 = ry2 - (rx2 * ry) + (0.25 * rx2)
    dx = 0
    dy = two_rx2 * y

    log.step("Região 1")
    log.info(f"p1 inicial = {p1:.2f}")
    log.separator()

    k = 0
    while dx < dy:
        #Simetria
        points.extend([
            (xc + x, yc + y),
            (xc - x, yc + y),
            (xc + x, yc - y),
            (xc - x, yc - y),
        ])

        if k % log_step == 0:
            log.iteration(f"k={k} | x={x} y={y} | p1={p1:.2f}")

        x += 1
        dx += two_ry2

        if p1 < 0:
            p1 += ry2 + dx
            decision = "E"
        else:
            y -= 1
            dy -= two_rx2
            p1 += ry2 + dx - dy
            decision = "SE"

        if k % log_step == 0:
            log.info(f"Decisão: {decision}")

        k += 1

    log.separator()
    log.step("Mudança para Região 2")
    log.separator()

    #Região 2 
    p2 = ry2 * (x + 0.5)**2 + rx2 * (y - 1)**2 - rx2 * ry2

    log.step("Região 2")
    log.info(f"p2 inicial = {p2:.2f}")
    log.separator()

    k = 0
    while y >= 0:
        points.extend([
            (xc + x, yc + y),
            (xc - x, yc + y),
            (xc + x, yc - y),
            (xc - x, yc - y),
        ])

        if k % log_step == 0:
            log.iteration(f"k={k} | x={x} y={y} | p2={p2:.2f}")

        y -= 1
        dy -= two_rx2

        if p2 > 0:
            p2 += rx2 - dy
            decision = "S"
        else:
            x += 1
            dx += two_ry2
            p2 += rx2 - dy + dx
            decision = "SE"

        if k % log_step == 0:
            log.info(f"Decisão: {decision}")

        k += 1

    log.separator()
    log.result(f"Total de pontos gerados: {len(points)}")

    return points