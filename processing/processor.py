__author__ = 'seth'

import os
import math
import logging

from geometry import geometryutils

EPS = 0.001

logger = logging.getLogger('processor')
logger.addHandler(logging.FileHandler('processor.log'))


def get_triangle_leg_angles(triangle_normale, view_vector, plane_normale):
    view_vector_projection = geometryutils.get_projection_onto_plane(view_vector, plane_normale)
    alpha = geometryutils.sharp_angle(view_vector_projection, triangle_normale)
    beta = geometryutils.sharp_angle(view_vector, view_vector_projection)

    return alpha, beta


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

    alpha_1, beta_1 = get_triangle_leg_angles(triangle.normale, view_vector, triangle.leg_2)
    alpha_2, beta_2 = get_triangle_leg_angles(triangle.normale, view_vector, triangle.leg_1)

    angles = {}
    if abs(triangle.leg_1.length - triangle.leg_2.length) < EPS:
        alpha = min(alpha_1, alpha_2)
        beta = min(beta_1, beta_2)
    elif triangle.leg_1 < triangle.leg_2:
        alpha, beta = alpha_1, beta_1
    else:
        alpha, beta = alpha_2, beta_2

    if alpha == 0 or beta == 0:
        raise ValueError('Triangle %s is perpendicular to view vector.' % triangle)

    a = min(triangle.leg_1.length, triangle.leg_2.length)
    b = max(triangle.leg_1.length, triangle.leg_2.length)

    f = get_f(alpha, beta, a, b, wavelength)

    result = {
        'a': a,
        'b': b,
        'alpha': angles['alpha'],
        'beta': angles['beta'],
        'f': f
    }

    return result


def get_triangle_properties(triangle, viewpoint):
    view_vector = triangle.vertex - viewpoint
    alpha_1, beta_1 = get_triangle_leg_angles(triangle.normale, view_vector, triangle.leg_2)
    alpha_2, beta_2 = get_triangle_leg_angles(triangle.normale, view_vector, triangle.leg_1)

    if abs(triangle.leg_1.length - triangle.leg_2.length) < EPS:
        alpha = min(alpha_1, alpha_2)
        beta = min(beta_1, beta_2)
    elif triangle.leg_1 < triangle.leg_2:
        alpha, beta = alpha_1, beta_1
    else:
        alpha, beta = alpha_2, beta_2

    if alpha == 0 or beta == 0:
        print triangle.normale, view_vector, view_vector.unit()
        print alpha_1, beta_1, alpha_2, beta_2
        print triangle.leg_1, triangle.leg_1.unit(), triangle.leg_2, triangle.leg_2.unit()
        raise ValueError('Triangle %s is perpendicular to view vector.' % triangle)

    a = min(triangle.leg_1.length, triangle.leg_2.length)
    b = max(triangle.leg_1.length, triangle.leg_2.length)

    return alpha, beta, a, b


def try_process_triangle(args):
    triangle, viewpoint, wavelength = args
    data = None
    try:
        data = process_triangle(viewpoint, wavelength, triangle)
    except ValueError as ex:
        logger.warn('Failed to process triangle %s: %s', triangle, ex)
    return data


def write_triangles_data(data, path):
    string_output = ['%.8f;%.8f;%.8f;%.8f;%.8f%s' % (d['a'], d['b'], d['alpha'], d['beta'], d['f'], os.linesep)
                     for d in data]
    with open(path, 'wb') as output_file:
        output_file.writelines(string_output)


def frange(a, b, step):
    if a >= b:
        raise ValueError('a cannot be smaller than b.')
    x = a
    while x < b:
        yield x
        x += step


def calculate_viewpoint_sums(triangles, wavelength, viewpoint,
                             update_percentage=None,
                             check_cancelled=None):
    k = 2 * math.pi / wavelength
    sum_cos = 0
    sum_sin = 0
    processed_triangles = 0
    last_percentage = -1
    if update_percentage:
        update_percentage(0)
    for t in triangles:
        e_n = calculate_En(t, wavelength, k, viewpoint)
        r_n = viewpoint.dist(t.vertex)
        sum_cos += e_n * math.cos(k * r_n)
        sum_sin += e_n * math.sin(k * r_n)

        if update_percentage:
            processed_triangles += 1
            percentage = int(100 * float(processed_triangles) / len(triangles))
            if percentage != last_percentage or True:
                update_percentage(percentage)
                last_percentage = percentage
                check_cancelled()
    return pow(sum_cos ** 2 + sum_sin ** 2, 0.5), sum_cos, sum_sin


def calculate_En(triangle, wavelength, k, viewpoint):
    alpha, beta, a, b = get_triangle_properties(triangle, viewpoint)

    sina, cosa, sinb, cosb = math.sin(alpha), math.cos(alpha), \
                             math.sin(beta), math.cos(beta)

    sigma = 4 * math.pi * (alpha ** 2) * (beta ** 2) / (wavelength ** 2)

    if abs(alpha) < EPS and abs(beta) < EPS:
        e_n = sigma
    elif abs(beta) < EPS:
        e_n = sigma * cosa ** 2 * \
              (math.sin(k * alpha * cosa) /
               k * alpha * sina) ** 4
    elif abs(alpha) < EPS:
        e_n = sigma * cosb ** 2 * \
              (((math.sin(k * b * sinb)) / (k * b * sinb)) ** 4 +
               ((1 - math.sin(2 * k * b * sinb / (2 * k * b * sinb)))
                / (k * b * sinb)) ** 2)
    else:
        e_n = ((sigma * (cosa * cosb) ** 2) /
               ((k * a * sina * cosb) ** 2 -
                (k * b * sinb) ** 2) ** 2) * \
              (math.sin(k * a * sina * cosb) ** 2 -
               (math.sin(k * b * sinb) ** 2 +
                (k * b * sinb) ** 2) * (
                   ((math.sin(2 * k * a * sina * cosb)) /
                    (2 * k * a * sina * cosb) -
                    (math.sin(2 * k * b * sinb)) /
                    (2 * k * b * sinb)) ** 2
               ))
    return e_n
