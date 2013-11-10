__author__ = 'seth'

from unittest import TestCase
import geometry.importutils as importutils
import geometry.vector
import tempfile
import shutil

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
        self.assertEquals(v, [2, 3, 4, 5])

    def test_parse_face_line_short(self):
        line = 'f 2 3'
        self.assertRaises(ValueError,
                          importutils.parse_face_line,
                          line)