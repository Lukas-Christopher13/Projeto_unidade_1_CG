import math

def binomial_coeff(n, k):
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))

def compute_bezier_point(u, ctrl_pts):
    n = len(ctrl_pts) - 1
    x = 0
    y = 0

    for k in range(len(ctrl_pts)):
        blend = binomial_coeff(n, k) * (u ** k) * ((1 - u) ** (n - k))
        x += ctrl_pts[k][0] * blend
        y += ctrl_pts[k][1] * blend

    return (x, y)

def draw_bezier_cubic(p0, p1, p2, p3, n_points=1000):
    ctrl_pts = [p0, p1, p2, p3]
    points = []

    for i in range(n_points + 1):
        u = i / n_points
        points.append(compute_bezier_point(u, ctrl_pts))

    return points