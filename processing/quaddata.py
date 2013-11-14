# -*- coding: utf-8 -*

import math

from geometry import geometryutils


class QuadData(object):
    def __init__(self, observation_point, quad):
        self.op = observation_point
        self.quad = quad

        self.check_data()

        self.process()

    def check_data(self):
        pass

    def process(self):
        self.perpendicular_angle = self.get_perpendicular_angle()
        self.process_normale_angle()
        self.process_distance()
        self.process_sizes()

    @staticmethod
    def get_perpendicular_angle(op, quad):
        d1, d2 = geometryutils.get_middle_perpendiculars(quad)
        ov = geometryutils.get_vector_to_center(op, quad)
        ov_proj = geometryutils.get_projection_onto_plane(ov, quad)

        a1, a2 = abs(ov_proj.angle(d1)), abs(ov_proj.angle(d2))
        a1, a2 = abs(a1), abs(a2)
        if a1 > math.pi / 2.:
            a1 = math.pi - a1
        if a2 > math.pi / 2.:
            a2 = math.pi - a2
        return min(a1, a2)

    def process_normale_angle(self):
        ov = geometryutils.get_vector_to_center(self.op, self.quad)
        return ov.angle(self.quad.normale)

    def process_distance(self):
        pass

    def process_sizes(self):
        pass