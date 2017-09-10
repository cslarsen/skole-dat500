Coursework for DAT-510
======================

Private repository for Christian Stigen Larsen.

Tasks 1 and 2
------------

    $ python sdes.py


Task 3
------

The last message should be run with pypy, otherwise it will be too slow. I
could make a version in C just to show, *or* go deep into the SDES algorithm to
try to break it in a smarter way to save time, but the input text and keyspace
is so low that the most practically effective way is to just brute-force it.

    $ python dec.py # message 1
    $ pypy dec2.py # message 2

Strategy used: Brute-force 10-bit and 20-bit keys. Every time a key decrypts to
a non-printable character (i.e., outside of the ASCII range 32-126), it is
removed from the list of key candidates. Thus, the keyspace is reduced quite
quickly. It seems to be very effective, but for the 20-bit key it takes two
seconds with pypy. For a larger keyspace (52 bit for example), it would still
be viable, but may need to move to C, and for larger keys, need a smarter
approach.

Requirements
============

Python 2.7 or 3.3+ with standard libraries such as zlib.

References
----------

  * (Cornell Cryptography)[https://www.math.cornell.edu/~mec/2003-2004/cryptography/subs/hints.html}
  * (Google 10000 English Words)[https://github.com/first20hours/google-10000-english]
  * (SDES explanation)[http://mercury.webster.edu/aleshunas/COSC%205130/G-SDES.pdf]
