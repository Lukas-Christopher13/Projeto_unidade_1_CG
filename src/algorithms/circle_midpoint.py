from src.algorithms.octant import draw_octant

def draw_circleMP(radius):
    points = []
    
    x = 0
    y = radius
    d = 1 - radius

    points.append((x, y))

    while y > x:
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
        points.append((x, y))
    
    return draw_octant(points)
