# -*- coding: utf-8 -*
__author__ = 'seth'

import logging
import sys

from vector import Vector
import geometryutils

logger = logging.getLogger('ImportUtils')
logger.addHandler(logging.StreamHandler(sys.stdout))


def parse_vertex_line(line):
    coordinates = line.split()[1:]  # skip "v "
    if len(coordinates) != 3:
        raise ValueError('Точка %s містить невірну кількість координат!' % line)
    try:
        coordinates = map(float, coordinates)
    # try:
    #     x, y, z = map(lambda s: BigFloat.exact(s, precision=50), (x, y, z))
    except ValueError:
        raise ValueError('Невірний формат числа в рядку %s' % line)
    return Vector(*coordinates)


def parse_face_line(line):
    vertices = line.split()[1:]    # skip "f "
    vertex_indices = []
    if len(vertices) < 3:
        raise ValueError('Рядок %s містить недостатньо вершин.' % line)
    for vertex_data in vertices:
        vertex_index = vertex_data.split('/')[0]
        vertex_index = int(vertex_index)-1  # indices in the file start with 1
        vertex_indices.append(vertex_index)
    return vertex_indices


def get_faces(path, update_percentage=None, check_cancelled=None):
    vertices = []
    faces = []
    with open(path, 'r') as objfile:
        lines = objfile.readlines()
    logger.debug('File read.')
    line_number = 0
    last_percentage = 0
    for line in lines:
        if update_percentage:
            percentage = int(100 * float(line_number) / len(lines))
            if percentage != last_percentage:
                update_percentage(percentage)
                last_percentage = percentage
                if check_cancelled:
                    check_cancelled()
        line_number += 1
        if line.startswith('v '):
            vertices.append(parse_vertex_line(line))
        elif line.startswith('f '):
            faces.append(parse_face_line(line))
    if update_percentage:
        update_percentage(100)
    logger.debug('Face and vertex lists created.')
    return [[vertices[i] for i in face] for face in faces]


def build_triangles(faces, update_percentage=None, check_cancelled=None):
    triangles = []
    processed_faces = 0
    previous_percentage = None
    for face in faces:
        if check_cancelled:
            check_cancelled()
        if update_percentage:
            processed_faces += 1
            if processed_faces % 100 == 0:
                percentage = int(float(processed_faces) / len(faces) * 100)
                if previous_percentage != percentage:
                    update_percentage(percentage)
                    previous_percentage = percentage
        triangles += geometryutils.build_triangles(face)
    return triangles


def analyze_file(path):
    vertex_count, face_count, lines_count = 0, 0, 0
    with open(path, 'r') as objfile:
        for line in objfile:
            lines_count += 1
            if line.startswith('v '):
                vertex_count += 1
            elif line.startswith('f '):
                face_count += 1
    return vertex_count, face_count, lines_count
