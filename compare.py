"""
Verifies that the C++ SDES implementation works by comparing with the working
Python version.
"""

import csdes
import sdes

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
