"""
Implements Simplified DES (SDES), as descibed in the paper:
http://mercury.webster.edu/aleshunas/COSC%205130/G-SDES.pdf

Written by Christian Stigen

The SDES paper counts bit from the MSB, which is unusual. I.e., what would
normally be called bit 10 (i.e. 0x200) is in the paper denoted bit 1.

For the permutation functions, we could easily write a loop, but I would guess
that if the number of permutation function is finite, they'd be implemented
with raw values, in C, because of speed (pipelining, cascading, branch
prediction, memory locality, etc.).
"""

import sys

def assert_nbit(n, bits):
    if n > ((1 << bits) - 1):
        raise ValueError("Value is larger than %d bits: %x" % (bits, n))

def assert_10bit(n):
    assert_nbit(n, 10)

def assert_8bit(n):
    assert_nbit(n, 8)

def assert_4bit(n):
    assert_nbit(n, 4)

def encrypt(key, plaintext):
    k1, k2 = create_subkeys(key)
    return revip(f(k2, sw(f(k1, ip(plaintext)))))

def decrypt(key, ciphertext):
    k1, k2 = create_subkeys(key)
    return revip(f(k1, sw(f(k2, ip(ciphertext)))))

def p10(key):
    """P10 permutation."""
    assert_10bit(key)
    out = 0
    out |= (key & 0b0010000000) << 2 # bit 3
    out |= (key & 0b0000100000) << 3 # bit 5
    out |= (key & 0b0100000000) >> 1 # bit 2
    out |= (key & 0b0000001000) << 3 # bit 7
    out |= (key & 0b0001000000) >> 1 # bit 4
    out |= (key & 0b0000000001) << 4 # bit 10
    out |= (key & 0b1000000000) >> 6 # bit 1
    out |= (key & 0b0000000010) << 1 # bit 9
    out |= (key & 0b0000000100) >> 1 # bit 8
    out |= (key & 0b0000010000) >> 4 # bit 6
    return out

def p8(key):
    """See P10.

    Bits 1 and 2 (i.e., the first two MSBs) are untouched.
    """
    out = 0
    out |= (key & 0b0000010000) << 3 # bit 6
    out |= (key & 0b0010000000) >> 1 # bit 3
    out |= (key & 0b0000001000) << 2 # bit 7
    out |= (key & 0b0001000000) >> 2 # bit 4
    out |= (key & 0b0000000100) << 1 # bit 8
    out |= (key & 0b0000100000) >> 3 # bit 5
    out |= (key & 0b0000000001) << 1 # bit 10
    out |= (key & 0b0000000010) >> 1 # bit 9
    return out

def ip(key):
    assert_8bit(key)
    out = 0
    out |= (key & 0b01000000) << 1 # bit 2
    out |= (key & 0b00000100) << 4 # bit 6
    out |= (key & 0b00100000)      # bit 3
    out |= (key & 0b10000000) >> 3 # bit 1
    out |= (key & 0b00010000) >> 1 # bit 4
    out |= (key & 0b00000001) << 2 # bit 8
    out |= (key & 0b00001000) >> 2 # bit 5
    out |= (key & 0b00000010) >> 1 # bit 7
    return out

def revip(key):
    """The reverse of IP."""
    assert_8bit(key)
    out = 0
    out |= (key & 0b00010000) << 3 # bit 4
    out |= (key & 0b10000000) >> 1 # bit 1
    out |= (key & 0b00100000)      # bit 3
    out |= (key & 0b00001000) << 1 # bit 5
    out |= (key & 0b00000010) << 2 # bit 7
    out |= (key & 0b01000000) >> 4 # bit 2
    out |= (key & 0b00000001) << 1 # bit 8
    out |= (key & 0b00000100) >> 2 # bit 6
    return out

def shiftl5(n):
    """Rotate the MSB and LSB 5 bits individually one position to the left."""
    assert_10bit(n)

    # Mask
    msb5 = (n & 0b1111100000) >> 5
    lsb5 = (n & 0b0000011111)

    # Rotate
    carry = (msb5 & 0b10000) >> 4
    msb5 = ((msb5 << 1) & 0b11110) | carry

    carry = (lsb5 & 0b10000) >> 4
    lsb5 = ((lsb5 << 1) & 0b11110) | carry

    return (msb5 << 5) | lsb5

def create_subkeys(key):
    """Key generation for Simplified DES.

    See figure G.2 in the paper.
    """
    assert_10bit(key)

    k2 = shiftl5(p10(key))
    k1 = p8(k2)
    k2 = p8(shiftl5(shiftl5(k2)))
    return k1, k2

def sw(n):
    """Interchanges the upper and lower 4 bits."""
    assert_8bit(n)
    return ((n & 0b11110000) >> 4) | ((n & 0b1111) << 4)

