#! /usr/bin/env python

"""
Cracks a TripleSDES ciphertext in 60ms (actual work) with 30ms overhead for the
Python binding.

Written by Christian Stigen
"""

from util import *
import argparse
import csdes

def read_ciphertext(filename):
    """Converts text file consisting of zeroes and ones in ASCII to binary
    string."""
    ciphertext = readfile(filename)
    return "".join(chr(int(c, 2)) for c in split_string(ciphertext, 8))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("FILE", type=str, nargs="?", default="ctx2.txt",
            help="""Ciphertext file to break, consiting of 0 and 1 in ASCII.""")
    opts = p.parse_args()

    ciphertext = read_ciphertext(opts.FILE)

    # Bruteforce it
    bf = csdes.bruteforce_3sdes_key(ciphertext, len(ciphertext))
    print("Found %d keys" % bf.count)

    k1 = (bf.key & 0xffc00) >> 10;
    k2 = (bf.key & 0x003ff);

    print("  20-bit key: 0x%5.5x" % bf.key);
    print("  10-bit k1:    0x%3.3x" % k1);
    print("  10-bit k2:    0x%3.3x" % k2);
