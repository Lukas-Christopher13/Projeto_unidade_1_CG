import math
from services.log_service import LogService

log = LogService()

#matemática base
def binomial_coeff(n, k):
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))


#cálculo de ponto da Bézier
def compute_bezier_point(u, ctrl_pts, log_details=False):
    n = len(ctrl_pts) - 1
    x = 0
    y = 0

    if log_details:
        log.step(f"u = {u:.3f}")

    for k in range(len(ctrl_pts)):
        coeff = binomial_coeff(n, k)
        blend = coeff * (u ** k) * ((1 - u) ** (n - k))
        px, py = ctrl_pts[k]

        if log_details:
            log.info(
                f"k={k} | C({n},{k})={coeff} | "
                f"blend={blend:.5f} | P{k}=({px},{py})"
            )

        x += px * blend
        y += py * blend

    if log_details:
        log.result(
            f"B(u)=({x:.2f}, {y:.2f}) → Pixel({round(x)}, {round(y)})"
        )
        log.separator()

    return (x, y)


#curva Bézier Cúbica
def draw_bezier_cubic(p0, p1, p2, p3, n_points=1000, log_interval=50):
    ctrl_pts = [p0, p1, p2, p3]
    points = []

    log.header("CURVA DE BÉZIER CÚBICA")

    #pontos de controle
    log.step("Pontos de Controle:")
    log.info(f"P0 = {p0}  (início)")
    log.info(f"P1 = {p1}  (controle inicial)")
    log.info(f"P2 = {p2}  (controle final)")
    log.info(f"P3 = {p3}  (fim)")
    log.separator()

    #coeficientes binomiais
    log.step("Coeficientes Binomiais:")
    for k in range(4):
        log.info(f"C(3,{k}) = {binomial_coeff(3,k)}")
    log.separator()

    #amostragem
    du = 1 / n_points
    log.step(f"Amostragem: n_points = {n_points}")
    log.info(f"Δu = {du:.6f}")
    log.info(f"Log a cada {log_interval} iterações")
    log.separator()

    #iterações
    log.step("Cálculo dos Pontos:")

    for i in range(n_points + 1):
        u = i / n_points

        #regra do log
        should_log = (
            i == 0 or
            i == n_points or
            i % log_interval == 0
        )

        point = compute_bezier_point(
            u,
            ctrl_pts,
            log_details=should_log
        )
        points.append(point)

    log.separator()
    log.result(f"Total de pontos gerados: {len(points)}")

    return points