def p4(n):
    assert_4bit(n)
    return ((n & 0b0100) << 1  # bit 2
          | (n & 0b0001) << 2  # bit 4
          | (n & 0b0010)       # bit 3
          | (n & 0b1000) >> 3) # bit 1

def S0(a,b):
    """S-box S0."""
    box = (
        (1, 0, 3, 2),
        (3, 2, 1, 0),
        (0, 2, 1, 3),
        (3, 1, 3, 2),
    )
    return box[a][b]

def S1(a,b):
    """S-box S1."""
    box = (
        (0, 1, 2, 3),
        (2, 0, 1, 3),
        (3, 0, 1, 0),
        (2, 1, 0, 3),
    )
    return box[a][b]

def ep(n):
    """Expansion/Permutation operation (E/P).

    Takes 4-bit input, returns 8-bit output.
    """
    assert_4bit(n)
    out = 0
    out |= (n & 0b00000001) << 7 # bit 4
    out |= (n & 0b00001000) << 3 # bit 1
    out |= (n & 0b00000100) << 3 # bit 2
    out |= (n & 0b00000010) << 3 # bit 3
    out |= (n & 0b00000100) << 1 # bit 2
    out |= (n & 0b00000010) << 1 # bit 3
    out |= (n & 0b00000001) << 1 # bit 4
    out |= (n & 0b00001000) >> 3 # bit 1
    return out

def Fmap(n, subkey):
    """4-bit mapping function."""
    assert_4bit(n)
    assert_8bit(subkey)

    n = ep(n)

    n4 = (n & 0b10000000) >> 7
    n1 = (n & 0b01000000) >> 6
    n2 = (n & 0b00100000) >> 5
    n3 = (n & 0b00010000) >> 4

    k11 = (subkey & 0b10000000) >> 7
    k12 = (subkey & 0b01000000) >> 6
    k13 = (subkey & 0b00100000) >> 5
    k14 = (subkey & 0b00010000) >> 4
    k15 = (subkey & 0b00001000) >> 3
    k16 = (subkey & 0b00000100) >> 2
    k17 = (subkey & 0b00000010) >> 1
    k18 = (subkey & 0b00000001)

    p00 = n4 ^ k11
    p01 = n1 ^ k12
    p02 = n2 ^ k13
    p03 = n3 ^ k14

    p10 = n2 ^ k15
    p11 = n3 ^ k16
    p12 = n4 ^ k17
    p13 = n1 ^ k18

    row1 = (p00 << 3) | (p01 << 2) | (p02 << 1) | p03
    row2 = (p10 << 3) | (p11 << 2) | (p12 << 1) | p13

    a = S0((row1 & 0b1100) >> 2, (row1 & 0b11))
    b = S1((row2 & 0b1100) >> 2, (row2 & 0b11))
    #a = S0((row1 & 0b11), (row1 & 0b1100) >> 2)
    #b = S1((row2 & 0b11), (row2 & 0b1100) >> 2)

    return p4(a << 2 | b)

def f(sk, n):
    assert_8bit(n)

    l = (n & 0b11110000) >> 4
    r = (n & 0b00001111)

    return (l ^ Fmap(r, sk)) << 4 | r

def testenc(key, plaintext, expected):
    ciphertext = encrypt(key, plaintext)
    sys.stdout.write("key %12s  plain %10s  cipher %10s" % (bin(key), bin(plaintext),
        bin(ciphertext)))

    if ciphertext == expected:
        sys.stdout.write("  OK\n")
        return True
    else:
        sys.stdout.write("  FAIL, expected %10s\n" % bin(expected))
        return False

def test(func, arg, expected):
    label = func.__name__
    actual = func(arg)
    ok = actual == expected

    print("%s %s(%s) => %s (%d) expected %s (%d) " % (
        "OK  " if ok else "FAIL",
        label, bin(arg), bin(actual), actual,
        bin(expected), expected))

def testall():
    k = 0b1010000010
    test(p10, k, 0b1000001100)
    test(shiftl5, p10(k), 0b0000111000)
    test(p8, shiftl5(p10(k)), 0b10100100)

    def ip_revip(k):
        return revip(ip(k))

    test(ip_revip, 0xf3, 0xf3)
    test(ip_revip, 0x07, 0x07)

    def subkey1(n):
        return create_subkeys(n)[0]
    def subkey2(n):
        return create_subkeys(n)[1]
    test(subkey1, k, 0b10100100)
    test(subkey2, k, 0b01000011)

    print("")
    testenc(0b0000000000, 0b10101010, 0b00010001)
    testenc(0b1110001110, 0b10101010, 0b11001010)
    testenc(0b1110001110, 0b01010101, 0b01110000)
    testenc(0b1111111111, 0b10101010, 0b00000100)

if __name__ == "__main__":
    testall()
