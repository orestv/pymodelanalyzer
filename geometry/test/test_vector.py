import unittest

__author__ = 'seth'

from geometry.vector import Vector
import math


class TestVector(unittest.TestCase):
    def test_is_normalized(self):
        v = Vector(1, 1, 1)
        self.assertFalse(v.is_normalized)

        v = Vector(1, 0, 0)
        self.assertTrue(v.is_normalized)

        v = Vector(0, 0, 0)
        self.assertFalse(v.is_normalized)

    def test_get_normalized(self):
        v = Vector(1, 1, 1)
        n = v.get_normalized()
        self.assertAlmostEqual(n.x, 0.577, 3)
        self.assertAlmostEqual(n.y, 0.577, 3)
        self.assertAlmostEqual(n.z, 0.577, 3)

        v = Vector(0, 0, 0)
        self.assertRaises(ValueError, v.get_normalized)

    def test_angle(self):
        v1 = Vector(1, 0, 0)
        v2 = Vector(0, 1, 0)
        angle = v1.angle(v2)
        self.assertAlmostEqual(angle, math.pi/2., 3)

    def test_parallel_vectors_angle(self):
        v1 = Vector(1, 1, 1)
        v2 = Vector(3, 3, 3)
        angle = v1.angle(v2)
        self.assertEquals(angle, 0)

    def test_zero_vector_angle(self):
        v1 = Vector(0, 0, 0)
        v2 = Vector(1, 0, 0)
        self.assertRaises(ValueError, v1.angle, v2)

    def test_negative_vector_angle(self):
        v1 = Vector(0, 1, 0)
        v2 = Vector(-1, -1, 0)
        angle = v1.angle(v2)
        self.assertAlmostEquals(angle, 3*math.pi/4, 3)

    def test_vector_product(self):
        v1 = Vector(1, 0, 0)
        v2 = Vector(0, 1, 0)
        v = v1.vector_product(v2)
        self.assertEquals(v, Vector(0, 0, 1))

    def test_vector_product_parallel(self):
        v1 = Vector(1, 0, 0)
        v2 = Vector(2, 0, 0)
        v = v1.vector_product(v2)
        self.assertEquals(v.length, 0)

    def test_vector_product_zero(self):
        v1 = Vector(1, 0, 0)
        v2 = Vector(0, 0, 0)
        v = v1.vector_product(v2)
        self.assertEquals(v.length, 0)

    def test_vector_sub(self):
        v1 = Vector(1, 1, 0)
        v2 = Vector(-1, 1, 0)
        v = v1 - v2
        self.assertEquals(v, Vector(2, 0, 0))

    def test_vector_add(self):
        v1 = Vector(1, 1, 0)
        v2 = Vector(-1, 1, 0)
        v = v1 + v2
        self.assertEquals(v, Vector(0, 2, 0))

if __name__ == '__main__':
    unittest.main()