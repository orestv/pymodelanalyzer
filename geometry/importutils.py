# -*- coding: utf-8 -*
__author__ = 'seth'

from vector import Vector
from quad import Quad


def parse_vertex_line(line):
    coordinates = line.split()[1:]  # skip "v "
    if len(coordinates) != 3:
        raise ValueError(u'Точка %s містить недостатньо координат!' % line)
    x, y, z = coordinates
    try:
        x, y, z = float(x), float(y), float(z)
    except ValueError:
        raise ValueError(u'Невірний формат числа в рядку %s' % line)
    return Vector(x, y, z)


def parse_face_line(line):
    vertices = line.split()[1:]    # skip "f "
    if len(vertices) != 4:
        raise ValueError(u'Примітив %s - не чотирикутник!' % line)
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
    quads = build_quads(vertices, faces)
    return quads


def build_quads(vertices, faces):
    quads = []
    for face in faces:
        quad_vertices = [vertices[i] for i in face]
        quad = Quad(quad_vertices, normale=None)
        quads.append(quad)
    return quads
