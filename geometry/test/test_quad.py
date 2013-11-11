from unittest import TestCase

__author__ = 'seth'

from geometry.vector import Vector
from geometry.quad import Quad


class TestQuad(TestCase):
    def test_auto_normale(self):
        vertices = [Vector(0, 0, 0),
                    Vector(1, 0, 0),
                    Vector(1, 0, -1),
                    Vector(0, 0, -1)]
        quad = Quad(vertices)
        self.assertEquals(quad.normale,
                          Vector(0, 1, 0))

    def test_auto_normale_2(self):
        vertices = [Vector(5, 4, 3),
                    Vector(6, 4, 3),
                    Vector(6, 4, 2),
                    Vector(5, 4, 2)]
        quad = Quad(vertices)
        self.assertEquals(quad.normale,
                          Vector(0, 1, 0))
