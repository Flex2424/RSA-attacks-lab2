#! /usr/bin/python3

from decimal import getcontext
from decimal import Decimal


def continued_fraction(exp, modulus):
    data = []

    while True:
        data.append(exp // modulus)
        f = modulus
        modulus = exp % modulus
        exp = f
        if modulus == 0:
            break
    return data


# Calculates continued fraction of length m for a / b
def continued_fraction(a, b, m, eps=200):
    getcontext().prec = eps
    x = Decimal(a) / Decimal(b)
    fraction = []
    fraction.append(int(x))
    xi = x - fraction[0]
    for i in range(m):
        try:
            ai = int(Decimal(1) / xi)
            xi = (Decimal(1) / xi) - ai
            fraction.append(ai)
            if xi < Decimal(1) / Decimal(10 ** (eps / 2)):
                break
        except Exception as ex:
            print('Error:', ex)
            break
    return fraction


# Calculates the convergent fractions
def convergent(fraction):
    p = []
    p.append(fraction[0])
    p.append(fraction[0] * fraction[1] + 1)
    q = []
    q.append(1)
    q.append(fraction[1])
    for k in range(2, len(fraction)):
        pk = p[k - 1] * fraction[k] + p[k - 2]
        p.append(pk)
        qk = q[k - 1] * fraction[k] + q[k - 2]
        q.append(qk)
    return p, q


msg = b'omg'
msg_int = int.from_bytes(msg, byteorder='big')

e = 60728973
n = 160523347


def wiener_attack():
    fraction = continued_fraction(e, n, 145)
    print('continued fraction:', fraction)
    p, q = convergent(fraction)
    # print(q)
    for i in range(len(q)):
        if pow(msg_int, e * q[i], n) == msg_int % n:
            d = q[i]
            return d


def main():
    d = wiener_attack()
    if d is not None:
        c = pow(msg_int, e, n)
        m = pow(c, d, n)
        print('d =', hex(d))
        print('message =', m.to_bytes(len(msg), byteorder='big'))
    else:
        print('d is not found')
    return d


if __name__ == '__main__':
    main()

