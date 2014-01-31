__author__ = 'seth'

import pstats

if __name__ == '__main__':
    p = pstats.Stats('profile_stats')
    p.strip_dirs().sort_stats('cumulative').print_stats(20)