#! /usr/bin/python3

# code from https://github.com/Airy-Fairy/CryptLabs/blob/master/CryptLab2/crt.py

from functools import reduce
from operator import mul, mod
from decimal import getcontext
from decimal import Decimal


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def crt(m, a):
    getcontext().prec = 300
    # the product of m elements
    M = reduce(mul, m)
    m_i = [Decimal(M) / Decimal(item) for item in m]
    b = map(mod, m_i, m)
    g, k, l = map(egcd, b, m)
    # transpose g, k and l arrays
    g, k, l = zip(g, k, l)
    t = map(mod, k, m)
    e = map(mul, m_i, t)

    x_sum = sum(map(mul, a, e))
    x = x_sum % M

    return x if x > 0 else x + M


# if __name__ == '__main__':
#     m = (31, 32, 33)
#     a = (14, 16, 18)
#
#     print('Result: {0}'.format(crt(m, a)))
