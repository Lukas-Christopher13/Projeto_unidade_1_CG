import math

def draw_circle_trigonometric(radius):
    points = []
    
    for grau in range(360):
        radiano = math.radians(grau)
        
        x_float = radius * math.cos(radiano)
        y_float = radius * math.sin(radiano)
        
        current_point = [round(x_float), round(y_float)]
        
        if not points or current_point != points[-1]:
            points.append(current_point)
           
    return points
