def drowLineMP(x1, y1, x2, y2) -> list:
    if abs(x2 - x1) > abs(y2 - y1): 
        return drowLineH(x1, y1, x2, y2)
    else:
        return drowLineV(x1, y1, x2, y2)

def drowLineH(x1, y1, x2, y2) -> list:
    result = []

    dx = x2 - x1
    dy = y2 - y1

    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    x, y = x1, y1

    result.append([x, y])
    while x < x2:
        if d <= 0:
            d += incE
            x += 1
        else:
            d += incNE
            x += 1
            y += 1
        result.append([x, y])
    return result

def drowLineV(x1, y1, x2, y2):
    result = []

    dx = x2 - x1
    dy = y2 - y1

    d = 2 * dx - dy
    incE = 2 * dx
    incNE = 2 * (dx - dy)

    x, y = x1, y1

    result.append([x, y])
    while y < y2:
        if d <= 0:
            d += incE
            y += 1
        else:
            d += incNE
            y += 1
            x += 1
        result.append([x, y])
    return result