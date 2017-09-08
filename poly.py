import collections
import sys

# english letters relative freqs
english = {
    "a": 8.167,
    "b": 1.492,
    "c": 2.782,
    "d": 4.253,
    "e": 12.702,
    "f": 2.228,
    "g": 2.015,
    "h": 6.094,
    "i": 6.996,
    "j": 0.153,
    "k": 0.772,
    "l": 4.025,
    "m": 2.406,
    "n": 6.749,
    "o": 7.507,
    "p": 1.929,
    "q": 0.095,
    "r": 5.987,
    "s": 6.327,
    "t": 9.056,
    "u": 2.758,
    "v": 0.978,
    "w": 2.360,
    "x": 0.150,
    "y": 1.974,
    "z": 0.074,
}

# common 3-letter words
words3 = ["the", "and", "for", "are", "but", "not", "you", "all", "any", "can",
        "her", "was"]

def letters():
    return "".join(map(lambda (a,b): b, sorted(map(lambda (a,b): (b,a),
        english.items()), reverse=True)))

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

def freqs(text):
    return collections.Counter(text)

def relfreqs(text):
    f = freqs(text)
    out = {}
    for char, count in f.items():
        out[char] = float(count)/float(len(text))
    return out

if __name__ == "__main__":
    encrypted = read_file("cipher.txt")

    print("Encrypted:\n")
    print("%s\n" % encrypted)


    # Find repetitions in the text. Focus on the ones who are a specific period
    # apart.

    good = set()
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
            pos = encrypted.find(key)
            print("len=%-3d pos=%-3d period=%-3dx%d key=%r" % (
                length, pos, per, times, key))
            start += 1

            # Get excerpt
            #if per > 100:
                #continue
            text = encrypted[pos:pos+per]
            print(text)
            f = relfreqs(text)
            f = map(lambda (a,b): (b,a), f.items())
            f = sorted(f, reverse=True)
            print("Relative freqs:")
            for cnt, ch in f:
                print("  %s  %f" % (ch, cnt))
            #print(f)
            table = {}
            # most frequent letter in english decreasingo rder
            dec = letters()
            for no, (count, char) in enumerate(f):
                if no >= len(dec):
                    break
                table[char] = dec[no]
                #print("Guess %s is %s" % (char, dec[no]))
            # decrypt
            for ciph, plain in table.items():
                text = text.replace(ciph, plain)
            print("Decrypted: %s" % text)
            for word in words3:
                if word in text:
                    good.add(text)
                    break
    print("Candidates:")
    for t in good:
        for w in words3:
            t = t.replace(w, " %s " % w.upper())
        while t.find("  ") != -1:
            t = t.replace("  ", " ")
        # make it readable
        print(t)
