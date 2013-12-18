class RightTriangle(object):
    def __init__(self, vertex, leg_1, leg_2):
        self.vertex = vertex
        self.leg_1 = leg_1
        self.leg_2 = leg_2

    @property
    def normale(self):
        product = self.leg_1.vector_product(self.leg_2)
        return product.get_normalized()