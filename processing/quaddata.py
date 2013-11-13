# -*- coding: utf-8 -*

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
        self.process_perpendiculars_angles()
        self.process_normale_angle()
        self.process_distance()
        self.process_sizes()

    def process_perpendiculars_angles(self):
        d1, d2 = geometryutils.get_middle_perpendiculars(self.quad)
        ov = geometryutils.get_vector_to_center(self.op, self.quad)
        ov_proj = geometryutils.get_projection_onto_plane(ov, self.quad)
        a1, a2 = abs(ov_proj.angle(d1)), abs(ov_proj.angle(d2))
        self.beta = min(a1, a2)

    def process_normale_angle(self):
        ov = geometryutils.get_vector_to_center(self.op, self.quad)
        self.alpha = ov.angle(self.quad.normale)

    def process_distance(self):
        pass

    def process_sizes(self):
        pass