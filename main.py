#!/usr/bin/env python2
# -*- coding: utf-8 -*
__author__ = 'seth'

from argparse import ArgumentParser
from multiprocessing import Pool
from itertools import chain

from geometry import importutils
from processing import processor
from geometry.vector import Vector
from geometry import geometryutils


DEFAULT_JOBS = 4


def parse_options():
    parser = ArgumentParser(description=u'Обчислення параметрів моделі.')

    parser.add_argument('input_file', type=str,
                        help=u'Повний шлях до .obj-файла моделі')
    parser.add_argument('-w', '--wavelength',
                        type=float, required=True,
                        help=u'Довжина хвилі')
    parser.add_argument('-op', '--observation_point',
                        type=float, nargs=3, required=True,
                        metavar=(u'x', u'y', u'z'),
                        help=u'Координати точки спостереження')
    parser.add_argument('-j', '--jobs',
                        type=int, help=u'Кількість потоків',
                        default=DEFAULT_JOBS)
    parser.add_argument('-o', '--output_file', type=str,
                        default='output.csv', required=True,
                        help=u'Шлях до файла, куди буде збережно результат.')

    args = parser.parse_args()
    return args


def main():
    args = parse_options()
    viewpoint = args.observation_point
    viewpoint = Vector(*viewpoint)
    vertex_count, face_count, lines_count = importutils.analyze_file(args.input_file)
    print 'Vertices: %d, Primitives: %d' % (vertex_count, face_count)
    faces = importutils.get_faces(args.input_file)
    print 'File imported.'

    pool = Pool(args.jobs)
    try:
        result = pool.map_async(geometryutils.build_triangles, faces, 10000)
    except KeyboardInterrupt:
        pool.terminate()
        print 'Program stopped.'
        return
    triangles = result.get()

    triangles = chain.from_iterable(triangles)

    print 'Triangles generated.'

    try:
        process_data = ((t, viewpoint, args.wavelength) for t in triangles)
        result = pool.map_async(processor.try_process_triangle, process_data)
    except KeyboardInterrupt:
        pool.terminate()
        print 'Program stopped.'
        return
    data = result.get()
    data = filter(lambda x: x, data)
    print 'Model processed.'
    processor.write_triangles_data(data, args.output_file)
    print 'Data written into %s' % args.output_file


if __name__ == '__main__':
    main()
