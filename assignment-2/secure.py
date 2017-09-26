#! /usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Implements secure communications

For DAT-510 Security and vulnerability in networks, University of Stavanger,
autumn 2017.

Written by Christian Stigen

Steps to be performed:

    step 1: Agree on global parameters for DH-like key exchange:
        - cyclic gropu G = <g> to use. E.g. Z_p^* w/generator g=2
          (choose prime as p=2q+1 from a prime) or a cyclic group generated
          from an elliptic curve E. (see textbook)

    step 2: using DH key exchange, alice and bob generates their own key pairs
        (PRa, PUa) and (PRb, PUb)

    step 3: A sends pubkey PUa to B, B sends pubkey PUb to A

    step 4: A generates a shared key Kab and so does B

    step 5: A and B agree to use the same cryptographically strong PRNG
        (CSPRNG) which takes Kab as seed, generates a secret key K for
        subsequent encryption/decryption

    step 6: A chooses a symmetric cipher to encrypt a file with the key K and
        sends the encrypted file over a public channel (internet) to B

    step 7: upon receiving the encrypted file from A, B uses the same key K and
        symmetric cipher to decrypt it and obtain A's file in clear form.
"""

import argparse

__author__ = "Christian Stigen"

def parse_args():
    p = argparse.ArgumentParser()

    opts = p.parse_args()
    return opts

def main(opts):
    pass

if __name__ == "__main__":
    opts = parse_args()
    main(opts)
