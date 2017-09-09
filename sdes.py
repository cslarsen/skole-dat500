"""
Implements Simplified DES (SDES), as descibed in the paper:
http://mercury.webster.edu/aleshunas/COSC%205130/G-SDES.pdf

Written by Christian Stigen
"""

def test():
    assert(encrypt(key=0b0000000000, plaintext=0b10101010) == 0b00010001)
    assert(encrypt(key=0b1110001110, plaintext=0b10101010) == 0b11001010)
    assert(encrypt(key=0b1110001110, plaintext=0b01010101) == 0b01110000)
    assert(encrypt(key=0b1111111111, plaintext=0b10101010) == 0b00000100)

def main():
    return x

def rev_ip(x):
    return x

def f(key, x):
    return x

def sw(x):
    return x

def ip(x):
    return x

def encrypt(key, plaintext):
    return rev_ip(f(k2, sw(f(k1, ip(plaintext)))))

def decrypt(key, ciphertext):
    return rev_ip(f(k1, sw(f(k2, ip(ciphertext)))))

def p10(key):
    """Performs the P10 permutation.

    The SDES paper counts bit from the MSB, which is unusual. I.e., what would
    normally be called bit 10 (i.e. 0x200) is in the paper denoted bit 1.

    We could easily create a loop out of this function, and if we wanted to
    implement true DES, we probably would. But to keep it simple, I'm not going
    to do it for this one. Besides, this function as it is (if written in C, or
    JIT-compiled with PyPy, possibly) is very fast without any loops or
    lookups. It has very good pipelining and cascading characteristics, too.
    """
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
    if not (key <= 0b1111111111):
        raise ValueError("Key must be 10 bits")

    k2 = shiftl5(p10(key))
    k1 = p8(k2)
    k2 = p8(shiftl5(shiftl5(k2)))
    return k1, k2

if __name__ == "__main__":
    key = 0b1010000010
    k1, k2 = create_subkeys(key)
    plaintext = 0b10101010
    ciphertext = encrypt(key, plaintext)
    print("key=%s plaintext=%s ciphertext=%s" % (bin(key), bin(plaintext),
        bin(ciphertext)))
