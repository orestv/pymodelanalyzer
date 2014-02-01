__author__ = 'seth'


class CalculationParams(object):
    __slots__ = ('c', 'f', 'wavelength', 'viewpoint')

    def __init__(self, c, f, wavelength, viewpoint):
        self.c = c
        self.f = f
        self.wavelength = wavelength
        self.viewpoint = viewpoint
