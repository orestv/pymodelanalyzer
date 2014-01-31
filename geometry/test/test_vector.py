import unittest

__author__ = 'seth'

from geometry.vector import Vector


class TestVector(unittest.TestCase):
    def test_vectors_not_equal(self):
        v1 = Vector(1, 1, 1)
        v2 = Vector(2, 2, 2)
        self.assertFalse(v1 == v2)
        self.assertNotEquals(v1, v2)

    def test_is_normalized(self):
        v = Vector(1, 1, 1)
        self.assertFalse(v.is_normalized)

        v = Vector(1, 0, 0)
        self.assertTrue(v.is_normalized)

        v = Vector(0, 0, 0)
        self.assertFalse(v.is_normalized)

    def test_get_normalized(self):
        v = Vector(1, 1, 1)
        n = v.unit()
        self.assertAlmostEqual(n.x, 0.577, 3)
        self.assertAlmostEqual(n.y, 0.577, 3)
        self.assertAlmostEqual(n.z, 0.577, 3)

        v = Vector(0, 0, 0)
        self.assertRaises(ValueError, v.unit)

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