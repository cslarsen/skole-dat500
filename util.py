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
