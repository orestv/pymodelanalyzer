class RightTriangle(object):
    def __init__(self, vertex, leg_1, leg_2):
        self.vertex = vertex
        self.leg_1 = leg_1
        self.leg_2 = leg_2

    @property
    def normale(self):
        product = self.leg_1.vector_product(self.leg_2)
        return product.unit()

    def __eq__(self, other):
        return self.vertex == other.vertex and \
               self.leg_1 == other.leg_1 and \
               self.leg_2 == other.leg_2

    def __str__(self):
        return 'Base: %s, legs: %s and %s' % (self.vertex, self.leg_1, self.leg_2)

    def __repr__(self):
        return 'Base: %s, legs: %s and %s' % (self.vertex, self.leg_1, self.leg_2)