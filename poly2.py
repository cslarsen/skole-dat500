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

def make_vigenere_table():
    """Returns a Vigenere table."""
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

if __name__ == "__main__":
    ciphertext = readfile("cipher.txt")

    print("Ciphertext:")
    for i, part in enumerate(split_string(ciphertext, 5)):
        write("%s " % part)
        if ((i+1) % 5) == 0:
            write("\n")
    print("")

    # Step 1: Find repeats, look for the lowest distance between two repeats
    lowest = 0
    mono = ""
    distances = set()
    for length in range(len(ciphertext), 3, -1):
        start = 0
        while start+length < len(ciphertext):
            key = ciphertext[start:start+length]
            positions = list(find_all(ciphertext, key))
            if len(positions) > 1:
                for i, pos in enumerate(positions):
                    dist = -1
                    if i > 0:
                        dist = pos - positions[i-1]
                        distances.add(dist)
                    write("pos=%3d %20r %s" % (pos,
                        ciphertext[pos:pos+length],
                            "dist=%d" % dist if dist>0 else ""))
                write("\n")
            start += length

    print("Distances: %s" % " ".join(map(str, distances)))
    divisible = lambda a, b: float(a)/b - a//b == 0

    # Find common factors
    common = set()
    for n in range(2, max(distances)):
        if all(divisible(d, n) for d in distances):
            if all(not divisible(n, c) for c in common):
                common.add(n)
    print("Common factors: %s" % " ".join(map(str, common)))
    cfactor = reduce(lambda a,b: a*b, common)
    print("Perhaps the keylength is %d" % cfactor)

    print("Ciphertext in %d columns" % cfactor)
    parts = list(split_string(ciphertext, cfactor))
    for i, part in enumerate(parts):
        print(part)
        if i > 5:
            print("... %d more" % (len(parts) - i))
            break

    print("Take every letter down vertically into %d strings" % cfactor)

    monos = []
    if len(parts[-1]) < cfactor:
        del parts[-1] # delete tail
    for index in range(cfactor):
        monos.append("".join(s[index] for s in parts))

    print(monos[0])
    print("These strings are stored in the variable 'monos'")

    out = []
    tables = []
    for mono in monos:
        tbl = {}
        rf = relfreqs(mono)
        rfitems = sorted(rf.items(), key=lambda (a,b): (b,a), reverse=True)
        for (c, f), (ef, ec) in zip(rfitems, english_freq()):
            tbl[c.upper()] = ec.upper()
        tables.append(tbl)
        out.append(transpose(mono, tbl))

    # convert back
    plain = ""
    for index in range(len(out[0])):
        plain += "".join(s[index] for s in out)
    print("---")
    print(plain)
    print("---")


    mono = monos[0]

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
