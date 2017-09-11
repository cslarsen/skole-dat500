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

for n in range(2**4):
    py = sdes.ep(n)
    cpp = csdes.ep(n)
    if cpp != py:
        raise RuntimeError("ep(0x%x) py=0x%x cpp=0x%x" % (n, py, cpp))
print("ok ep")

for n in range(2**10):
    py = sdes.shiftl5(n)
    cpp = csdes.shiftl5(n)
    if cpp != py:
        raise RuntimeError("shiftl5(0x%x) py=0x%x cpp=0x%x" % (n, py, cpp))
print("ok shiftl5")

for n in range(2**10):
    py = sdes.shiftl5(sdes.p10(n))
    cpp = csdes.shiftl5(sdes.p10(n))
    if cpp != py:
        raise RuntimeError("shiftl5(p10(0x%x)) py=0x%x cpp=0x%x" % (n, py, cpp))
print("ok shiftl5(p10)")

for n in range(2**10):
    py = sdes.p8(sdes.shiftl5(sdes.shiftl5(n)))
    cpp = csdes.p8(csdes.shiftl5(csdes.shiftl5(n)))
    if cpp != py:
        raise RuntimeError("p8-shiftl5-shiftl5(0x%x)) py=0x%x cpp=0x%x" % (n, py, cpp))
print("ok p8-shiftl5-shiftl5")

# Check by converting Python to 20-bit value
for key in range(2**10):
    py = sdes.create_subkeys(key)
    py = (py[0] << 10) | py[1]

    cpp = csdes.create_subkeys(key)

    if py != cpp:
        raise RuntimeError(
            "create_subkeys(key=0x%x) py=%r cpp=%r py-shift" % (key,
                py, cpp))
print("OK create_subkeys py-shift")

# Check by converting C++ to tuple
for key in range(2**10):
    py = sdes.create_subkeys(key)

    cpp = csdes.create_subkeys(key)
    cpp = ((cpp & 0b11111111110000000000) >> 10,
            cpp & 0b00000000001111111111)

    if py != cpp:
        raise RuntimeError(
            "create_subkeys(key=0x%x) py=%r cpp=%r cpp-shift" % (key,
                py, cpp))
print("ok create_subkeys cpp-shift")

for row in range(4):
    for col in range(4):
        py = sdes.S0(row, col)
        cpp = csdes.S0(row, col)
        if cpp != py:
            raise RuntimeError(
                "S0(row=0x%x, col=0x%x) py=%r cpp=%r" % (row, col, py, cpp))
print("ok S0")

for row in range(4):
    for col in range(4):
        py = sdes.S1(row, col)
        cpp = csdes.S1(row, col)
        if cpp != py:
            raise RuntimeError(
                "S1(row=0x%x, col=0x%x) py=%r cpp=%r" % (row, col, py, cpp))
print("ok S1")

for n in range(256):
    py = sdes.sw(n)
    cpp = csdes.sw(n)
    if cpp != py:
        raise RuntimeError("sw(0x%x) py=0x%x cpp=0x%x" % (n, py, cpp))
print("ok sw")

for n in range(2**4):
    for sk in range(256):
        py = sdes.Fmap(n, sk)
        cpp = csdes.Fmap(n, sk)
        if cpp != py:
            raise RuntimeError("Fmap(n=0x%x, sk=0x%x) py=0x%x cpp=0x%x" % (
                n, sk, py, cpp))
print("ok Fmap")

print("   start encrypt compare")
for key in range(2**10):
    for plaintext in range(256):
        py = sdes.encrypt(key, plaintext)
        cpp = csdes.encrypt(key, plaintext)
        if py != cpp:
            raise RuntimeError(
                "encrypt(key=0x%x, plaintext=0x%x) py=0x%x cpp=0x%x" % (key,
                    plaintext, py, cpp))
print("ok encrypt")

for sk in range(2**10):
    for n in range(256):
        py = sdes.f(sk, n)
        cpp = csdes.fK(sk, n)
        if cpp != py:
            raise RuntimeError("f(sk=0x%x, n=0x%x) py=0x%x cpp=0x%x" % ( sk, n,
                py, cpp))
print("ok f / fK")

print("   start decrypt compare")
for key in range(2**10):
    for ciphertext in range(256):
        py = sdes.decrypt(key, ciphertext)
        cpp = csdes.decrypt(key, ciphertext)
        if py != cpp:
            raise RuntimeError(
                "decrypt(key=0x%x, ciphertext=0x%x) py=0x%x cpp=0x%x" % (key,
                    ciphertext, py, cpp))
print("ok decrypt")
