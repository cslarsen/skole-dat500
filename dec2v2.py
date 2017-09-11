"""
Part II task 3, second message

Optimized version of dec2.py. This runs in 0.7 secs in pypy and 10 secs in
ordinary python 2.7

The original version ran on 2.5 seconds on pypy and 1.5 minutes on python.
I was first able to optimize that down to 1.6s pypy and 30s python. This
version takes 0.56s pypy and ~10s python. I believe it is possible to optimize
it further.
"""

from util import *
from sdes import *
import collections

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

cipher = map(lambda c: int(c, 2), split_string(cipher_raw, 8))
unique = set(cipher)

badk1s = set()
badk2s = set()
removed = set()

# Create a decrypt map and ALSO:
#
# Consider the triplesdes_decrypt function body:
#
#     return decrypt(k1, encrypt(k2, decrypt(k1, c)))
#
# The LAST call is decrypt(k1, byte) here. We are only interested in the input
# bytes that produce printable ASCII. So let's iterate through all (k1, byte)
# pairs and keep track of which ones produce ASCII output.
decrypt_map = [[0]*256]*(2**10)
dec2ascii = collections.defaultdict(set)
for k in range(2**10):
    for byte in range(256):
        out = decrypt(k, byte)
        decrypt_map[k][byte] = out
        if 32 <= out <= 126:
            dec2ascii[k].add(byte)

# Create map of middle layer
encrypt_map = [[0]*256]*(2**10)
for k in range(2**10):
    for byte in range(256):
        # NOTE: This maps k2 values. Perhaps we can do everything here? Find
        # (k2, byte) pairs that produce ascii??
        encrypt_map[k][byte] = encrypt(k, byte)

# Now start with the FIRST TWO calls in the triplesdes_decrypt chaing above:
# encrypt(k2, decrypt(k1, cipher_byte)). For all unique cipher bytes, this must
# produce a (k1, decrypted_byte) that is in dec2ascii, or else it won't produce
# an ASCII output. Consequently, those (k1, k2) pairs that don't produce ASCII
# for all cipher bytes can be thrown away.

# Number of key pairs left to try
keypairs_left = 2**20

try:
    for k1, produces_ascii in dec2ascii.items():
        # Precalculate FIRST call decrypt(k1, cipher_byte).
        decrypted_k1_cipherbytes = map(lambda c: decrypt_map[k1][c], unique)
        for k2 in range(2**10):
            try:
                for byte in decrypted_k1_cipherbytes:
                    out = encrypt_map[k2][byte]
                    if out not in produces_ascii:
                        raise RuntimeError()
            except RuntimeError:
                removed.add((k1 << 10) | k2)
                keypairs_left -= 1

                # This breaks early, but has no effect on the keys for this
                # assignment. It would be slightly faster if key1 was a low number
                # like 0x60. Leaving it here just to show that this is possible.
                if keypairs_left <= 1:
                    raise RuntimeError()
except RuntimeError:
    pass

print("Removing %d unsuitable 20-bit keys" % len(removed))
keys -= removed

print("Number of possible 20-bit keys: %d" % len(keys))

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
