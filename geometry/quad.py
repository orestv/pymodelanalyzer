__author__ = 'seth'


class Quad(object):
    def __init__(self, vertices, normale=None):
        self.vertices = vertices
        if not normale:
            v1 = self.vertices[0] - self.vertices[1]
            v2 = self.vertices[2] - self.vertices[1]
            normale = v2.vector_product(v1)
        normale = normale.get_normalized()
        self.normale = normale

    def __eq__(self, other):
        return self.vertices == other.vertices and self.normale == other.normale

    def __repr__(self):
        return 'Quad of %s, normale: %s' % (self.vertices, self.normale)

    def __str__(self):
        return 'Quad of %s, normale: %s' % (self.vertices, self.normale)