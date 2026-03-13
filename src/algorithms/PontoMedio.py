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
    sx = 1 if dx >= 0 else -1
    sy = 1 if dy >= 0 else -1
    dx_abs = abs(dx)
    dy_abs = abs(dy)

    d = 2 * dy_abs - dx_abs
    incE = 2 * dy_abs
    incNE = 2 * (dy_abs - dx_abs)

    log.step(f"1. dx = x2 - x1 = {dx}")
    log.step(f"2. dy = y2 - y1 = {dy}")
    log.step(f"3. d₀ = 2·|dy| - |dx| = 2·{dy_abs} - {dx_abs} = {d}")
    log.step(f"4. incE  = 2·|dy| = {incE}")
    log.step(f"5. incNE = 2·(|dy| - |dx|) = 2·({dy_abs} - {dx_abs}) = {incNE}")
    log.separator()

    x, y = x1, y1

    result.append([x, y])
    log.iteration(f"k=0: Pixel({x}, {y})  d={d}")

    k = 1
    while k <= dx_abs:
        if d <= 0:
            d += incE
            x += sx
            direction = "E"
        else:
            d += incNE
            x += sx
            y += sy
            direction = "NE"
        result.append([x, y])
        if k <= 15 or k == dx_abs:
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
    sx = 1 if dx >= 0 else -1
    sy = 1 if dy >= 0 else -1
    dx_abs = abs(dx)
    dy_abs = abs(dy)

    d = 2 * dx_abs - dy_abs
    incE = 2 * dx_abs
    incNE = 2 * (dx_abs - dy_abs)

    log.step(f"1. dx = x2 - x1 = {dx}")
    log.step(f"2. dy = y2 - y1 = {dy}")
    log.step(f"3. d₀ = 2·|dx| - |dy| = 2·{dx_abs} - {dy_abs} = {d}")
    log.step(f"4. incE  = 2·|dx| = {incE}")
    log.step(f"5. incNE = 2·(|dx| - |dy|) = 2·({dx_abs} - {dy_abs}) = {incNE}")
    log.separator()

    x, y = x1, y1

    result.append([x, y])
    log.iteration(f"k=0: Pixel({x}, {y})  d={d}")

    k = 1
    while k <= dy_abs:
        if d <= 0:
            d += incE
            y += sy
            direction = "E"
        else:
            d += incNE
            y += sy
            x += sx
            direction = "NE"
        result.append([x, y])
        if k <= 15 or k == dy_abs:
            log.iteration(f"k={k}: d→{direction}  d={d}  → Pixel({x}, {y})")
        elif k == 16:
            log.iteration("...")
        k += 1

    log.result(f"Total: {len(result)} pixels gerados")
    log.separator()
    return result
