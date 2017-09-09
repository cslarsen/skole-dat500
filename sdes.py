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

def create_subkeys(key):
    return 0, 0

if __name__ == "__main__":
    key = 0
    k1, k2 = create_subkeys(key)
    plaintext = 0b10101010
    ciphertext = encrypt(key, plaintext)
    print("key=%s plaintext=%s ciphertext=%s" % (bin(key), bin(plaintext),
        bin(ciphertext)))

    k = 0b1010000010
    print("p10(%s) => %s" % (bin(k), bin(p10(k))))
