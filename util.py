import collections
import sys
import zlib

# List of English words
_words = None

def get_words(filename="words.txt.gz"):
    """Returns a list of 230k English words."""
    global _words
    if _words is None:
        _words = read_wordlist(filename)
        _words = set(map(lambda x: x.lower(), _words))
    return _words

def normalize(s):
    """Removes whitespace from string and makes it uppercase."""
    out = ""
    for ch in s:
        if not ch.isspace():
            out += ch
    return out.upper()

def read_wordlist(filename="words.txt.gz"):
    """Reads a (optionally gzipped) wordlist, one word per line.

    Typically, you can use /usr/share/dict/words.
    """
    with open(filename, "rb") as f:
        data = f.read()
        if filename.endswith(".gz"):
            decoder = zlib.decompressobj(16 + zlib.MAX_WBITS) # gzip support
            data = decoder.decompress(data)
        data = str(data.decode("ascii"))
        return data.split()

def reverse_pairs(pairs):
    """Reverses pairs in an iterable."""
    for a, b in pairs:
        yield (b, a)

def subst(text, table, default=""):
    """Translates each character according to table."""
    return "".join(table[c] for c in text)

def readfile(filename):
    """Returns normalized text in file."""
    with open(filename, "rt") as f:
        return normalize(f.read())

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

def snippets(s, minimum=1):
    """Yields all ngrams in text."""
    for start in range(len(s)):
        for length in range(len(s)-start+1):
            snippet = s[start:start+length]
            if len(snippet) >= minimum:
                yield s[start:start+length]

def is_english(text):
    """Attempts to guess if the text is English.

    Returns a number between 0=nope, 1=most likely.
    """
    # Remove non-alphas
    #text = "".join(map(lambda x: x if x.isalpha() else "", text.lower()))

    words = get_words()
    snips = list(snippets(text, 3))

    count = 0
    for snip in snips:
        if snip in words:
            count += 1

    #return count / float(len(snips))
    return count

def ngrams(text, n=1, minimum=0, relative=False):
    """Returns (n-grams, count) that appear a minimum times in the text."""
    counts = collections.defaultdict(int)

    for gram in all_ngrams(text, n):
        counts[gram] += 1

    out = []
    total = sum(counts.values())

    for gram, count in sorted(counts.items(), reverse=True):
        if count >= minimum:
            if relative == True:
                count /= float(total)
            elif relative == "both":
                count = (count, count / float(total))
            out.append((gram, count))

    def sort_by_count(gram_count):
        gram, count = gram_count
        return (count, gram)

    return sorted(out, reverse=True, key=sort_by_count)

def digrams(text, **kw):
    """Wrapper around ngrams(text, 2, ...)"""
    return ngrams(text, 2, **kw)

def trigrams(text, **kw):
    """Wrapper around ngrams(text, 3, ...)"""
    return ngrams(text, 3, **kw)

def quadgrams(text, **kw):
    """Wrapper around ngrams(text, 4, ...)"""
    return ngrams(text, 4, **kw)
