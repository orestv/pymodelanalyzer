from unittest import TestCase

__author__ = 'seth'

import geometry.utils as utils
from geometry.vector import Vector
from geometry.quad import Quad
import tempfile
import shutil


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
        self.assertTrue(utils.is_rectangle(quad))

    def test_is_rectangle_fail(self):
        vertices = [Vector(-1, 0, -1),
                    Vector(3, 0, -1),
                    Vector(2, 0, 1),
                    Vector(-1, 0, 1)]

        normale = Vector(0, 1, 0)
        quad = Quad(vertices, normale)
        self.assertFalse(utils.is_rectangle(quad))

    def test_middle_perpendiculars(self):
        vertices = [Vector(-1, 0, -1),
                    Vector(1, 0, -1),
                    Vector(1, 0, 1),
                    Vector(-1, 0, 1)]
        normale = Vector(0, 1, 0)
        quad = Quad(vertices, normale)

        d1, d2 = utils.get_middle_perpendiculars(quad)

        self.assertEquals((d1.x, d1.y, d1.z),
                          (0, 0, -2))
        self.assertEquals((d2.x, d2.y, d2.z),
                          (2, 0, 0))