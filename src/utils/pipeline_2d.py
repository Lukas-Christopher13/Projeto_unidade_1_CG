#model
#world -> cliping
#camera
#viewport
#screm

import numpy as np

from src.utils.matrix_transform import basic_scaling, translate

class Pipeline2D:
    world_xmin, world_ymin = -1000, -1000
    world_xmax, world_ymax = 1000, 1000

    # o mondo sou eu que defino (definir o mundo aqui)
    # mapeio para a tela do meu computado
    # depois normalizo

    def __init__(self, viewport_xmin, viewport_ymin, viewport_xmax, viewport_ymax):
        self.viewport_xmin = viewport_xmin
        self.viewport_ymin = viewport_ymin
        self.viewport_xmax = viewport_xmax
        self.viewport_ymax = viewport_ymax
        
    def transform(self, np_matrix):
        #modeling_transformation = None #Implementar () #aparentemente não precisa - o Shape Ja faz!!!

        np_matrix_copy = np_matrix.copy()

        np_matrix_copy[:, :4] = np_matrix_copy[:, :4] @ self.normalize_transformation().T

        np_matrix_copy[:, :4] = np_matrix_copy[:, :4] @ self.viwport_transformation().T
        
        # Object Coordinates
        # ↓ (Model Transform)
        # World Coordinates
        #         ↓ (Clipping)
        # World-Coordinate Clipping Window
        #         ↓ (Window → Viewport)
        # Normalized Device Coordinates (opcional)
        #         ↓
        # Viewport / Device Coordinates
        #         ↓
        # OpenGL (glVertex)

        return np_matrix_copy
    
    #talvez eu tenha que usar as formulas que centralizem
    
    def normalize_transformation(self): 
        sx = 2 / (self.world_xmax - self.world_xmin) 
        sy = 2 / (self.world_ymax - self.world_ymin) 
        
        n_cx = (self.world_xmin + self.world_xmax) / 2 
        n_cy = (self.world_ymin + self.world_ymax) / 2 
        
        w_cx = (-1 + 1) / 2 
        w_cy = (-1 + 1) / 2 
        
        return translate(n_cx, n_cy) @ basic_scaling(sx, sy) @ translate(-w_cx, -w_cy)
    
    def viwport_transformation(self): 
        sx = (self.viewport_xmax - self.viewport_xmin) / 2 
        sy = (self.viewport_ymax - self.viewport_ymin) / 2 

        tx = (self.viewport_xmax + self.viewport_xmin) / 2
        ty = (self.viewport_ymax + self.viewport_ymin) / 2
        
        n_cx = (-1 + 1) / 2 
        n_cy = (-1 + 1) / 2 
 
        return translate(tx, ty) @ basic_scaling(sx, sy) @ translate(-n_cx, -n_cy)


   


#o window seleciona uma parte da cena no mundo
#o viewport exibe essa parte da sena 