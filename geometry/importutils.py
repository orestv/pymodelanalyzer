# -*- coding: utf-8 -*
__author__ = 'seth'

from bigfloat import BigFloat

from vector import Vector
from quad import Quad
import geometryutils


def parse_vertex_line(line):
    coordinates = line.split()[1:]  # skip "v "
    if len(coordinates) != 3:
        raise ValueError('Точка %s містить невірну кількість координат!' % line)
    x, y, z = coordinates
    try:
        x, y, z = map(lambda s: BigFloat.exact(s, precision=50), (x, y, z))
    except ValueError:
        raise ValueError('Невірний формат числа в рядку %s' % line)
    return Vector(x, y, z)


def parse_face_line(line):
    vertices = line.split()[1:]    # skip "f "
    vertex_indices = []
    for vertex_data in vertices:
        vertex_index = vertex_data.split('/')[0]
        vertex_index = int(vertex_index)-1  # indices in the file start with 1
        vertex_indices.append(vertex_index)
    return vertex_indices


def import_obj(path):
    vertices = []
    faces = []
    with open(path, 'r') as objfile:
        for line in objfile:
            if line.startswith('v '):
                vertices.append(parse_vertex_line(line))
            elif line.startswith('f '):
                faces.append(parse_face_line(line))
    triangles = []
    for face in faces:
        face_vertices = [vertices[i] for i in face]
        triangles += geometryutils.build_triangles(face_vertices)
    return triangles


def build_quads(vertices, faces):
    quads = []
    for face in faces:
        quad_vertices = [vertices[i] for i in face]
        quad = Quad(quad_vertices, normale=None)
        quads.append(quad)
    return quads
