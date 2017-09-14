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

import collections
import sys

# local imports
from poly import find_all, period, english
from util import readfile, split_string, transpose, normalize, block_print

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
    return sorted(counts, key=lambda (a,b): (b,a), reverse=True)

def freqs(text):
    # Frequency count letters
    counts = collections.defaultdict(int)
    for char in normalize(text):
        counts[char.upper()] += 1

    # Sort by decreasing count
    items = counts.items()
    items = sorted(items, key=lambda (a,b): (b,a), reverse=True)

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

def coinc(text, shifts):
    """Coincidence factor."""
    text = shift(text, shifts)
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

    txt = sorted(rev(txt).items())
    eng = sorted(rev(eng).items())

    coinc = 0
    for (ch1, n1), (ch2, n2) in zip(txt, eng):
        coinc += n1*n2
    return coinc

def recombine(parts):
    plain = ""
    for index in range(len(parts[0])):
        line = ""
        for s in parts:
            try:
                line += s[index]
            except IndexError:
                pass
        plain += "".join(line)
        #plain += "".join(s[index] for s in parts)
    return plain

def rebuild(parts, tables, show=True):
    decoded = []
    for part, table in zip(parts, tables):
        after = transpose(part, table)
        decoded.append(after)
        if show:
            print("  cipher %s" % " ".join(split_string(part, len(parts))))
            print("  plain  %s" % " ".join(split_string(after, len(parts))))
    return recombine(decoded)

if __name__ == "__main__":
    minlength, maxlength = 3, 10 # keylengths
    assert(minlength < maxlength)

    filename = "cipher.txt"
    ciphertext = readfile(filename)

    print("Ciphertext in %s:\n" % filename)
    block_print(ciphertext, 5, 10)
    print("")

    # Step 1: Find repeats, look for the lowest distance between two repeats
    print("Looking for repeated substrings with lengths [%d, %d]:\n" % (
        minlength, maxlength))
    distances = set()
    for length in range(maxlength, minlength, -1): # problem said max 10 keylength
        start = 0
        while start+length < len(ciphertext):
            key = ciphertext[start:start+length]
            positions = list(find_all(ciphertext, key))
            if len(positions) > 1:
                sys.stdout.write("  Found %-12r at " % key)
                sys.stdout.write(", ".join("%3d" % p for p in positions))
                for i, pos in enumerate(positions):
                    dist = -1
                    if i > 0:
                        dist = pos - positions[i-1]
                        distances.add(dist)
                    if dist > 0:
                        sys.stdout.write(" distance %3d" % dist)
                sys.stdout.write("\n")
            start += length
    print("")

    print("Attempting to deduce key length:\n")
    print("  Set of distances: %s" % " ".join(map(str, distances)))
    divisible = lambda a, b: float(a)/b - a//b == 0

    # Find common factors
    common = set()
    for n in range(2, max(distances)):
        if all(divisible(d, n) for d in distances):
            if all(not divisible(n, c) for c in common):
                common.add(n)
    print("  Common factors:   %s" % " ".join(map(str, common)))
    keylength = reduce(lambda a,b: a*b, common)
    print("  Proposed length:  %s = %d" % ("*".join(map(str, common)),
        keylength))
    print("")

    print("Finding monoalphabetic ciphers. Ciphertext arranged in %d columns is:\n" % keylength)
    columns = list(split_string(ciphertext, keylength))
    for i, part in enumerate(columns):
        print("  %s" % part)
        if i > 5:
            print("  %s (%d more)" % ("."*keylength, len(columns) - i))
            break

    # Take character N from every column
    monos = []
    tables = []
    for i in range(keylength):
        tables.append({})

    # Create strings from each vertical column, put in monos
    for index in range(keylength):
        line = ""
        for col in columns:
            try:
                line += col[index]
            except IndexError:
                pass
        monos.append("".join(line))
    mlen = 30
    if mlen > len(monos[0]):
        mlen = len(monos[0])//2
    print("  First column: %*.*s..." % (mlen, mlen, monos[0]))
    print("")

    def show():
        p = rebuild(monos, tables, show=False)
        cols = 12
        p = list(split_string(p, keylength*cols))
        c = list(split_string(ciphertext, keylength*cols))

        for plain, ciph in zip(p, c):
            print(" ".join(split_string(ciph, keylength)))
            print(" ".join(split_string(plain, keylength)))

    # Now, calculate the best coincidence:
    # https://en.wikipedia.org/wiki/Index_of_coincidence
    print("Frequency analysis -- finding best coincidence match for each column:\n")
    for i in range(len(monos)):
        cf, shifts = max([(coinc(monos[i], n), n) for n in range(26)])
        print("  Column %d: match %f, shifts %2d" % (i, cf, shifts))
        # Perform shift
        monos[i] = shift(monos[i], shifts)
    print("")

    print("Deduced plaintext using above shifts:\n")
    plaintext = recombine(monos)
    block_print(plaintext, keylength, 60//(keylength+1), indent="  ")
    print("")

    key = vigenere_decrypt(ciphertext, plaintext)[:keylength]
    print("Key for above plaintext: %r" % key)
