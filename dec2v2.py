"""
Part II task 3, second message
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

# Consider the triplesdes_decrypt function body:
#
#     return decrypt(k1, encrypt(k2, decrypt(k1, c)))
#
# The LAST call is decrypt(k1, byte) here. We are only interested in the input
# bytes that produce printable ASCII. So let's iterate through all (k1, byte)
# pairs and keep track of which ones produce ASCII output.
dec2ascii = collections.defaultdict(set)
for k1 in range(2**10):
    for byte in range(256):
        if 32 <= decrypt(k1, byte) <= 126:
            dec2ascii[k1].add(byte)

# Now start with the FIRST TWO calls in the triplesdes_decrypt chaing above:
# encrypt(k2, decrypt(k1, cipher_byte)). For all unique cipher bytes, this must
# produce a (k1, decrypted_byte) that is in dec2ascii, or else it won't produce
# an ASCII output. Consequently, those (k1, k2) pairs that don't produce ASCII
# for all cipher bytes can be thrown away.
for k1, good in dec2ascii.items():
    # Precalculate FIRST call decrypt(k1, cipher_byte).
    decr = map(lambda c: decrypt(k1, c), unique)
    for k2 in range(2**10):
        try:
            for byte in decr:
                out = encrypt(k2, byte)
                if out not in good:
                    raise RuntimeError()
        except RuntimeError:
            removed.add((k1 << 10) | k2)
            continue
#for key in keys:
    #k1, k2 = split_key(key)
    #for byte in unique:
        #out = decrypt(k1, encrypt(k2, decrypt(k1, byte)))
        #if not (32 <= out <= 126):
            #removed.add(key)
            #break
print("Removing %d keys" % len(removed))
keys -= removed

print("Possible keys: %d" % len(keys))

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