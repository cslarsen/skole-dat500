# -*- encoding: utf-8 -*-

"""
Completes table in part II, task 2.

Written by Christian Stigen
"""

import csdes

def binary(number, bits):
    s = bin(number)[2:]
    s = "0"*(bits - len(s)) + s
    return s

def main():
    # 10-bit key, 10-bit key, 8-bit plaintext
    plaintexts = [
        (0b1000101110, 0b0110101110, 0b11010111),
        (0b1000101110, 0b0110101110, 0b10101010),
        (0b1111111111, 0b1111111111, 0b00000000),
        (0b0000000000, 0b0000000000, 0b01010010),
    ]

    # 10-bit key, 10-bit key, 8-bit ciphertext
    ciphertexts = [
        (0b1000101110, 0b0110101110, 0b11100110),
        (0b1011101111, 0b0110101110, 0b01010000),
        (0b1111111111, 0b1111111111, 0b00000100),
        (0b0000000000, 0b0000000000, 0b11110000),
    ]

    print("TASK 2\n")

    print("Key 1       Key 2      Plaintext  Ciphertext")
    print("--------------------------------------------")

    for key1, key2, plaintext in plaintexts:
        ciphertext = csdes.triplesdes_encrypt(key1, key2, plaintext)
        assert(csdes.triplesdes_decrypt(key1, key2, ciphertext) == plaintext)
        print("%s  %s  %s  *%s" % (binary(key1, 10), binary(key2, 10),
            binary(plaintext, 8), binary(ciphertext, 8)))

    print("--------------------------------------------")

    for key1, key2, ciphertext in ciphertexts:
        plaintext = csdes.triplesdes_decrypt(key1, key2, ciphertext)
        assert(csdes.triplesdes_encrypt(key1, key2, plaintext) == ciphertext)
        print("%s  %s  %s  *%s" % (binary(key1, 10), binary(key2, 10),
            binary(plaintext, 8), binary(ciphertext, 8)))
    print("--------------------------------------------")

if __name__ == "__main__":
    main()
