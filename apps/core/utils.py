import math
class Coordinate:

    x = 0
    y = 0

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def get_distance(self, segundo_ponto):
        variacao_x = segundo_ponto.x - self.x
        variacao_y = segundo_ponto.y - self.y
        variacao_x = variacao_x**2
        variacao_y = variacao_y**2
        resultado = variacao_x+variacao_y
        return math.sqrt(resultado)

