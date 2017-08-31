import collections
import sys

def normalize(s):
    return s.replace(" ", "").strip().upper()

def encrypt(key, text):
    pass

def read_file(filename):
    with open(filename, "rt") as f:
        return f.read()

def alphas(start, length):
    start = ord(start) - ord('A')
    for n in range(length):
        yield chr(ord('A') + ((start + n) % length))

if __name__ == "__main__":
    encrypted = normalize(read_file("poly.txt"))
    print(encrypted)

    table = collections.defaultdict(dict)
    length = ord('Z') - ord('A') + 1

    put = sys.stdout.write
    put("   ")
    for a in alphas('A', length):
        put("%c" % a)
    put("\n   ")
    for a in alphas('A', length):
        put("-")
    put("\n")
    for a in alphas('A', length):
        put("%c: " % a)
        for b in alphas(a, length):
            put("%c" % b)
            table[a][b] = b
        put("\n")
