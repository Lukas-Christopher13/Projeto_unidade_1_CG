def draw_octant(points):
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
