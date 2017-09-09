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

def test():
    assert(encrypt(key=0b0000000000, plaintext=0b10101010) == 0b00010001)
    assert(encrypt(key=0b1110001110, plaintext=0b10101010) == 0b11001010)
    assert(encrypt(key=0b1110001110, plaintext=0b01010101) == 0b01110000)
    assert(encrypt(key=0b1111111111, plaintext=0b10101010) == 0b00000100)

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
    return revip(f(k2, sw(f(k1, ip(plaintext)))))

def decrypt(key, ciphertext):
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

def sw(x):
    return x

def p4(n):
    assert_4bit(n)
    return ((n & 0b0100) << 1  # bit 2
          | (n & 0b0001) << 2  # bit 4
          | (n & 0b0010)       # bit 3
          | (n & 0b1000) >> 3) # bit 1

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
    return n

def f(k, n):
    assert_8bit(n)

    l = (n & 0b11110000) >> 4
    r = (n & 0b00001111)

    sk = 123
    return (l ^ Fmap(r, sk)) << 4 | r

if __name__ == "__main__":
    key = 0b1010000010
    k1, k2 = create_subkeys(key)
    plaintext = 0b10101010
    ciphertext = encrypt(key, plaintext)
    print("key=%s plaintext=%s ciphertext=%s" % (bin(key), bin(plaintext),
        bin(ciphertext)))
