# -*- encoding: utf-8 -*-

"""
Utility library used for all the tasks.

Written by Christian Stigen
"""

import sys

def normalize(s):
    """Removes whitespace from string and makes it uppercase."""
    out = ""
    for ch in s:
        if not ch.isspace():
            out += ch
    return out.upper()

def transpose(text, table, default="."):
    """Transposes (translates) characters in a string based on table, using
    default if not found."""
    return "".join(table.get(char, default) for char in text)

def readfile(filename):
    """Returns normalized text in file."""
    with open(filename, "rt") as f:
        return normalize(f.read())

def split_string(string, length, start=0, tail=True):
    """Splits string up in given lengths, with a tail that can be less than
    that."""
    while start + length < len(string):
        yield string[start:start+length]
        start += length

    if tail:
        yield string[start:]

def block_print(text, width=8, columns=4, indent="  ", spacing=" ", stop=None,
        stream=sys.stdout):
    """Prints text in columns."""
    for i, part in enumerate(split_string(text, width)):
        if i == 0:
            stream.write(indent)
        stream.write("%s%s" % (part, spacing))
        if (i % columns) == (columns - 1):
            stream.write("\n")
            if (i+1) == stop:
                break
            stream.write(indent)

    if (i % columns) != (columns - 1):
        stream.write("\n")
