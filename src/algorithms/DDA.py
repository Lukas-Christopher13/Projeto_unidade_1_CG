from services.log_service import LogService

log = LogService()


def drawLineDDA(x1: float, y1: float, x2: float, y2: float) -> list:
    log.header("RETA - Algoritmo DDA")
    log.step(f"Entrada: P1({x1}, {y1}) → P2({x2}, {y2})")

    if abs(x2 - x1) > abs(y2 - y1):
        log.step("|Δx| > |Δy| → Variação principal em X (horizontal)")
        return drawLineDDAH(x1, y1, x2, y2)
    else:
        log.step("|Δy| ≥ |Δx| → Variação principal em Y (vertical)")
        return drawLineDDAV(x1, y1, x2, y2)


def drawLineDDAH(x1: float, y1: float, x2: float, y2: float):
    result = []

    lenght = abs(x2 - x1)
    if abs(y2 - y1) > lenght:
        lenght = abs(y2 - y1)

    xinc = (x2 - x1) / lenght
    yinc = (y2 - y1) / lenght

    log.step(f"1. Δx = x2 - x1 = {x2} - {x1} = {x2 - x1}")
    log.step(f"2. Δy = y2 - y1 = {y2} - {y1} = {y2 - y1}")
    log.step(f"3. passos = max(|Δx|, |Δy|) = {int(lenght)}")
    log.step(f"4. xinc = Δx / passos = {x2 - x1} / {int(lenght)} = {xinc:.4f}")
    log.step(f"5. yinc = Δy / passos = {y2 - y1} / {int(lenght)} = {yinc:.4f}")
    log.separator()

    x = x1
    y = y1

    result.append([round(x), round(y)])
    log.iteration(f"k=0: x={x:.2f}  y={y:.2f}  → Pixel({round(x)}, {round(y)})")

    k = 1
    while x < x2 if xinc >= 0 else x > x2:
        x = x + xinc
        y = y + yinc
        result.append([round(x), round(y)])
        if k <= 15 or k == int(lenght):
            log.iteration(f"k={k}: x={x:.2f}  y={y:.2f}  → Pixel({round(x)}, {round(y)})")
        elif k == 16:
            log.iteration("...")
        k += 1

    log.result(f"Total: {len(result)} pixels gerados")
    log.separator()
    return result


def drawLineDDAV(x1: float, y1: float, x2: float, y2: float):
    result = []

    lenght = abs(y2 - y1)
    if abs(x2 - x1) > lenght:
        lenght = abs(x2 - x1)

    xinc = (x2 - x1) / lenght
    yinc = (y2 - y1) / lenght

    log.step(f"1. Δx = x2 - x1 = {x2} - {x1} = {x2 - x1}")
    log.step(f"2. Δy = y2 - y1 = {y2} - {y1} = {y2 - y1}")
    log.step(f"3. passos = max(|Δx|, |Δy|) = {int(lenght)}")
    log.step(f"4. xinc = Δx / passos = {x2 - x1} / {int(lenght)} = {xinc:.4f}")
    log.step(f"5. yinc = Δy / passos = {y2 - y1} / {int(lenght)} = {yinc:.4f}")
    log.separator()

    x = x1
    y = y1

    result.append([round(x), round(y)])
    log.iteration(f"k=0: x={x:.2f}  y={y:.2f}  → Pixel({round(x)}, {round(y)})")

    k = 1
    while y < y2 if yinc >= 0 else y > y2:
        x = x + xinc
        y = y + yinc
        result.append([round(x), round(y)])
        if k <= 15 or k == int(lenght):
            log.iteration(f"k={k}: x={x:.2f}  y={y:.2f}  → Pixel({round(x)}, {round(y)})")
        elif k == 16:
            log.iteration("...")
        k += 1

    log.result(f"Total: {len(result)} pixels gerados")
    log.separator()
    return result
