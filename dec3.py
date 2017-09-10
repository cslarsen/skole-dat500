"""
Part II task 3, second message

a second try to make it faster... idea is to start with the decryption formula

encrypt(k1, decrypt(k2, encrypt(k1, p)))

start from the left: encrypt(k1, char)
Map out all (k1, char) pairs that give printable output.

That map contains all possible k1 keys.

Now continue left-right then right-left and try to connect the dots, should
find a combo of k1 and k2 that is possible, and at last try each one
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

print("Precalc 1")
keys = set()
ciph = map(lambda x: int(x, 2), split_string(cipher_raw, 8))
uniqs = set(ciph)
print("uniqs: %d" % len(uniqs))

encpath = set()
k1s = set()
for k1 in range(2**10):
    for char in range(256):
        out = encrypt(k1, char)
        if 32 <= out <= 126:
            encpath.add((k1, char))
            k1s.add(k1)

print("enc combos: %d" % len(encpath))

decpath = set()
decbytes = set()
k2s = set()
for k1 in range(2**10):
    for char in uniqs:
        out = decrypt(k1, char)
        if (k1, out) in encpath:
            decbytes.add(out)
            decpath.add((k1, char))
            k2s.add(k1)

print("dec combos: %d" % len(decpath))
#return encrypt(k1, decrypt(k2, encrypt(k1, p)))

keys1 = set()
keys2 = set()

for k2 in k2s:
    for k1 in k1s:
        for byte in uniqs:
            out = encrypt(k1, byte)
            if out in decbytes:
                pass #print(k1,k2)
        # find a path that satisfies everything

# Now try the bytes we found, run encrypt() on it.. find a k1 that gives
# something that is in set
goodk1 = set()
for k1 in k1s:
    try:
        for byte in uniqs:
            out = encrypt(k1, byte)
            if out in decbytes:
                goodk1.add(k1)
            else:
                raise RuntimeError()
    except:
        continue

print("good k1: %r" % len(goodk1))
print("keys1: %r" % keys1)

if False:
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
