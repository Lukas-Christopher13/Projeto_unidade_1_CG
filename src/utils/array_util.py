
def transpose(matriz):
    return [
        [matriz[i][j] for i in range(len(matriz))]
        for j in range(len(matriz[0]))
    ]