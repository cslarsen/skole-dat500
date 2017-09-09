"""
Mono-alphabetic deciphering.
"""

from util import *
import argparse
import itertools
import sys

alphabet = "abcdefghijklmnopqrstuvwxyz"

# Cornell
en_letters = {
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
en_doubles = ["s", "l", "o", "e", "n", "p"]

# Cornell
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

# Trigrams from
# http://practicalcryptography.com/cryptanalysis/letter-frequencies-various-languages/english-letter-frequencies/
en_trigrams = {
    "the": 1.81,
    "and": 0.73,
    "ing": 0.72,
    "ent": 0.42,
    "ion": 0.42,
    "her": 0.36,
    "for": 0.34,
    "tha": 0.33,
    "nth": 0.33,
    "int": 0.32,
    "ere": 0.31,
    "tio": 0.31, # cutoff to save time
    "ter": 0.30,
    "ers": 0.28,
    "est": 0.28,
    "ati": 0.26,
    "hat": 0.26,
    "all": 0.25,
    "ate": 0.25,
    "eth": 0.24,
    "hes": 0.24,
    "his": 0.24,
    "ver": 0.24,
    "oft": 0.22,
    "fth": 0.21,
    "ith": 0.21,
    "oth": 0.21,
    "res": 0.21,
    "sth": 0.21,
    "ont": 0.20,
}

def map_ngrams(grams):
    """Try to map an n-gram with an English one."""
    grams = list(map(lambda x: x[0], grams))
    n = len(grams[0])

    if n == 3:
        actual = en_trigrams
    elif n == 2:
        actual = en_digrams
    elif n == 1:
        actual = en_letters
    else:
        raise ValueError(str(n))

    for combo in itertools.permutations(actual.keys(), len(grams)):
        combo = list(map(lambda x: x.lower(), combo))
        # Matches an n-gram with an English n-gram
        yield zip(grams, combo)

def analyse(text):
    cutoff = 2
    for n in (1, 2, 3):
        print("%d-gram relative frequencies (cutoff=%d):" % (n, cutoff))
        for ngram, count in ngrams(text, n=n, relative="both", minimum=cutoff):
            print("  %s %3d %5.2f" % (ngram, count[0], count[1]))

    def decr(txt, tbl):
        out = ""
        for ch in txt:
            out += tbl.get(ch, ".")
        return out

    if False:
        for tgrams in map_ngrams(ngrams(text, 3, 2, relative="both")):
            table = {}
            for (ours, theirs) in tgrams:
                for l, r in zip(ours[0], theirs[0]):
                    #if l in table:
                    if l in dtable.keys() or r in dtable.values():
                        # Actually, we should jump right to the next tgram here
                        continue
                    table[l] = r

            plain = decr(text, table)
            corr = is_english(plain)
            if corr > 0.1:
                print("%.4f %s" % (corr, plain))

    if False:
        dd = ngrams(text, 2, 3, relative="both")
        #dd = dd[:5]
        table = {}
        bestcorr = 0
        skip = False
        for dgrams in map_ngrams(dd):
            dtable = dict(table) # keep original table
            try:
                for (ours, theirs) in dgrams:
                    for l, r in zip(ours[0], theirs[0]):
                        if l in dtable.keys() or r in dtable.values():
                            # Actually, we should jump right to the next tgram here
                            raise IndexError()
                            continue
                        dtable[l] = r
            except IndexError:
                continue

            # Try to decrypt with the table
            plain = decr(text, dtable)
            corr = is_english(plain)
            if corr > bestcorr:
                bestcorr = corr
                #print("       %s" % text)
                print("%6.4f %s" % (corr, plain))
            #for monogram in ngrams(text, 1, 8, relative="both"):
            #pass

    dd = ngrams(text, 2, 3, relative="both")
    #dd = dd[:5]
    table = {}
    bestcorr = 0
    skip = False
    for dgrams in map_ngrams(dd):
        dtable = dict(table) # keep original table
        try:
            for (ours, theirs) in dgrams:
                for l, r in zip(ours[0], theirs[0]):
                    if l in dtable:
                        # Actually, we should jump right to the next tgram here
                        raise IndexError()
                        continue
                    dtable[l] = r

            # Try to decrypt with the table
            plain = decr(text, dtable)
            corr = is_english(plain)
            if corr > bestcorr:
                bestcorr = corr
                #print("       %s" % text)
                print("%6.4f %s" % (corr, plain))

            for mgrams in map_ngrams(ngrams(text, 1, 8, relative="both")):
                mtable = dict(dtable) # keep original table
                try:
                    for (ours, theirs) in mgrams:
                        if l in mtable:
                            raise IndexError()
                        mtable[l] = r
                except IndexError:
                    continue

                # Try to decrypt with the table
                plain = decr(text, mtable)
                corr = is_english(plain)
                if corr > bestcorr:
                    bestcorr = corr
                    #print("       %s" % text)
                    print("%6.4f %s" % (corr, plain))

        except IndexError:
            continue

        #for monogram in ngrams(text, 1, 8, relative="both"):
        #pass




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
    pass

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
