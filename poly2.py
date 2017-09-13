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

from util import *
import sys
from poly import find_all, period

write = sys.stdout.write

def main():
    ciphertext = readfile("cipher.txt")

    print("Ciphertext:")
    for i, part in enumerate(split_string(ciphertext, 5)):
        write("%s " % part)
        if ((i+1) % 5) == 0:
            write("\n")
    print("")

    # Find repeats, look for the lowest distance between two repeats
    lowest = 999999
    for length in range(3, 11):
        start = 0
        while start+length < len(ciphertext):
            key = ciphertext[start:start+length]
            positions = list(find_all(ciphertext, key))
            if len(positions) > 1:
                if len(positions) == 2:
                    dist = positions[1] - positions[0]
                    if dist < lowest:
                        lowest = dist
                        print("** distance %d between two repeats at %d" %
                                (lowest, positions[0]))
                for pos in positions:
                    write("pos=%3d %11r  " % (pos, ciphertext[pos:pos+length]))
                write("\n")
            start += length

if __name__ == "__main__":
    main()
