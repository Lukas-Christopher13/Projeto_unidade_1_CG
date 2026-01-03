#model
#world -> cliping
#camera
#viewport
#screm

import numpy as np

class Pipeline2D:
    world_xmin, world_ymin = -1000, -1000
    world_xmax, world_ymax = 1000, 1000

    # o mondo sou eu que defino (definir o mundo aqui)
    # mapeio para a tela do meu computado
    # depois normalizo

    def __init__(self, window_xmin, window_ymin, window_xmax, window_ymax):
        self.window_xmin = window_xmin
        self.window_ymin = window_ymin
        self.window_xmax = window_xmax
        self.window_ymax = window_ymax
        
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

    def model(self):
        pass

    def world(self):
        pass
    
    def viwing_to_normalized(self):
        pass

    def normalized_to_divice(self):
        pass


    #colocar a tranformação de word antes dessa!
    def normalize_transformation(self):
        sx = 2 / (self.world_xmax - self.world_xmin)
        sy = 2 / (self.world_ymax - self.world_ymin)
        tx = -(self.world_xmax + self.world_xmin) / (self.world_xmax - self.world_xmin)
        ty = -(self.world_ymax + self.world_xmin) / (self.world_ymax - self.world_ymin)

        return np.array([
            [sx,  0.0, 0.0, tx],
            [0.0, sy,  0.0, ty],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=np.float32)
        
    def viwport_transformation(self):
        sx = (self.window_xmax - self.window_xmin) / 2
        sy = (self.window_ymax - self.window_ymin) / 2
        tx = (self.window_xmax + self.window_xmin) / 2
        ty = (self.window_ymax + self.window_xmin) / 2

        return np.array([
            [sx,  0.0, 0.0, tx],
            [0.0, sy,  0.0, ty],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=np.float32)
    


#o window seleciona uma parte da cena no mundo
#o viewport exibe essa parte da sena 