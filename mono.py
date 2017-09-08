"""
Mono-alphabetic deciphering.
"""

from util import *
import argparse
import sys

alphabet = "abcdefghijklmnopqrstuvwxyz"

# Cornell
letters = {
    "e": 12.02,
    "t": 9.10,
    "a": 8.12,
    "o": 7.68,
    "i": 7.31,
    "n": 6.95,
    "s": 6.28,
    "r": 6.02,
    "h": 5.92,
    "d": 4.32,
    "l": 3.98,
    "u": 2.88,
    "c": 2.71,
    "m": 2.61,
    "f": 2.30,
    "y": 2.11,
    "w": 2.09,
    "g": 2.03,
    "p": 1.82,
    "b": 1.49,
    "v": 1.11,
    "k": 0.69,
    "x": 0.17,
    "q": 0.11,
    "j": 0.10,
    "z": 0.07,
}

# Cornell: Common English double letters
doubles = ["s", "l", "o", "e", "n", "p"]

# Cornell
digrams = {
    "th": 1.52,
    "he": 1.28,
    "in": 0.94,
    "er": 0.94,
    "an": 0.82,
    "re": 0.68,
    "nd": 0.63,
    "at": 0.59,
    "on": 0.57,
    "nt": 0.56,
    "ha": 0.56,
    "es": 0.56,
    "st": 0.55,
    "en": 0.55,
    "ed": 0.53,
    "to": 0.52,
    "it": 0.50,
    "ou": 0.50,
    "ea": 0.47,
    "hi": 0.46,
    "is": 0.46,
    "or": 0.43,
    "ti": 0.34,
    "as": 0.33,
    "te": 0.27,
    "et": 0.19,
    "ng": 0.18,
    "of": 0.16,
    "al": 0.09,
    "de": 0.09,
    "se": 0.08,
    "le": 0.08,
    "sa": 0.06,
    "si": 0.05,
    "ar": 0.04,
    "ve": 0.04,
    "ra": 0.04,
    "ld": 0.02,
    "ur": 0.02,
}

def analyse(text):
    cutoff = 2
    for n in (1, 2, 3):
        print("%d-gram relative frequencies (cutoff=%d):" % (n, cutoff))
        for ngram, count in ngrams(text, n=n, relative=True, minimum=cutoff):
            print("  %s %5.2f" % (ngram, count))

    # Proceed like this:
    #
    # for each trigram:
    #   Assign one unique English trigram to each, all combos.
    #   for each digram:
    #       Assign one unique English digram to each, all combos.
    #       If they contradict the above trigrams, skip.
    #           for each monogram:
    #               Assign one unique English monogram to each, all combos ---
    #               at this point, there should be considerably less than 26!
    #               combos, else give a user warning
    #
    #               Decrypt and detect relative number of english words. over a
    #               given threshold, print the message.

def main(filename):
    cipher = readfile(filename).lower()

    print("Ciphertext:")
    block_print(cipher)

    print("Analysis:")
    analyse(cipher)

if __name__ == "__main__":
    p = argparse.ArgumentParser()

    p.add_argument("files", nargs="+", default="cipher-mono.txt",
            help="File to attempt to mono-alpha decrypt")

    opt = p.parse_args()

    for filename in opt.files:
        main(filename)
