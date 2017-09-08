import collections
import sys

def normalize(s):
    s = s.replace(" ", "")
    s = s.replace("\n", "")
    s = s.replace("\r", "")
    s = s.strip().upper()
    return s

def encrypt(key, text):
    pass

def read_file(filename="cipher.txt"):
    with open(filename, "rt") as f:
        return normalize(f.read())

def alphas(start, length):
    start = ord(start) - ord('A')
    for n in range(length):
        yield chr(ord('A') + ((start + n) % length))

def show_table():
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

def find_all(haystack, needle):
    start = 0
    while start  < len(haystack):
        found = haystack.find(needle, start)
        if found == -1:
            break
        yield found
        start += found + 1

def period(positions):
    return list(map(lambda (a,b): b-a, zip(positions, positions[1:])))

if __name__ == "__main__":
    encrypted = read_file("cipher.txt")

    print("Encrypted:\n")
    print("%s\n" % encrypted)


    # Find repetitions in the text. Focus on the ones who are a specific period
    # apart.

    for length in range(3, len(encrypted)//2):
        start = 0
        while start+length < len(encrypted):
            key = encrypted[start:start+length]
            positions = list(find_all(encrypted, key))
            if len(positions) < 2:
                start += 1
                continue
            per = list(set(period(positions)))
            times = len(per)
            if len(per) != 1:
                start += 1
                continue
            per = per[0]
            print("length %3d, key: %r, period: %3d, times: %d" % (length, key, per, times))
            start += 1
