__author__ = 'ovol'

from vector import Vector


class Triangle(object):
    def __init__(self, vertices):
        if len(vertices) != 3:
            raise ValueError('Triangle must contain 3 vertices.')
        for vertex in vertices:
            if not isinstance(vertex, Vector):
                raise ValueError('%s is not a Vector' % vertex)
        self.vertices = vertices

    @property
    def vertices(self):
        return self.vertices


class RightTriangle(object):
    def __init__(self, vertex, legs):
        if not isinstance(vertex, Vector):
            raise ValueError('Triangle right angle vertex is not a vector')
        if len(legs) != 2:
            raise ValueError('Triangle must contain exactly 2 legs (%d found)' % len(legs))
        for leg in legs:
            if not isinstance(leg, Vector):
                raise ValueError('Leg %s is not a Vector' % leg)

        self.vertex = vertex
        self.legs = legs

    @property
    def vertex(self):
        return self.vertex

    @property
    def legs(self):
        return self.legs