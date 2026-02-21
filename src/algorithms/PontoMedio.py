from services.log_service import LogService

log = LogService()


def drawLineMP(x1, y1, x2, y2) -> list:
    log.header("RETA - Ponto Médio (Bresenham)")
    log.step(f"Entrada: P1({x1}, {y1}) → P2({x2}, {y2})")

    if abs(x2 - x1) > abs(y2 - y1):
        log.step("|Δx| > |Δy| → Variação principal em X")
        return drawLineH(x1, y1, x2, y2)
    else:
        log.step("|Δy| ≥ |Δx| → Variação principal em Y")
        return drawLineV(x1, y1, x2, y2)


def drawLineH(x1, y1, x2, y2) -> list:
    result = []

    dx = x2 - x1
    dy = y2 - y1

    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    log.step(f"1. dx = x2 - x1 = {dx}")
    log.step(f"2. dy = y2 - y1 = {dy}")
    log.step(f"3. d₀ = 2·dy - dx = 2·{dy} - {dx} = {d}")
    log.step(f"4. incE  = 2·dy = {incE}")
    log.step(f"5. incNE = 2·(dy - dx) = 2·({dy} - {dx}) = {incNE}")
    log.separator()

    x, y = x1, y1

    result.append([x, y])
    log.iteration(f"k=0: Pixel({x}, {y})  d={d}")

    k = 1
    while x < x2:
        if d <= 0:
            d += incE
            x += 1
            direction = "E"
        else:
            d += incNE
            x += 1
            y += 1
            direction = "NE"
        result.append([x, y])
        if k <= 15 or x == x2:
            log.iteration(f"k={k}: d→{direction}  d={d}  → Pixel({x}, {y})")
        elif k == 16:
            log.iteration("...")
        k += 1

    log.result(f"Total: {len(result)} pixels gerados")
    log.separator()
    return result


def drawLineV(x1, y1, x2, y2):
    result = []

    dx = x2 - x1
    dy = y2 - y1

    d = 2 * dx - dy
    incE = 2 * dx
    incNE = 2 * (dx - dy)

    log.step(f"1. dx = x2 - x1 = {dx}")
    log.step(f"2. dy = y2 - y1 = {dy}")
    log.step(f"3. d₀ = 2·dx - dy = 2·{dx} - {dy} = {d}")
    log.step(f"4. incE  = 2·dx = {incE}")
    log.step(f"5. incNE = 2·(dx - dy) = 2·({dx} - {dy}) = {incNE}")
    log.separator()

    x, y = x1, y1

    result.append([x, y])
    log.iteration(f"k=0: Pixel({x}, {y})  d={d}")

    k = 1
    while y < y2:
        if d <= 0:
            d += incE
            y += 1
            direction = "E"
        else:
            d += incNE
            y += 1
            x += 1
            direction = "NE"
        result.append([x, y])
        if k <= 15 or y == y2:
            log.iteration(f"k={k}: d→{direction}  d={d}  → Pixel({x}, {y})")
        elif k == 16:
            log.iteration("...")
        k += 1

    log.result(f"Total: {len(result)} pixels gerados")
    log.separator()
    return result