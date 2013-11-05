__author__ = 'seth'

import math
from geometry.vector import Vector

def vector_product(v1, v2):
    pass


def main():

    v_normal = Vector(1, 1, 1).get_normalized()
    v_spotter = Vector(50, 0, 0)

    print 'Normal vector length is %s, spotter vector length is %s' % \
          (v_normal.length, v_spotter.length)

    normalized = v_spotter.get_normalized()
    print normalized

    print 'Dot product is %d' % (v_normal * v_spotter)

    print 'Angle between vectors is %f' % math.degrees(v_spotter.angle(v_normal))


if __name__ == '__main__':
    main()

    pass
