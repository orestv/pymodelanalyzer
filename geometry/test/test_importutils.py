__author__ = 'seth'

from unittest import TestCase
import geometry.importutils as importutils
import geometry.vector
from geometry.vector import Vector
from geometry.quad import Quad
import tempfile
import shutil
import sys, os
import mock


class TestImportUtils(TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp('pyquadtest')
        self.addCleanup(self.clean_temp_dir)

    def clean_temp_dir(self):
        try:
            shutil.rmtree(self.tempdir)
        except:
            print 'Failed to remove tempdir %s' % self.tempdir

    def test_parse_vertex_line(self):
        v = importutils.parse_vertex_line('v 0.2 0.5 0.3')
        self.assertEquals(v, geometry.vector.Vector(0.2, 0.5, 0.3))

    def test_parse_vertex_line_short(self):
        line = 'v 0.2 0.3'
        self.assertRaises(ValueError, importutils.parse_vertex_line,
                          line)

    def test_parse_face_line(self):
        line = 'f 2 3 4 5'
        v = importutils.parse_face_line(line)
        self.assertEquals(v, [1, 2, 3, 4])

    def test_parse_face_line_short(self):
        line = 'f 2 3'
        self.assertRaises(ValueError,
                          importutils.parse_face_line,
                          line)

    def test_import_obj(self):
        path = os.path.join(self.tempdir, 'valid.obj')
        lines = [
            "v -1 0 -1\n",
            "v -1 0 1\n",
            "v 1 0 1\n",
            "v 1 0 -1\n",
            "v -1 1 -1\n",
            "f 1 2 3 4\n",
        ]

        expected_vertices = [
            Vector(-1, 0, -1),
            Vector(-1, 0, 1),
            Vector(1, 0, 1),
            Vector(1, 0, -1),
            Vector(-1, 1, -1),
        ]
        expected_faces = [
            [0, 1, 2, 3]
        ]
        with open(path, 'w') as f:
            f.writelines(lines)

        importutils.build_quads = mock.MagicMock()

        quads = importutils.import_obj(path)

        importutils.build_quads.assert_called_with(expected_vertices, expected_faces)

    def test_build_quads(self):
        vertices = [
            Vector(-1, 0, -1),
            Vector(-1, 0, 1),
            Vector(1, 0, 1),
            Vector(1, 0, -1),
            Vector(-1, 1, 1),
            Vector(1, 1, 1),
        ]
        faces = [
            [3, 2, 1, 0],
            [1, 2, 5, 4],
        ]
        expected_quads = [
            Quad([Vector(1, 0, -1),
                  Vector(1, 0, 1),
                  Vector(-1, 0, 1),
                  Vector(-1, 0, -1)
            ]),
            Quad([Vector(-1, 0, 1),
                  Vector(1, 0, 1),
                  Vector(1, 1, 1),
                  Vector(-1, 1, 1)
            ]),
        ]

        quads = importutils.build_quads(vertices, faces)

        self.assertEquals(quads, expected_quads)