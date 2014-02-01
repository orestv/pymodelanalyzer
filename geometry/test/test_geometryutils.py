__author__ = 'seth'

from unittest import TestCase
import tempfile
import math
import shutil
import mox

import geometry.geometryutils as geometryutils
from geometry.vector import Vector
from geometry.quad import Quad
from geometry.triangle import RightTriangle


class TestUtils(TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp('pyquadtest')
        self.addCleanup(self.clean_temp_dir)
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def clean_temp_dir(self):
        try:
            shutil.rmtree(self.tempdir)
        except:
            print 'Failed to remove tempdir %s' % self.tempdir

    def test_is_rectangle(self):
        vertices = [Vector(-1, 0, -1),
                    Vector(2, 0, -1),
                    Vector(2, 0, 1),
                    Vector(-1, 0, 1)]
        normale = Vector(0, 1, 0)

        quad = Quad(vertices, normale)
        self.assertTrue(geometryutils.is_rectangle(quad))

    def test_is_rectangle_fail(self):
        vertices = [Vector(-1, 0, -1),
                    Vector(3, 0, -1),
                    Vector(2, 0, 1),
                    Vector(-1, 0, 1)]

        normale = Vector(0, 1, 0)
        quad = Quad(vertices, normale)
        self.assertFalse(geometryutils.is_rectangle(quad))

    def test_middle_perpendiculars(self):
        vertices = [Vector(-1, 0, -1),
                    Vector(1, 0, -1),
                    Vector(1, 0, 1),
                    Vector(-1, 0, 1)]
        normale = Vector(0, 1, 0)
        quad = Quad(vertices, normale)

        d1, d2 = geometryutils.get_middle_perpendiculars(quad)

        self.assertEquals((d1.x, d1.y, d1.z),
                          (0, 0, -2))
        self.assertEquals((d2.x, d2.y, d2.z),
                          (2, 0, 0))

    def test_get_center(self):
        vertices = [Vector(-1, 1, -1),
                    Vector(1, 1, -1),
                    Vector(1, 0, 1),
                    Vector(-1, 0, 1)]
        quad = Quad(vertices)
        center = geometryutils.get_center(quad)
        self.assertEquals(center, Vector(0, 0.5, 0))

    def test_get_projection(self):
        vector = Vector(1, 0, 0)
        vector_proj = Vector(1, 1, 0)
        expected_projection = Vector(0.5, 0.5, 0)
        projection = geometryutils.get_projection_onto_vector(vector, vector_proj)
        self.assertAlmostEqual(projection.x, expected_projection.x, 2)
        self.assertAlmostEqual(projection.y, expected_projection.y, 2)
        self.assertAlmostEqual(projection.z, expected_projection.z, 2)

    def test_get_projection_onto_plane(self):
        plane_normale = Vector(0, 2, 0)
        vector = Vector(1, 1, 1)
        expected_projection = Vector(1, 0, 1)
        projection = geometryutils.get_projection_onto_plane(vector, plane_normale)
        self.assertAlmostEqual(projection.x, expected_projection.x, 2)
        self.assertAlmostEqual(projection.y, expected_projection.y, 2)
        self.assertAlmostEqual(projection.z, expected_projection.z, 2)

    def test_get_projection_onto_diagonal_plane(self):
        plane_normale = Vector(-1, 1, 0)
        vector = Vector(1, 0, 0)
        expected_projection = Vector(0.5, 0.5, 0)
        projection = geometryutils.get_projection_onto_plane(vector, plane_normale)
        self.assertAlmostEqual(projection.x, expected_projection.x, 2)
        self.assertAlmostEqual(projection.y, expected_projection.y, 2)
        self.assertAlmostEqual(projection.z, expected_projection.z, 2)

    def test_angle(self):
        a = geometryutils.angle(Vector(1, 0, 0), Vector(1, 1, 0))
        self.assertAlmostEquals(a, math.pi / 4.)

        a = geometryutils.angle(Vector(1, 0, 0), Vector(-1, -1, 0))
        self.assertAlmostEqual(a, 3 * math.pi / 4)

    def test_angle_parallel(self):
        a = geometryutils.angle(Vector(1, 0, 0), Vector(2, 0, 0))
        self.assertEquals(a, 0)

    def test_angle_perpendicular(self):
        a = geometryutils.angle(Vector(1, 0, 0), Vector(0, 1, 0))
        self.assertEquals(a, math.pi / 2)

    def test_sharp_angle(self):
        a = geometryutils.sharp_angle(Vector(1, 0, 0), Vector(-1, -1, 0))
        self.assertAlmostEqual(a, math.pi / 4)

    def test_find_longest_side(self):
        vertices = [Vector(0, 2, 0),
                    Vector(10, 2, 0),
                    Vector(0, 0, 0)]
        v1_expected = Vector(10, 2, 0)
        v2_expected = Vector(0, 0, 0)

        v1, v2 = geometryutils.find_longest_side(vertices)

        self.assertEquals(v1, v1_expected)
        self.assertEquals(v2, v2_expected)

    def test_split_triangle(self):

        vertices = [Vector(0, 0, 0),
                    Vector(15, 0, 0),
                    Vector(13, 2, 0)]
        t1_expected = RightTriangle(Vector(13, 0, 0),
                                    Vector(0, 2, 0),
                                    Vector(-13, 0, 0))
        t2_expected = RightTriangle(Vector(13, 0, 0),
                                    Vector(2, 0, 0),
                                    Vector(0, 2, 0))

        t1, t2 = geometryutils.split_triangle(vertices)

        self.assertEquals(t1, t1_expected)
        self.assertEquals(t2, t2_expected)

    def test_find_right_triangle_vertex(self):
        vertices = [Vector(0, 0, 0),
                    Vector(15, 0, 0),
                    Vector(13, 2, 0)]
        v = geometryutils.find_right_triangle_vertex(vertices)
        self.assertEquals(v, None)

        vertices = [Vector(0, 0, 0),
                    Vector(15, 0, 0),
                    Vector(0, 2, 0)]
        v = geometryutils.find_right_triangle_vertex(vertices)
        self.assertEquals(v, Vector(0, 0, 0))

    def test_right_triangle_vertex_isosceles(self):
        vertices = [Vector(2, 0, 0),
                    Vector(0, 0, 0),
                    Vector(0, 2, 0)]
        v = geometryutils.find_right_triangle_vertex(vertices)
        self.assertEquals(v, Vector(0, 0, 0))