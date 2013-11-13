from unittest import TestCase

__author__ = 'seth'

from geometry import geometryutils
from mock import patch
from mock import sentinel
from processing.quaddata import QuadData


class TestQuadData(TestCase):
    @patch.multiple(QuadData, check_data=sentinel.DEFAULT,
                    process_perpendiculars_angles=sentinel.DEFAULT,
                    process_normale_angle=sentinel.DEFAULT,
                    process_distance=sentinel.DEFAULT,
                    process_sizes=sentinel.DEFAULT)
    def test_process(self, check_data,
                     process_perpendiculars_angles,
                     process_normale_angle,
                     process_distance,
                     process_sizes):
        qd = QuadData(None, None)

        assert qd.check_data.called

        assert qd.process_perpendiculars_angles.called
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
        def test_process_perpendiculars_angles(self,
                                               get_middle_perpendiculars,
                                               get_vector_to_center,
                                               get_projection_onto_plane):
            pass
