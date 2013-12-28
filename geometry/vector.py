__author__ = 'seth'

from bigfloat import BigFloat


class Vector(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self._length = self.__length

    def __lt__(self, other):
        return self.length < other.length

    def __str__(self):
        return '(%.2f, %.2f, %.2f)' % self.coordinates

    def __repr__(self):
        return '(%.2f, %.2f, %.2f)' % self.coordinates

    def __unicode__(self):
        return unicode(str(self))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __sub__(self, other):
        if isinstance(other, (int, long, float)):
            return self.scalar_sub(other)
        elif isinstance(other, Vector):
            return self.vector_sub(other)

    def __add__(self, other):
        x, y, z = self.x + other.x, self.y + other.y, self.z + other.z
        return Vector(x, y, z)

    def __div__(self, other):
        if isinstance(other, (int, long, float, BigFloat)):
            x, y, z = self.x / other, self.y / other, self.z / other
            return Vector(x, y, z)
        raise ValueError('Expected a number, found %s' % type(other))

    def __mul__(self, number):
        if not isinstance(number, (int, long, float, BigFloat)):
            raise ValueError('Expected a number, found %s' % type(number))
        x, y, z = self.x * number, self.y * number, self.z * number
        return Vector(x, y, z)

    @property
    def coordinates(self):
        return self.x, self.y, self.z

    @property
    def __length(self):
        len_square = self.x * self.x + self.y * self.y + self.z * self.z
        return pow(len_square, 0.5)

    @property
    def length(self):
        return self._length

    @property
    def is_normalized(self):
        return self.length == 1

    def unit(self):
        if self.length == 0:
            raise ValueError("Cannot normalize zero vector.")
        x, y, z = self.x / self.length, self.y / self.length, self.z / self.length
        return Vector(x, y, z)

    def scalar_add(self, number):
        x, y, z = self.x + number, self.y + number, self.z + number
        return Vector(x, y, z)

    def scalar_sub(self, number):
        return self.scalar_add(-number)

    def dot_product(self, other):
        result = self.x * other.x + self.y * other.y + self.z * other.z
        return result

    def vector_product(self, other):
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        return Vector(x, y, z)

    def vector_add(self, other):
        x, y, z = self.x + other.x, self.y + other.y, self.z + other.z
        return Vector(x, y, z)

    def vector_sub(self, other):
        x, y, z = self.x - other.x, self.y - other.y, self.z - other.z
        return Vector(x, y, z)