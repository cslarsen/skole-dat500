"""
Steps:
Find repeated characters of increasing length. Look for the one that has the
lowest period, i.e. the lowest distance between the two repeated substrings.

This should indicate a region where *one* alphabet substition is used. When
that is found, crack it like an ordinary monoalphabetic cipher. Example:

    ....abc....xabc....

Distance from first abc to next is 8, between them 5. So take the string

abc....x

and crack that by itself as a monoalphabetic section.
"""

from util import *
import sys
from poly import find_all, period, relfreqs, english

write = sys.stdout.write

en_digrams = {
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
    "ea": 0.47, # cutoff to save time
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

def english_freq():
    total = sum(count for (letter, count) in english.items())
    en = dict((float(count)/total, c) for (c,count) in english.items())
    for letter, count in sorted(en.items(), reverse=True):
        yield letter, count

if __name__ == "__main__":
    ciphertext = readfile("cipher.txt")

    print("Ciphertext:")
    for i, part in enumerate(split_string(ciphertext, 5)):
        write("%s " % part)
        if ((i+1) % 5) == 0:
            write("\n")
    print("")

    # Step 1: Find repeats, look for the lowest distance between two repeats
    lowest = 999999
    mono = ""
    for length in range(3, 11):
        start = 0
        while start+length < len(ciphertext):
            key = ciphertext[start:start+length]
            positions = list(find_all(ciphertext, key))
            if len(positions) > 1:
                for pos in positions:
                    write("pos=%3d %11r  " % (pos, ciphertext[pos:pos+length]))
                if len(positions) == 2:
                    dist = positions[1] - positions[0]
                    if dist < lowest:
                        lowest = dist
                        print("** distance %d between two repeats at %d" %
                                (lowest, positions[0]))
                        pos = positions[0]
                        mono = ciphertext[pos:pos+dist]
                        print("%r" % ciphertext[pos:pos+dist+length])
                write("\n")
            start += length

    print("")
    print("Next step is to decode the shortest string we found:")
    print(repr(mono))

    # Step 2: Look at letter frequencies
    def rf():
        """Print relative frequencies"""
        rf = relfreqs(mono)
        rfitems = sorted(rf.items(), key=lambda (a,b): (b,a), reverse=True)
        for (c, f), (ec, ef) in zip(rfitems, english_freq()):
            print("  %6.5f '%c' vs %6.5f '%c'" % (f, c, ec, ef))

    tbl = {}
    print(mono)
    def tr():
        """Transpose according to table."""
        print(mono)
        print(transpose(mono, tbl))

    def digs(n=1):
        """Show digrams that appear more than n times."""
        dd = ngrams(mono, 2, n, relative=True)
        print(dd)

    def endigs():
        return sorted(map(lambda (a,b): (b,a), en_digrams.items()), reverse=True)

    print(transpose(mono, tbl))
    print("Now continue by hand (run w/python -i poly2.py")
    print("Translation table is in 'tbl', cipher in 'mono'")
    print("Helpful functions: rf() print relfreqs, tr() transpose")
    print(" digs(n) digrams in text that occur more than n")
    print(" endigs() english digrams")
