#! /usr/bin/env python

from util import *
import csdes

if __name__ == "__main__":
    # TODO: Take input file from the command line
    ciphertext = readfile("ctx2.txt")

    # Decode to binary
    ciphertext = "".join(chr(int(c, 2)) for c in split_string(ciphertext, 8))

    # Bruteforce it
    result = csdes.bruteforce_3sdes_key(ciphertext, len(ciphertext))
    print("Found %d keys" % result.count)
    print("20-bit key: 0x%5.5x" % result.key)
