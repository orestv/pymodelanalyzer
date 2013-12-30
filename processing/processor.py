__author__ = 'seth'

import os
import math
import logging

from geometry import geometryutils

VECTOR_EQUALITY_EPS = 0.001

logger = logging.getLogger('processor')
logger.addHandler(logging.FileHandler('processor.log'))


def get_triangle_leg_angles(triangle_normale, view_vector, plane_normale):
    view_vector_projection = geometryutils.get_projection_onto_plane(view_vector, plane_normale)
    alpha = geometryutils.sharp_angle(view_vector_projection, triangle_normale)
    beta = geometryutils.sharp_angle(view_vector, view_vector_projection)

    return {'alpha': alpha, 'beta': beta}


def get_f(alpha, beta, a, b, wavelength):
    cosa = math.cos(alpha)
    cosb = math.cos(beta)
    sina = math.sin(alpha)
    sinb = math.sin(beta)

    sigma = 4 * math.pi * (a ** 2) * (b ** 2) / (wavelength ** 2)
    k = 2 * math.pi / wavelength

    f = (sigma * (cosa * cosb) ** 2 /
         ((k * a * sina * cosb) ** 2 -
          (k * b * sinb) ** 2) ** 2) * \
        ((math.sin(k * a * sina * cosb) ** 2 -
          math.sin(k * b * sinb) ** 2) ** 2 +
         (k * b * sinb) ** 2 *
         (((math.sin(2 * k * a * sina * cosb)) /
           (2 * k * a * math.sin(a) * cosb)) -
          ((math.sin(2 * k * b * sinb)) /
           (2 * k * b * sinb))) ** 2)

    return f


def process_triangle(viewpoint, wavelength, triangle):
    view_vector = triangle.vertex - viewpoint

    # we need to project stuff onto the smaller leg's plane;
    # use the longer leg as the plane's normale

    angles_1 = get_triangle_leg_angles(triangle.normale, view_vector, triangle.leg_2)
    angles_2 = get_triangle_leg_angles(triangle.normale, view_vector, triangle.leg_1)

    angles = {}
    if abs(triangle.leg_1.length - triangle.leg_2.length) < VECTOR_EQUALITY_EPS:
        angles['alpha'] = min(angles_1['alpha'], angles_2['alpha'])
        angles['beta'] = min(angles_1['beta'], angles_2['beta'])
    elif triangle.leg_1 < triangle.leg_2:
        angles = angles_1
    else:
        angles = angles_2

    if angles['alpha'] == 0 or angles['beta'] == 0:
        raise ValueError('Triangle %s is perpendicular to view vector.' % triangle)

    a = min(triangle.leg_1.length, triangle.leg_2.length)
    b = max(triangle.leg_1.length, triangle.leg_2.length)

    f = get_f(angles['alpha'], angles['beta'], a, b, wavelength)

    result = {
        'a': a,
        'b': b,
        'alpha': angles['alpha'],
        'beta': angles['beta'],
        'f': f
    }

    return result


def try_process_triangle(args):
    triangle, viewpoint, wavelength = args
    data = None
    try:
        data = process_triangle(viewpoint, wavelength, triangle)
    except ValueError as ex:
        logger.warn('Failed to process triangle %s: %s', triangle, ex)
    return data


def write_triangles_data(data, path):
    string_output = ['%.8f,%.8f,%.8f,%.8f,%.8f%s' % (d['a'], d['b'], d['alpha'], d['beta'], d['f'], os.linesep)
                     for d in data]
    with open(path, 'w') as output_file:
        output_file.writelines(string_output)

