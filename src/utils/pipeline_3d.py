
import numpy as np

class Pipeline3D:
    def __init__(self, width, height, x_min, y_min):
        self.width = width
        self.height = height
        self.x_min = x_min
        self.y_min = y_min

    def transform(self, np_matrix):
        #modeling_transformation = None #Implementar ()
        #clipping = None #Implementar
 
        result = np_matrix @ self.isometric_rotation().T

        # 2 — Projeção ortográfica paralela
        result = result @ self.orthographic_projection().T

        # 3 — Normalização NDC
        result = np.array([self.normalize_to_ndc(v) for v in result])

        # 4 — Viewport
        result = result @ self.viewport_transformation().T

        # --Ordem--
        #Modeling Transformation
        #Viewing Transformation
        #Projection Transformation
        #Normalization Transformation
        #Viewport Transformation
        #Clipping Transformation 

        return result
    
    def isometric_rotation(self):
        # Rotação em Y: 45°
        Ry = np.array([
            [ np.sqrt(2)/2, 0,  -np.sqrt(2)/2, 0],
            [ 0,             1,  0,             0],
            [ np.sqrt(2)/2, 0,  np.sqrt(2)/2,  0],
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

    def orthographic_projection(self, l=-200, r=200, b=-200, t=200, n=-500, f=500):
        return np.array([
            [2/(r-l), 0,         0,         -(r+l)/(r-l)],
            [0,       2/(t-b),   0,         -(t+b)/(t-b)],
            [0,       0,        -2/(f-n),   -(f+n)/(f-n)],
            [0,       0,         0,          1]
        ], dtype=np.float32)
    
    
    def normalize_to_ndc(self, v):
        """
        Converte um ponto em Clip Space (x, y, z, w)
        para NDC ao dividir tudo por w.
        """
        x, y, z, w = v
        
        if w == 0:
            raise ValueError("w = 0 → não é possível dividir")

        return np.array([x/w, y/w, z/w, 1.0], dtype=np.float32)
    
    def viewport_transformation(self):
        """
        Retorna a matriz 4x4 de transformação de viewport.
        
        Parâmetros:
            x_min  → posição inicial do viewport no eixo X
            y_min  → posição inicial do viewport no eixo Y
            width  → largura do viewport (em pixels)
            height → altura do viewport (em pixels)
        """

        # Metade das dimensões
        w2 = self.width / 2.0
        h2 = self.height / 2.0

        # A matriz de viewport é uma transformação afim:
        M = np.array([
            [ w2,   0.0, 0.0, self.x_min + w2 ],
            [ 0.0,  h2, 0.0, self.y_min + h2 ],  # OBS: sinal negativo para inverter Y
            [ 0.0,  0.0, 0.5, 0.5       ], # mapeia Z de [-1,1] para [0,1]
            [ 0.0,  0.0, 0.0, 1.0       ]
        ], dtype=np.float32)

        return M