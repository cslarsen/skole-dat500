from mono import *
from util import *

if __name__ == "__main__":
    ciph = readfile("cipher-mono.txt").lower()
    block_print(ciph)

    print("Letter frequencies")
    print("Ciphertext   English")
    letters = ngrams(ciph, 1, 0, relative=True)
    eletters = list(sorted(en_letters.items(), reverse=True, key=lambda (a,b):
        (b,a)))
    for text, english in zip(letters, eletters):
        print("   %c %5.3f   %c %5.3f" % (text[0], text[1], english[0],
            english[1]))
