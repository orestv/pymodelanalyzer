__author__ = 'seth'

import math

from vector import Vector
from geometry.triangle import RightTriangle


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
    unit_vector = vector_project.unit()
    scalar_projection = vector.dot_product(unit_vector)
    return unit_vector * scalar_projection


def get_projection_onto_plane(vector, plane_normale):
    vector_normale_part = get_projection_onto_vector(vector, plane_normale)
    return vector - vector_normale_part


def angle(v1, v2):
    if v1.length == 0 or v2.length == 0:
        raise ValueError('Cannot get angle to zero vector.')
    angle_cos = v1.unit().dot_product(v2.unit())
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


def find_longest_side(vertices):
    vertices = vertices + [vertices[0]]
    pairwise = ((vertices[i], vertices[i + 1]) for i in range(3))
    v1_out, v2_out, max_len = None, None, None
    for v1, v2 in pairwise:
        l = (v2 - v1).length
        if l > max_len:
            v1_out, v2_out = v1, v2
            max_len = l
    return v1_out, v2_out


def split_triangle(vertices):
    v1, v2 = find_longest_side(vertices)
    perp_base = None
    for v in vertices:
        if v not in (v1, v2):
            perp_base = v
            break
    hippotenuse = perp_base - v1
    a = angle(hippotenuse, v2 - v1)
    v_unit = (v2 - v1).unit()
    leg = v_unit * (math.cos(a) * hippotenuse.length)

    right_angle_vertex = v1 + leg

    t1 = RightTriangle(right_angle_vertex,
                       perp_base - right_angle_vertex,
                       v1 - right_angle_vertex)
    t2 = RightTriangle(right_angle_vertex,
                       v2 - right_angle_vertex,
                       perp_base - right_angle_vertex)
    return t1, t2


def find_right_triangle_vertex(vertices):
    for vertex in vertices:
        other_vertices = [v for v in vertices if v != vertex]
        vectors = [v - vertex for v in other_vertices]
        a = angle(*vectors)
        if abs(math.pi / 2 - a) < 0.01:
            return vertex
    return None


def build_triangles(vertices):
    result = []
    if len(vertices) == 3:
        right_triangle_vertex = find_right_triangle_vertex(vertices)
        if right_triangle_vertex:
            other_vertices = [v for v in vertices if v != right_triangle_vertex]
            legs = [v - right_triangle_vertex for v in other_vertices]
            triangle = RightTriangle(right_triangle_vertex, *legs)
            result.append(triangle)
        else:
            triangles = split_triangle(vertices)
            result.extend(triangles)
    elif len(vertices) == 4:
        v1 = [vertices[i] for i in [0, 1, 2]]
        v2 = [vertices[i] for i in [0, 2, 3]]
        result = build_triangles(v1) + build_triangles(v2)
    return result