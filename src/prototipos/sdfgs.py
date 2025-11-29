#Translatar(rotacionar) o centro da VRP para a origem(camera)
#Determine VPN
   #--

import numpy as np

def orthographic_projection(self,
    l=-200, r=200,
    b=-200, t=200,
    n=-500, f=500
):
    return np.array([
        [2/(r-l), 0,         0,         -(r+l)/(r-l)],
        [0,       2/(t-b),   0,         -(t+b)/(t-b)],
        [0,       0,        -2/(f-n),   -(f+n)/(f-n)],
        [0,       0,         0,          1]
    ], dtype=np.float32)



