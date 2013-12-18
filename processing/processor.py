__author__ = 'seth'

import math

from geometry import geometryutils

VECTOR_EQUALITY_EPS = 0.1


def get_triangle_leg_angles(triangle_normale, view_vector, plane_normale):
    view_vector_projection = geometryutils.get_projection_onto_plane(view_vector, plane_normale)
    alpha = geometryutils.sharp_angle(view_vector_projection, triangle_normale)
    beta = geometryutils.sharp_angle(view_vector, view_vector_projection)

    return {'alpha': alpha, 'beta': beta}


def get_f(alpha, beta, a, b, wavelength):
    sigma = 4 * math.pi * (a ** 2) * (b ** 2) / (wavelength ** 2)
    k = 2 * math.pi / wavelength

    f = (sigma * (math.cos(alpha) * math.cos(beta)) ** 2 /
         ((k * a * math.sin(alpha) * math.cos(beta)) ** 2 -
          (k * b * math.sin(beta)) ** 2) ** 2) * \
        ((math.sin(k * a * math.sin(alpha) * math.cos(beta)) ** 2 -
          math.sin(k * b * math.sin(beta)) ** 2) ** 2 + \
         (k * b * math.sin(beta)) ** 2 * \
         (((math.sin(2 * k * a * math.sin(alpha) * math.cos(beta))) /
           (2 * k * a * math.sin(a) * math.cos(beta))) - \
          ((math.sin(2 * k * b * math.sin(beta))) /
           (2 * k * b * math.sin(beta)))) ** 2)

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

