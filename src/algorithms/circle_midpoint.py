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
    
    return draw_oc(points)

def draw_oc(points):
    circle = []
    for x, y in points:
        circle.append([+x, +y])
        circle.append([-x, +y])
        circle.append([+x, -y])
        circle.append([-x, -y])
        circle.append([+y, +x])
        circle.append([-y, +x])
        circle.append([+y, -x])
        circle.append([-y, -x])
    return circle

