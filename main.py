#!/usr/bin/env python2
# -*- coding: utf-8 -*
__author__ = 'seth'

from argparse import ArgumentParser
import sys

from bigfloat import BigFloat

from geometry import importutils
from processing import processor
from geometry.vector import Vector


def parse_options():
    parser = ArgumentParser(description=u'Обчислення параметрів моделі.')

    parser.add_argument('input_file', type=str,
                        help=u'Повний шлях до .obj-файла моделі')
    parser.add_argument('-w', '--wavelength',
                        type=BigFloat, required=True,
                        help=u'Довжина хвилі')
    parser.add_argument('-op', '--observation_point',
                        type=float, nargs=3, required=True,
                        metavar=(u'x', u'y', u'z'),
                        help=u'Координати точки спостереження')
    parser.add_argument('-o', '--output_file', type=str,
                        default='output.csv',
                        help=u'Шлях до файла, куди буде збережно результат.')

    args = parser.parse_args()
    return args


def generate_notify_func(message):
    progress_string = '\r%s %%d%%%% завершено.' % message

    def notify_func(percentage):
        sys.stdout.write(progress_string % percentage)
        if percentage == 100:
            sys.stdout.write('\n')
        sys.stdout.flush()

    return notify_func


def main():
    args = parse_options()
    viewpoint = args.observation_point
    viewpoint = Vector(*viewpoint)
    vertex_count, face_count, lines_count = importutils.analyze_file(args.input_file)
    print 'Кількість вершин: %d, кількість примітивів: %d' % (vertex_count, face_count)
    faces = importutils.get_faces(args.input_file)
    print 'Файл імпортовано.'
    triangles = importutils.build_triangles(faces, generate_notify_func('Обробка трикутників...'))
    print 'Трикутники згенеровано.'

    processor.write_triangles_data(triangles, viewpoint, args.wavelength, args.output_file)
    print 'Модель оброблено, дані збережено в %s.' % args.output_file


if __name__ == '__main__':
    main()
