# -*- encoding: utf-8 -*-

"""
Completes table in part II, task 1.

Written by Christian Stigen
"""

import csdes

def binary(number, bits):
    s = bin(number)[2:]
    s = "0"*(bits - len(s)) + s
    return s

def verify():
    # key, plaintext, ciphertext
    tests = [
        (0b0000000000, 0b10101010, 0b00010001),
        (0b1110001110, 0b10101010, 0b11001010),
        (0b1110001110, 0b01010101, 0b01110000),
        (0b1111111111, 0b10101010, 0b00000100),
    ]

    print("VERIFY\n")

    print("Raw key    Plaintext  Ciphertext")
    print("--------------------------------")

    for k, p, c in tests:
        print("%s %s   %s" % (binary(k, 10), binary(p, 8), binary(c, 8)))
        tp = csdes.decrypt(k, c)
        print("           %s" % binary(tp, 8))
        assert(p == csdes.decrypt(k, c))
        tc = csdes.encrypt(k, p)
        print("                      %s" % binary(tc, 8))
        assert(c == csdes.encrypt(k, p))
        print("--------------------------------")

    print("")

def main():
    # 10-bit key, 8-bit plaintext
    plaintexts = [
        (0b0000000000, 0b00000000),
        (0b0000011111, 0b11111111),
        (0b0010011111, 0b11111100),
        (0b0010011111, 0b10100101),
    ]

    ciphertexts = [
        (0b1111111111, 0b00001111),
        (0b0000011111, 0b01000011),
        (0b1000101110, 0b00011100),
        (0b1000101110, 0b11000010),
    ]

    print("TASK 1\n")

    print("Raw key    Plaintext  Ciphertext")
    print("--------------------------------")

    for key, plaintext in plaintexts:
        ciphertext = csdes.encrypt(key, plaintext)
        print("%s %s   %s" % (binary(key, 10), binary(plaintext, 8),
            binary(ciphertext, 8)))
        if csdes.decrypt(key, ciphertext) != plaintext:
            print("WRONG")
    print("--------------------------------")

    for key, ciphertext in ciphertexts:
        plaintext = csdes.decrypt(key, ciphertext)
        print("%s %s   %s" % (binary(key, 10), binary(plaintext, 8),
            binary(ciphertext, 8)))
    print("--------------------------------")

if __name__ == "__main__":
    verify()
    main()
