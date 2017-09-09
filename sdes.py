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

if __name__ == "__main__":
    key = 0
    k1 = 0
    k2 = 0
    plaintext = 0b10101010
    ciphertext = encrypt(key, plaintext)
    print("key=%s plaintext=%s ciphertext=%s" % (bin(key), bin(plaintext),
        bin(ciphertext)))
