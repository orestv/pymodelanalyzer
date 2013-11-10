__author__ = 'seth'


class Quad(object):
    def __init__(self, vertices, normale=None):
        self.vertices = vertices
        if not normale:
            normale = self.vertices[0].vector_product(self.vertices[1])
        self.normale = normale