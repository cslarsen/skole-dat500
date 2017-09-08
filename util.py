import collections
import sys

def normalize(s):
    s = s.replace(" ", "")
    s = s.replace("\n", "")
    s = s.replace("\r", "")
    s = s.strip().upper()
    return s

def reverse_pairs(pairs):
    for a, b in pairs:
        yield (b, a)

def encrypt(key, text):
    pass

def read_file(filename="cipher.txt"):
    with open(filename, "rt") as f:
        return normalize(f.read())

def relative_freqs(text):
    frequencies = collections.Counter(text)

    for character, count in frequencies.items():
        yield (float(count) / len(text), character)

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
