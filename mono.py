"""
Mono-alphabetic deciphering.
"""

from util import *
import collections
import sys

def subst(cipher, table):
    return "".join(table[c] for c in cipher)

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

def find_double_letters(text):
    for char in alphabet:
        if text.find(char + char) != -1:
            yield char

def show_candidates(cands):
    """Prints determined candidates."""
    for char, alts in sorted(cands.items()):
        if len(alts) == 1:
            print("** Determined that %c maps to %c" % (char, alts[0]))
        elif len(alts) == 2:
            print("Character %c may be either %c or %c" % (char, min(alts),
                max(alts)))

def decrypt(text):
    # Use the method of elimination: For each input letter, keep a list of
    # possible output letters. Initialize with all possibilities. We'll
    # eliminate as we go.
    cands = collections.defaultdict(list)
    for char in alphabet:
        cands[char] = list(alphabet)

    for char in find_double_letters(text):
        # Found a double letter. This means those can only be one of a few
        # possible values.
        cands[char] = doubles
        print("Double letter '%c%c' can be any of %s" % (
            char, char, ", ".join(sorted(doubles))))

    show_candidates(cands)

    print("")
    print("Relative letter frequencies vs English")
    print("    Cipher       English")
    freqs = sorted(relfreq(text), reverse=True)
    for i in range(26):
        try:
            cfreq, cchar = freqs[i]
        except IndexError:
            cfreq, cchar = 0, "-"

        efreq, echar = list(sorted(reverse_pairs(letters.items()),
            reverse=True))[i]
        print("    %c %7.4f    %c %7.4f" % (cchar, cfreq, echar, efreq))

    return ""

def main():
    cipher = readfile("cipher-mono.txt").lower()

    print("Ciphertext:\n")
    block_print(cipher)
    print("")

    print("Analysis:\n")
    plain = decrypt(cipher)
    print("")
    print("Plaintext:\n")
    block_print(plain)
    print("")

if __name__ == "__main__":
    main()
