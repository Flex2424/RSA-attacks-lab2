#! /usr/bin/python3

import gmpy2
from Crypto.Cipher import DES
from parser import ASN1
from chinese_remainder_theorem import crt

FILENAME = 'lab3var9.efn'


asn = ASN1()
asn.parse_file(FILENAME)
# result will be store in binary file cipher

params1 = (
    asn.decoded_values[0],
    asn.decoded_values[1],
    asn.decoded_values[2]
)

params2 = (
    asn.decoded_values[3],
    asn.decoded_values[4],
    asn.decoded_values[5]
)
params3 = (
    asn.decoded_values[6],
    asn.decoded_values[7],
    asn.decoded_values[8]
)

# use crt for restored params
m = (params1[0], params2[0], params3[0])
a = (params1[2], params2[2], params3[2])

x = crt(m, a)
# use gmpy2 for nth root
gmpy2.get_context().precision = 200
m = int(gmpy2.root(x, params1[1]))

key = m.to_bytes(8, byteorder='big')
des = DES.new(key, DES.MODE_ECB)

decrypted_text = bytes()
with open('cipher', 'rb') as file:
    while True:
        block = file.read(DES.block_size)
        if len(block) == 0:
            break
        if len(block) % DES.block_size != 0:
            block += b'\x03' * (DES.block_size - len(block) % DES.block_size)
        decrypted_text += des.decrypt(block)

with open('output', 'wb') as file:
    file.write(decrypted_text)





