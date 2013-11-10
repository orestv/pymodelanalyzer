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