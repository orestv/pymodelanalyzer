__author__ = 'seth'

import math

from vector import Vector


def is_rectangle(quad):
    v1 = quad.vertices[1] - quad.vertices[2]
    v2 = quad.vertices[0] - quad.vertices[3]
    return angle(v1, v2) == 0 and v1.length == v2.length


def get_middle_perpendiculars(quad):
    a = (quad.vertices[0] + quad.vertices[1]) / 2
    b = (quad.vertices[1] + quad.vertices[2]) / 2
    c = (quad.vertices[2] + quad.vertices[3]) / 2
    d = (quad.vertices[3] + quad.vertices[0]) / 2

    d1 = a - c
    d2 = b - d
    return d1, d2


def get_center(quad):
    center = Vector(0, 0, 0)
    for vertex in quad.vertices:
        center = center + vertex
    return center / 4.


def get_vector_to_center(vector_from, quad):
    center = get_center(quad)
    return center - vector_from


def get_projection_onto_vector(vector, vector_project):
    unit_vector = vector_project.get_normalized()
    scalar_projection = vector.dot_product(unit_vector)
    return unit_vector * scalar_projection


def get_projection_onto_plane(vector, plane_normale):
    vector_normale_part = get_projection_onto_vector(vector, plane_normale)
    return vector - vector_normale_part


def angle(v1, v2):
    if v1.length == 0 or v2.length == 0:
        raise ValueError('Cannot get angle to zero vector.')
    angle_cos = v1.get_normalized().dot_product(v2.get_normalized())
    if angle_cos == 0:
        result = math.pi / 2
    elif abs(abs(angle_cos) - 1) < 0.001:
        result = 0
    else:
        result = math.acos(angle_cos)
    return result


def sharp_angle(v1, v2):
    a = angle(v1, v2)
    if a > math.pi / 2:
        a = math.pi - a
    return a