#! /usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Attempts to recover the plaintext of a Vigenére polyalphabetic ciphertext.

Written by Christian Stigen
"""

import argparse
import collections
import functools
import operator
import os
import sys

# Local imports
from util import (
    block_print,
    normalize,
    readfile,
    split_string,
    transpose,
)

# Relative frequencies for English (percentages)
english = {
    "a": 8.167,
    "b": 1.492,
    "c": 2.782,
    "d": 4.253,
    "e": 12.702,
    "f": 2.228,
    "g": 2.015,
    "h": 6.094,
    "i": 6.996,
    "j": 0.153,
    "k": 0.772,
    "l": 4.025,
    "m": 2.406,
    "n": 6.749,
    "o": 7.507,
    "p": 1.929,
    "q": 0.095,
    "r": 5.987,
    "s": 6.327,
    "t": 9.056,
    "u": 2.758,
    "v": 0.978,
    "w": 2.360,
    "x": 0.150,
    "y": 1.974,
    "z": 0.074,
}

def reverse_pair(ab):
    a, b = ab
    return (b, a)

def find_all(haystack, needle):
    start = 0
    while start  < len(haystack):
        found = haystack.find(needle, start)
        if found == -1:
            break
        yield found
        start += found + 1

def english_freq():
    total = sum(count for (letter, count) in english.items())
    en = dict((float(count)/total, c) for (c,count) in english.items())
    for letter, count in sorted(en.items(), reverse=True):
        yield letter, count

def make_vigenere_table():
    """Returns a Vigenere table. Vastly inefficient code."""
    tbl = {}
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for shift in range(len(alpha)):
        Y = alpha[shift]
        tbl[Y] = {}
        for n in range(len(alpha)):
            char = alpha[(shift + n) % len(alpha)]
            X = alpha[n]
            tbl[Y][X] = char
    return tbl

def vigenere_encrypt(plaintext, key):
    """Encrypts Vigenère cipher (vastly inefficient code)."""
    ciphertext = ""
    table = make_vigenere_table()
    plaintext = plaintext.replace(" ", "").upper()
    key = key.upper()
    for n in range(len(plaintext)):
        x = key[n % len(key)]
        y = plaintext[n]
        if y != " ":
            ciphertext += table[x][y]
    return ciphertext

def vigenere_decrypt(ciphertext, key):
    """Decrypts Vigenère cipher (vastly inefficient code)."""
    table = make_vigenere_table()
    plaintext = ""
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ciphertext = ciphertext.replace(" ", "").upper()
    key = key.upper()
    for n in range(len(ciphertext)):
        x = key[n % len(key)]
        byte = ciphertext[n]

        line = "".join(table[x][c] for c in alpha)
        # find byte in line
        idx = line.find(byte)
        plaintext += alpha[idx]
    return plaintext

def freqs_en():
    counts = [
        (12.02, "e"),
        (9.10, "t"),
        (8.12, "a"),
        (7.68, "o"),
        (7.31, "i"),
        (6.95, "n"),
        (6.28, "s"),
        (6.02, "r"),
        (5.92, "h"),
        (4.32, "d"),
        (3.98, "l"),
        (2.88, "u"),
        (2.71, "c"),
        (2.61, "m"),
        (2.30, "f"),
        (2.11, "y"),
        (2.09, "w"),
        (2.03, "g"),
        (1.82, "p"),
        (1.49, "b"),
        (1.11, "v"),
        (0.69, "k"),
        (0.17, "x"),
        (0.11, "q"),
        (0.10, "j"),
        (0.07, "z"),
    ]
    total = sum(count for (count, letter) in counts)
    counts = [(ch.upper(), float(count)/total) for (count, ch) in counts]
    return sorted(counts, key=reverse_pair, reverse=True)

def freqs(text):
    # Frequency count letters
    counts = collections.defaultdict(int)
    for char in normalize(text):
        counts[char.upper()] += 1

    # Sort by decreasing count
    items = counts.items()
    items = sorted(items, key=reverse_pair, reverse=True)

    # Calculate relative frequency
    total = sum(count for (char, count) in items)
    items = [(char, float(count)/total) for (char, count) in items]

    return items

def shift(text, amount):
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    assert(len(alpha) == 26)
    shifted = ""
    for n in range(len(alpha)):
        shifted += alpha[(n + amount) % len(alpha)]

    tbl = dict((a, b) for (a, b) in zip(alpha, shifted))
    return transpose(text.upper(), tbl)

def show_freqs(text):
    txt = freqs(text)
    eng = freqs_en()

    # Change it up: Show frequencies by alphabetical entries
    def rev(pairs):
        out = {}
        for a in range(ord("A"), ord("Z")):
            out[chr(a)] = 0
        for char, count in pairs:
            out[char] = count
        return out

    txt = rev(txt)
    eng = rev(eng)

    txt = sorted(txt.items())
    eng = sorted(eng.items())

    print("                   Text - English")
    max1 = max(n for (c,n) in txt)
    max2 = max(n for (c,n) in eng)
    for (ch1, n1), (ch2, n2) in zip(txt, eng):
        bar1 = "*"*int(round(10*n1/max1)) if n1>0 else ""
        bar2 = "*"*int(round(10*n2/max2)) if n2>0 else ""
        print("%10s %7.4f %c  - %7.4f %c %-10s" % (bar1, n1, ch1, n2, ch2, bar2))

def coincidence_factor(text, shifts):
    """Calculates the coincidence factor for a string, based on the English
    letter frequencies.

    In practical terms, this calcualtes the correlation of the frequency counts
    in the input string with those found in typical English texsts. If the
    coincidence factor is high, the frequency distribution is very similar to
    the English. If it is low, there is a low correlation.
    """
    text = shift(text, shifts)
    txt = freqs(text)
    eng = freqs_en()

    def rev(pairs):
        out = {}
        for a in range(ord("A"), ord("Z")):
            out[chr(a)] = 0
        for char, count in pairs:
            out[char] = count
        return out

    txt = sorted(rev(txt).items())
    eng = sorted(rev(eng).items())

    coinc = 0
    for (ch1, n1), (ch2, n2) in zip(txt, eng):
        coinc += n1*n2
    return coinc

def parse_args():
    p = argparse.ArgumentParser(
            description="Recovers plaintext and key from Vigenère ciphertext")
    p.add_argument("file", default="cipher.txt",
        help="File with ASCII ciphertext to decipher")
    p.add_argument("--min-length", default=4, type=int,
        help="Minimum keylength to scan for")
    p.add_argument("--max-length", default=10, type=int,
        help="Maximum keylength to scan for")
    p.add_argument("-v", "--verbose", default=False, action="store_true",
        help="Show steps performed to decipher")
    opts = p.parse_args()

    if not os.path.isfile(opts.file):
        print("Not a file: %s" % opts.file)
        sys.exit(1)

    if opts.min_length >= opts.max_length:
        print("Min/max lengths invalid: %s %s" % (opts.min_length,
            opts.max_length))
        sys.exit(1)

    return opts

def is_divisible(divisor, dividend):
    """Checks if divisor is evenly divisible by dividend, i.e. results in a
    plain integer."""
    return (float(divisor)/dividend - divisor//dividend) == 0

def find_common_factors(numbers):
    """Finds factors that are common to *all* numbers.

    For example, 30 and 70 factorize to 2*3*5 and 7*2*5, but only 2 and 5 are
    common factors.
    """
    common = set()
    for factor in range(2, max(numbers)):
        if all(is_divisible(number, factor) for number in numbers):
            if all(not is_divisible(factor, number) for number in common):
                common.add(factor)
    return common

def extract_string_columns(text, length):
    """Splits input string into n strings of given length, then transposes
    them so that each output string consists of the characters found in the
    same positions in the input strings.

    For example:

       string 1: abc
       string 2: def
       output 1: ad
       output 2: be
       output 3: cf
    """
    columns = []
    for index in range(length):
        column = ""
        for col in split_string(text, length):
            try:
                column += col[index]
            except IndexError:
                # This happens if any input string is shorter than the others
                pass
        columns.append("".join(column))
    return columns

def recombine_string_columns(columns, length):
    """Does the reverse of ``extract_string_columns``."""
    string = ""
    for index in range(length):
        column = ""
        for col in columns:
            try:
                column += col[index]
            except IndexError:
                # This happens if any input string is shorter than the others
                pass
        string += "".join(column)
    return string

def main():
    opts = parse_args()
    ciphertext = readfile(opts.file)

    def verbose(message):
        if opts.verbose:
            sys.stdout.write(message)

    print("Ciphertext in %s:\n" % opts.file)
    block_print(ciphertext, 5, 60//(5+1))
    print("")

    # Step 1: Find repeats, look for the lowest distance between two repeats
    verbose("Looking for repeated substrings with lengths [%d, %d]:\n\n" % (
        opts.min_length, opts.max_length))

    distances = set()
    for length in range(opts.max_length, opts.min_length-1, -1): # problem said max 10 keylength
        start = 0
        while start+length < len(ciphertext):
            key = ciphertext[start:start+length]
            positions = list(find_all(ciphertext, key))
            if len(positions) > 1:
                verbose("  Found %-12r at " % key)
                verbose(", ".join("%3d" % p for p in positions))

                for i, pos in enumerate(positions):
                    dist = -1
                    if i > 0:
                        dist = pos - positions[i-1]
                        distances.add(dist)
                    if dist > 0:
                        verbose(" distance %3d" % dist)
                verbose("\n")
            start += 1
    verbose("\n")

    verbose("Attempting to deduce key length:\n\n")
    verbose("  Set of distances: %s\n" % " ".join(map(str, distances)))

    common = find_common_factors(distances)

    if len(common) == 0:
        print("Could not find any common factors for the repated distances:")
        print(" ".join(map(str, sorted(distances))))
        print("Try changing the --min-length and --max-length")
        sys.exit(1)

    keylength = functools.reduce(operator.mul, common)
    verbose("  Common factors:   %s\n" % " ".join(map(str, common)))
    verbose("  Proposed length:  %s = %d\n" % ("*".join(map(str, common)),
        keylength))
    verbose("\n")

    verbose("Finding monoalphabetic ciphers. ")
    verbose("Ciphertext arranged in %d columns is:\n\n" % keylength)
    if opts.verbose:
        block_print(ciphertext, keylength, 1, stop=5)
    verbose("  %s\n\n" % ("."*keylength))

    # Take character N from every column
    columns = []
    tables = []
    for i in range(keylength):
        tables.append({})

    # Create strings from each vertical column, put in columns
    columns = extract_string_columns(ciphertext, keylength)
    mlen = min(30, len(columns[0])//2)
    verbose("  First column: %*.*s...\n\n" % (mlen, mlen, columns[0]))

    # Now, calculate the best coincidence:
    # https://en.wikipedia.org/wiki/Index_of_coincidence
    verbose("Frequency analysis:\n")
    verbose("Shifts alphabets for each column to find the best coincidence match\n\n")
    for i in range(len(columns)):
        factor, shifts = max((coincidence_factor(columns[i], n), n) for n in
                range(26))
        verbose("  Column %d length %d: best match %f with %2d shifts\n" % (i,
            len(columns[i]), factor, shifts))
        columns[i] = shift(columns[i], shifts)
    verbose("\n")

    print("Proposed plaintext:\n")
    plaintext = recombine_string_columns(columns, max(map(len, columns)))
    block_print(plaintext, keylength, 60//(keylength+1), indent="  ")
    print("")

    key = vigenere_decrypt(ciphertext, plaintext)[:keylength]
    print("Key for above plaintext: %r" % key)

if __name__ == "__main__":
    main()
