import collections
import sys

def normalize(s):
    """Removes whitespace from string and makes it uppercase."""
    out = ""
    for ch in s:
        if not ch.isspace():
            out += ch
    return out.upper()

def reverse_pairs(pairs):
    """Reverses pairs in an iterable."""
    for a, b in pairs:
        yield (b, a)

def subst(text, table):
    """Translates each character according to table."""
    return "".join(table[c] for c in text)

def readfile(filename):
    """Returns normalized text in file."""
    with open(filename, "rt") as f:
        return normalize(f.read())

def relfreq(text, n=1, minimum=0):
    """Finds relative frequency counts of n-grams in text.

    Returns:
        For  a digram, for example [(0.112, "XY"), ...]
    """
    grams = list(ngrams(text, n, minimum))
    total = sum(map(lambda (char, count): count, grams))

    out = []
    for char, count in grams:
        out.append((float(count) / total, char))

    return sorted(out, reverse=True)

def split_string(string, length, start=0, tail=True):
    while start + length < len(string):
        yield string[start:start+length]
        start += length + 1

    if tail:
        yield string[start:]

def block_print(text, width=8, columns=4):
    for i, part in enumerate(split_string(text, width)):
        sys.stdout.write("  %s" % part)
        if (i % columns) == (columns - 1):
            sys.stdout.write("\n")

    if (i % columns) != (columns - 1):
        sys.stdout.write("\n")

def all_ngrams(text, n):
    """Yields all n-grams in the text."""
    for s in range(len(text)-n+1):
        yield text[s:s+n]

def ngrams(text, n=1, minimum=0):
    """Returns (n-grams, count) that appear a minimum times in the text."""
    counts = collections.defaultdict(int)

    for gram in all_ngrams(text, n):
        counts[gram] += 1

    out = []

    for gram, count in sorted(counts.items(), reverse=True):
        if count >= minimum:
            out.append((gram, count))

    return sorted(out, reverse=True)

def digrams(text, minimum=0):
    return ngrams(text, 2, minimum)

def trigrams(text, minimum=0):
    return ngrams(text, 3, minimum)

def quadgrams(text, minimum=0):
    return ngrams(text, 4, minimum)
