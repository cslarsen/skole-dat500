"""
Verifies that the C++ SDES implementation works by comparing with the working
Python version.
"""

import csdes
import sdes

for n in range(2**10):
    py = sdes.p10(n)
    cpp = csdes.p10(n)
    if cpp != py:
        raise RuntimeError("p10(0x%x) py=0x%x cpp=0x%x" % (n, py, cpp))
print("ok p10")

for n in range(2**10):
    py = sdes.p8(n)
    cpp = csdes.p8(n)
    if cpp != py:
        raise RuntimeError("p8(0x%x) py=0x%x cpp=0x%x" % (n, py, cpp))
print("ok p8")

for n in range(2**4):
    py = sdes.p4(n)
    cpp = csdes.p4(n)
    if cpp != py:
        raise RuntimeError("p4(0x%x) py=0x%x cpp=0x%x" % (n, py, cpp))
print("ok p4")

for n in range(2**8):
    py = sdes.ip(n)
    cpp = csdes.ip(n)
    if cpp != py:
        raise RuntimeError("ip(0x%x) py=0x%x cpp=0x%x" % (n, py, cpp))
print("ok ip")

for n in range(2**8):
    py = sdes.revip(n)
    cpp = csdes.revip(n)
    if cpp != py:
        raise RuntimeError("revip(0x%x) py=0x%x cpp=0x%x" % (n, py, cpp))
print("ok revip")

for n in range(2**8):
    py = sdes.ep(n)
    cpp = csdes.ep(n)
    if cpp != py:
        raise RuntimeError("ep(0x%x) py=0x%x cpp=0x%x" % (n, py, cpp))
print("ok ep")

# Check by converting C++ to tuple
for key in range(2**10):
    py = sdes.create_subkeys(key)

    cpp = csdes.create_subkeys(key)
    cpp = ((cpp & 0b11111111110000000000) >> 10,
            cpp & 0b00000000001111111111)

    if py != cpp:
        raise RuntimeError(
            "create_subkeys(key=0x%x) py=%r cpp=%r" % (key,
                py, cpp))
print("ok create_subkeys")

# Check by converting Python to 20-bit value
for key in range(2**10):
    py = sdes.create_subkeys(key)
    py = (py[0] << 10) | py[1]

    if py != cpp:
        raise RuntimeError(
            "create_subkeys(key=0x%x) py=%r cpp=%r" % (key,
                py, cpp))

for key in range(2**10):
    for plaintext in range(256):
        py = sdes.encrypt(key, plaintext)
        cpp = csdes.encrypt(key,plaintext)
        if py != cpp:
            raise RuntimeError(
                "encrypt(key=0x%x, plaintext=0x%x) py=0x%x cpp=0x%x" % (key,
                    plaintext, py, cpp))
