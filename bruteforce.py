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

    p.add_argument("--sdes", default=False, action="store_true",
            help="""Bruteforces SDES key instead of TripleSDES.""")

    opts = p.parse_args()

    print("Reading %s" % opts.FILE)
    ciphertext = read_ciphertext(opts.FILE)

    if opts.sdes:
        print("Interpreting file as SDES-encrypted")
        bruteforce_key = csdes.bruteforce_sdes_key
    else:
        print("Interpreting file as TripleSDES-encrypted")
        bruteforce_key = csdes.bruteforce_3sdes_key

    # Bruteforce it
    start = mark_time()
    bf = bruteforce_key(ciphertext, opts.start, opts.stop)
    stop = mark_time()

    print("Found %d keys in %.2f ms CPU time" % (bf.count, 1000.0*(stop - start)))

    print("First found key:")

    if not opts.sdes:
        print("  20-bit key: %20s = 0x%5.5x" % (bin(bf.key)[2:], bf.key))
        k1 = (bf.key & 0xffc00) >> 10;
        print("   10-bit k1: %10.10s.......... = 0x%5.5x" % (bin(bf.key)[2:12], k1))
        k2 = (bf.key & 0x003ff);
        print("   10-bit k2: ..........%10.10s = 0x%5.5x" % (bin(bf.key)[12:], k2))
    else:
        print("  10-bit key: %10s = 0x%3.3x / %d" % (bin(bf.key)[2:], bf.key,
            bf.key));

    if bf.count == 1:
        if opts.sdes:
            plaintext = csdes.sdes_decrypt_buffer(bf.key, ciphertext)
        else:
            plaintext = csdes.triplesdes_decrypt_buffer(k1, k2, ciphertext)
        print("Plaintext (%d bytes):" % len(plaintext))
        print("%r" % plaintext)
    else:
        print("None or several keys were found; not decrypting")
