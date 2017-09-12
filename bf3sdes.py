#! /usr/bin/env python

"""
Cracks a TripleSDES ciphertext in 60ms (actual work) with 30ms overhead for the
Python binding.

Written by Christian Stigen
"""

from util import *
import argparse
import csdes
import time
import sys

# Which function to use to measure time spent brute-forcing
if sys.version_info.major < 3:
    mark_time = time.clock
else:
    mark_time = time.perf_counter

def read_ciphertext(filename):
    """Converts text file consisting of zeroes and ones in ASCII to binary
    string."""
    ciphertext = readfile(filename)
    ciphertext = [int(c, 2) for c in split_string(ciphertext, 8)]
    return bytearray(ciphertext)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("FILE", type=str, nargs="?", default="ctx2.txt",
            help="""Ciphertext file to break, consiting of 0 and 1 in ASCII.""")
    p.add_argument("--start", type=int, default=32,
            help="""
Discard keys that decrypt to bytes outside of the --start and --end range. A
good starting point is to require that all decrypted bytes fall within the
visible ASCII range of 32 to 126.""".lstrip())

    p.add_argument("--stop", type=int, default=126,
            help="""End of range; see --start""")

    opts = p.parse_args()

    ciphertext = read_ciphertext(opts.FILE)

    # Bruteforce it
    start = mark_time()
    bf = csdes.bruteforce_3sdes_key(ciphertext, opts.start, opts.stop)
    stop = mark_time()

    print("Found %d keys in %.1f ms CPU time" % (bf.count, 1000.0*(stop - start)))

    k1 = (bf.key & 0xffc00) >> 10;
    k2 = (bf.key & 0x003ff);

    print("First found key:")
    print("  20-bit key: 0x%5.5x" % bf.key);
    print("  10-bit k1:    0x%3.3x" % k1);
    print("  10-bit k2:    0x%3.3x" % k2);

    print("  key binary: %20s" % bin(bf.key))
    print("  k1 binary:  %10s.........." % bin(k1))
    print("  k2 binary:  ..........%12s" % bin(k2))

    if bf.count == 1:
        plaintext = csdes.triplesdes_decrypt_buffer(k1, k2, ciphertext)
        print("Plaintext (%d bytes):" % len(plaintext))
        print("%r" % plaintext)
    else:
        print("None or several keys were found; not decrypting")
