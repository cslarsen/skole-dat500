def encrypt(key, plaintext):
    pass

def test():
    assert(encrypt(key=0b0000000000, plaintext=0b10101010) == 0b00010001)
    assert(encrypt(key=0b1110001110, plaintext=0b10101010) == 0b11001010)
    assert(encrypt(key=0b1110001110, plaintext=0b01010101) == 0b01110000)
    assert(encrypt(key=0b1111111111, plaintext=0b10101010) == 0b00000100)

def main():
    pass

if __name__ == "__main__":
    pass
