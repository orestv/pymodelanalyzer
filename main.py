#!/usr/bin/env python2
# -*- coding: utf-8 -*
__author__ = 'seth'

from argparse import ArgumentParser
from geometry import importutils
from geometry import geometryutils
from geometry.vector import Vector


def parse_options():
    parser = ArgumentParser(description=u'Обчислення параметрів моделі.')

    parser.add_argument('input_file', type=str,
                        help=u'Повний шлях до .obj-файла моделі')
    parser.add_argument('-o', '--output_file', type=str,
                        help=u'Шлях до файла, куди буде збережно результат.')
    parser.add_argument('-op', '--observation_point',
                        type=float, nargs=3, required=True,
                        metavar=(u'x', u'y', u'z'),
                        help=u'Координати точки спостереження')
    parser.add_argument('-ov', '--observation_vector',
                        type=float, nargs=3,
                        metavar=(u'x', u'y', u'z'),
                        help=u'Вектор спостереження')

    args = parser.parse_args()
    return args


def main():
    args = parse_options()
    viewpoint = args.observation_point
    viewpoint = Vector(*viewpoint)
    triangles = importutils.import_obj(args.input_file)
    visible_triangles = geometryutils.get_visible_triangles(triangles, viewpoint)


if __name__ == '__main__':
    main()
