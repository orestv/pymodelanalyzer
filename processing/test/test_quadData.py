from unittest import TestCase
import math

__author__ = 'seth'

from geometry.vector import Vector
from geometry.quad import Quad
from geometry import geometryutils
from mock import patch
from mock import sentinel
from processing.quaddata import QuadData


class TestQuadData(TestCase):
    @patch('geometry.geometryutils.get_vector_to_center')
    @patch.multiple(QuadData,
                    get_perpendicular_angle=sentinel.DEFAULT,
                    process_normale_angle=sentinel.DEFAULT,
                    process_distance=sentinel.DEFAULT,
                    process_sizes=sentinel.DEFAULT)
    def test_process(self,
                     get_vector_to_center,
                     get_perpendicular_angle,
                     process_normale_angle,
                     process_distance,
                     process_sizes):
        qd = QuadData(None, None)
        qd.process()

        #assert qd.check_data.called

        assert get_vector_to_center.called
        assert qd.get_perpendicular_angle.called
        assert qd.process_normale_angle.called
        assert qd.process_distance.called
        assert qd.process_sizes.called

        #def test_check_data(self):
        #    self.fail()
        #
        #def test_process_angles(self):
        #    self.fail()
        #
        #def test_process_distance(self):
        #    self.fail()
        #
        #def test_process_sizes(self):
        #    self.fail()
        #
        #@patch.object

    @patch.multiple(geometryutils,
                    get_middle_perpendiculars=sentinel.DEFAULT,
                    get_vector_to_center=sentinel.DEFAULT,
                    get_projection_onto_plane=sentinel.DEFAULT)
    def test_get_perpendicular_angle(self,
                                     get_middle_perpendiculars,
                                     get_vector_to_center,
                                     get_projection_onto_plane):
        ov = Vector(3, 3, 3)
        quad = Quad([Vector(-1, 0, -1),
                     Vector(-1, 0, 1),
                     Vector(1, 0, 1),
                     Vector(1, 0, -1)])

        get_middle_perpendiculars.return_value = Vector(2, 0, 0), Vector(0, 0, 2)
        get_vector_to_center.return_value = Vector(-3, -3, -3)
        get_projection_onto_plane.return_value = Vector(-1, 0, -1)

        angle = QuadData.get_perpendicular_angle(ov, quad)

        self.assertEquals(angle, math.pi / 4.)
