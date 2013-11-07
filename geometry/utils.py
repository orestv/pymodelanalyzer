__author__ = 'seth'

from quad import Quad

def is_rectangle(quad):
    v1 = quad.vertices[1] - quad.vertices[2]
    v2 = quad.vertices[0] - quad.vertices[3]
    return v1.angle(v2) == 0 and v1.length == v2.length

def get_middle_perpendiculars(quad):
    a = (quad.vertices[0] + quad.vertices[1]) / 2
    b = (quad.vertices[1] + quad.vertices[2]) / 2
    c = (quad.vertices[2] + quad.vertices[3]) / 2
    d = (quad.vertices[3] + quad.vertices[0]) / 2

    d1 = a - c
    d2 = b - d
    return d1, d2