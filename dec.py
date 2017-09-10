from util import *
from sdes import *

cipher_raw = readfile("ctx1.txt")

# Require that all bytes are within the printable range, i.e.
# from 32 to 126 (inclusive)

# Keep a list of possible keys, then remove from that list once one byte gives
# a value outside the printable range

# 10-bit key
keys = set(range(1024))

def is_printable(char):
    return 32 <= ord(char) <= 126

print("Brute-forcing 10-bit key")
for char in split_string(cipher_raw, 8):
    byte = int(char, 2)
    removed = set()
    for key in keys:
        out = chr(decrypt(key, byte))
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
    print("Decrypted:")
    print("Key: %d / 0x%x / %s" % (key, key, bin(key)))
    cipher = "".join(map(lambda x: chr(int(x, 2)), split_string(cipher_raw, 8)))
    print("Cipher text: %r" % cipher)
    plain = "".join(map(lambda x: chr(decrypt(key, ord(x))), cipher))
    print("Plain: %r" % plain)
