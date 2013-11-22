__author__ = 'seth'

from unittest import TestCase
import tempfile
import shutil

import geometry.geometryutils as geometryutils
from geometry.vector import Vector
from geometry.quad import Quad


class TestUtils(TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp('pyquadtest')
        self.addCleanup(self.clean_temp_dir)

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
        vertices = [Vector(-1, 2, -1),
                    Vector(1, 2, -1),
                    Vector(1, 2, 1),
                    Vector(-1, 2, 1)]
        quad = Quad(vertices)
        quad_normale = Vector(0, 1, 0)
        vector = Vector(1, 1, 1)
        expected_projection = Vector(1, 0, 1)
        projection = geometryutils.get_projection_onto_plane(vector, quad_normale)
        self.assertAlmostEqual(projection.x, expected_projection.x, 2)
        self.assertAlmostEqual(projection.y, expected_projection.y, 2)
        self.assertAlmostEqual(projection.z, expected_projection.z, 2)

    def test_get_projection_onto_diagonal_plane(self):
        vertices = [Vector(0, 0, -1),
                    Vector(1, 1, -1),
                    Vector(1, 1, 1),
                    Vector(0, 0, 1)]
        quad = Quad(vertices)
        quad_normale = Vector(1, -1, 0)
        vector = Vector(1, 0, 0)
        expected_projection = Vector(0.5, 0.5, 0)
        projection = geometryutils.get_projection_onto_plane(vector, quad_normale)
        self.assertAlmostEqual(projection.x, expected_projection.x, 2)
        self.assertAlmostEqual(projection.y, expected_projection.y, 2)
        self.assertAlmostEqual(projection.z, expected_projection.z, 2)
