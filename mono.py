"""
Mono-alphabetic deciphering.
"""

from util import *
import sys

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
doubles = ["ss", "ll", "oo", "ee", "nn", "pp"]

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

def decrypt(text):
    freqs = sorted(relative_freqs(text), reverse=True)

    table = {}
    for no, (count, char) in enumerate(freqs):
        table[char] = sorted(reverse_pairs(letters.items()))[no][1]
        print(count, char)
        if no > 3:
            break

    return "".join(table.get(c, c.upper()) for c in text)

def main():
    cipher = read_file("cipher-mono.txt").lower()

    print("Ciphertext:\n")
    block_print(cipher)
    print("\n")

    print("Plaintext:\n")
    plain = decrypt(cipher)
    print("")
    block_print(plain)

if __name__ == "__main__":
    main()
