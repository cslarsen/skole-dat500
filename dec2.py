"""
Part II task 3, second message
"""

from util import *
from sdes import *

cipher_raw = readfile("ctx2.txt")

# Require that all bytes are within the printable range, i.e.
# from 32 to 126 (inclusive)

# Keep a list of possible keys, then remove from that list once one byte gives
# a value outside the printable range

# two 10-bit keys, or 20 bits
keys = set(range(2**20))

def is_printable(char):
    return 32 <= ord(char) <= 126

def split_key(key):
    return (key & 0xffc00) >> 10, key & 0x3ff

print("Brute-forcing 10-bit key")
for char in split_string(cipher_raw, 8):
    byte = int(char, 2)
    removed = set()
    for key in keys:
        k1, k2 = split_key(key)
        out = chr(triplesdes_decrypt(k1, k2, byte))
        if not is_printable(out):
            removed.add(key)
    keys -= removed
    if len(keys) <= 1:
        break

print("Possible keys:")
for key in keys:
    print(key)

if len(keys) == 1:
    key = list(keys)[0]
    k1, k2 = split_key(key)
    print("Decrypted:")
    print("Key 1: %d / 0x%x / %s" % (k1, k1, bin(k1)))
    print("Key 2: %d / 0x%x / %s" % (k2, k2, bin(k1)))
    cipher = "".join(map(lambda x: chr(int(x, 2)), split_string(cipher_raw, 8)))
    print("Cipher text: %r" % cipher)
    plain = "".join(map(lambda x: chr(triplesdes_decrypt(k1, k2, ord(x))), cipher))
    print("Plain: %r" % plain)
