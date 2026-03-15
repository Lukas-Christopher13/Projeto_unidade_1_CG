def draw_ellipse_midpoint(rx, ry, xc=0, yc=0):
    points = []

    x = 0
    y = ry
    rx2 = rx * rx
    ry2 = ry * ry
    two_rx2 = 2 * rx2
    two_ry2 = 2 * ry2

   
    p1 = ry2 - (rx2 * ry) + (0.25 * rx2)
    dx = 0
    dy = two_rx2 * y

    
    while dx < dy:
        
        points.append(( xc + x,  yc + y))
        points.append(( xc - x,  yc + y))
        points.append(( xc + x,  yc - y))
        points.append(( xc - x,  yc - y))

        x += 1
        dx += two_ry2
        if p1 < 0:
            p1 += ry2 + dx
        else:
            y -= 1
            dy -= two_rx2
            p1 += ry2 + dx - dy

    
    p2 = ry2 * (x + 0.5)**2 + rx2 * (y - 1)**2 - rx2 * ry2
    while y >= 0:
        points.append(( xc + x,  yc + y))
        points.append(( xc - x,  yc + y))
        points.append(( xc + x,  yc - y))
        points.append(( xc - x,  yc - y))

        y -= 1
        dy -= two_rx2
        if p2 > 0:
            p2 += rx2 - dy
        else:
            x += 1
            dx += two_ry2
            p2 += rx2 - dy + dx

    return points