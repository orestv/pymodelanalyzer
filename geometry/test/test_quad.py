from unittest import TestCase

__author__ = 'seth'

from geometry.vector import Vector
from geometry.quad import Quad


class TestQuad(TestCase):
    def test_is_rectangle(self):
        vertices = [Vector(-1, 0, -1),
                    Vector(2, 0, -1),
                    Vector(2, 0, 1),
                    Vector(-1, 0, 1)]
        normale = Vector(0, 1, 0)

        quad = Quad(vertices, normale)
        self.assertTrue(quad.is_rectangle())

    def test_is_rectangle_fail(self):
        vertices = [Vector(-1, 0, -1),
                    Vector(3, 0, -1),
                    Vector(2, 0, 1),
                    Vector(-1, 0, 1)]

        normale = Vector(0, 1, 0)
        quad = Quad(vertices, normale)
        self.assertFalse(quad.is_rectangle())