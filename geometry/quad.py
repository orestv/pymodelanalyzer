__author__ = 'seth'

import math
from vector import Vector


class Quad(object):
    def __init__(self, vertices, normale):
        self.vertices = vertices
        self.normale = normale

    def is_rectangle(self):
        v1 = self.vertices[1] - self.vertices[2]
        v2 = self.vertices[0] - self.vertices[3]
        return v1.angle(v2) == 0 and v1.length == v2.length
