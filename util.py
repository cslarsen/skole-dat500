import collections

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
