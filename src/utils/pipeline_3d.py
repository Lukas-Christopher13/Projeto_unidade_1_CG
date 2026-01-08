
import numpy as np

class Pipeline3D:
    xw_min, yw_min, z_near = -2000.0, -2000.0, -2000.0
    xw_max, yw_max, z_far  =  2000.0,  2000.0,  2000.0

    def __init__(self, viewport_xmin, viewport_ymin, viewport_xmax, viewport_ymax):
        self.viewport_xmin = viewport_xmin
        self.viewport_ymin = viewport_ymin
        self.viewport_xmax = viewport_xmax
        self.viewport_ymax = viewport_ymax

    def transform(self, np_matrix):
        #modeling_transformation = None #Implementar () #aparentemente não precisa - o Shape Ja faz!!!
        #clipping = None #Implementar
        np_matrix_copy = np_matrix.copy()
 
        np_matrix_copy[:, :4] = np_matrix_copy[:, :4] @ self.isometric_rotation().T

        # 3 — Normalização NDC
        np_matrix_copy[:, :4] = np_matrix_copy[:, :4] @ self.normalize_transformation().T

        # 4 — Viewport
        np_matrix_copy[:, :4] = np_matrix_copy[:, :4] @ self.viewport_tranformation().T

        # --Ordem--
        #Modeling Transformation
        #Viewing Transformation
        #Projection Transformation
        #Normalization Transformation
        #Viewport Transformation
        #Clipping Transformation 

        return np_matrix_copy
    
    def isometric_rotation(self):
        # Rotação em Y: 45°
        Ry = np.array([
            [ np.sqrt(2)/2, 0,  -np.sqrt(2)/2,  0],
            [ 0,             1,  0,             0],
            [ np.sqrt(2)/2, 0,  np.sqrt(2)/2,   0],
            [ 0,             0,  0,             1]
        ], dtype=np.float32)

        # Rotação em X: 35.264° (arctan(1/sqrt(2)))
        cosx = np.sqrt(2/3)
        sinx = 1/np.sqrt(3)

        Rx = np.array([
            [1,    0,     0,     0],
            [0,  cosx, -sinx,    0],
            [0,  sinx,  cosx,    0],
            [0,    0,     0,     1]
        ], dtype=np.float32)

        return Rx @ Ry
    
    def normalize_transformation(self):
        sx =  2 / (self.xw_max - self.xw_min)
        sy =  2 / (self.yw_max - self.yw_min)
        sz = -2 / (self.z_near - self.z_far)

        tx = - (self.xw_max + self.xw_min) / (self.xw_max - self.xw_min)
        ty = - (self.yw_max + self.yw_min) / (self.yw_max - self.yw_min)
        tz =   (self.z_near + self.z_far) / (self.z_near - self.z_far)

        return np.array([
            [ sx,  0.0, 0.0, tx ],
            [ 0.0, sy,  0.0, ty ],
            [ 0.0, 0.0, sz,  tz ], 
            [ 0.0, 0.0, 0.0, 1.0]
        ], dtype=np.float32)
    
    def normalize_transformation_2(self):
        sx = -2 * self.z_near / (self.xw_max - self.xw_min)
        sy = -2 * self.z_near / (self.yw_max - self.yw_min)
        sz = (self.z_near + self.z_far) / (self.z_near - self.z_far)

        tx = (self.xw_max + self.xw_min) / (self.xw_max - self.xw_min)
        ty = (self.yw_max + self.yw_min) / (self.yw_max - self.yw_min)
        tz = - 2 * (self.z_near * self.z_far) / (self.z_near - self.z_far)

        return np.array([
            [ sx,  0.0, tx,  0.0 ],
            [ 0.0, sy,  ty,  0.0 ],
            [ 0.0, 0.0, sz,  tz ], 
            [ 0.0, 0.0, 0.0, 0.0]
        ], dtype=np.float32)
    
    def viewport_tranformation(self):
        sx = (self.viewport_xmax - self.viewport_xmin) / 2
        sy = (self.viewport_ymax - self.viewport_ymin) / 2
        sz = 1 / 2

        tx = (self.viewport_xmax + self.viewport_xmin) / 2
        ty = (self.viewport_ymax + self.viewport_ymin) / 2
        tz = 1 / 2

        return np.array([
            [ sx,  0.0, 0.0, tx ],
            [ 0.0, sy,  0.0, ty ],
            [ 0.0, 0.0, sz,  tz ],
            [ 0.0, 0.0, 0.0, 1.0]
        ], dtype=np.float32)
