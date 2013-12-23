__author__ = 'seth'

import unittest
import mox
import math

from processing import processor
from geometry.vector import Vector
from geometry.triangle import RightTriangle
from geometry import geometryutils


class TestProcessor(unittest.TestCase):
    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_get_f(self):
        alpha = math.pi / 4
        beta = math.pi / 4
        a = 0.2
        b = 0.6
        wavelength = 0.1
        f = processor.get_f(alpha, beta, a, b, wavelength)
        self.assertAlmostEqual(f, 1.002 * 10 ** (-5))

    def test_get_triangle_leg_angles(self):
        self.mox.StubOutWithMock(geometryutils, 'get_projection_onto_plane')
        self.mox.StubOutWithMock(geometryutils, 'sharp_angle')

        geometryutils.get_projection_onto_plane(Vector(-1, -1, -1),
                                                Vector(1, 0, 0)).AndReturn(Vector(99, 0, 0))
        geometryutils.sharp_angle(Vector(99, 0, 0),
                                  Vector(0, 1, 0)).AndReturn(50)
        geometryutils.sharp_angle(Vector(-1, -1, -1),
                                  Vector(99, 0, 0)).AndReturn(-50)

        self.mox.ReplayAll()
        angles = processor.get_triangle_leg_angles(Vector(0, 1, 0),
                                                   Vector(-1, -1, -1),
                                                   Vector(1, 0, 0))
        self.mox.VerifyAll()

        self.assertDictEqual(angles, {'alpha': 50, 'beta': -50})


    def test_process_triangle(self):
        self.mox.StubOutWithMock(processor, 'get_triangle_leg_angles')
        self.mox.StubOutWithMock(processor, 'get_f')

        processor.get_triangle_leg_angles(Vector(0, 0, 1),
                                          Vector(-1, -1, -1),
                                          Vector(0, 1, 0)).AndReturn(
            {'alpha': 0.5, 'beta': 1}
        )
        processor.get_triangle_leg_angles(Vector(0, 0, 1),
                                          Vector(-1, -1, -1),
                                          Vector(1, 0, 0)).AndReturn(
            {'alpha': 1.0, 'beta': 0.5}
        )
        processor.get_f(0.5, 0.5, 1.0, 1.0, 0.3).AndReturn(10)

        self.mox.ReplayAll()

        result = processor.process_triangle(Vector(1, 1, 1), 0.3,
                                            RightTriangle(Vector(0, 0, 0),
                                                          Vector(1, 0, 0),
                                                          Vector(0, 1, 0)))

        self.mox.VerifyAll()
        self.assertDictEqual(result, {'a': 1, 'b': 1,
                                      'alpha': 0.5,
                                      'beta': 0.5,
                                      'f': 10})


if __name__ == '__main__':
    unittest.main()