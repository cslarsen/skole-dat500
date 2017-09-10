Coursework for DAT-500
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

Requirements
============

Python 2.7 or 3.3+ with standard libraries such as zlib.

References
----------

  * (Cornell Cryptography)[https://www.math.cornell.edu/~mec/2003-2004/cryptography/subs/hints.html}
  * (Google 10000 English Words)[https://github.com/first20hours/google-10000-english]
  * (SDES explanation)[http://mercury.webster.edu/aleshunas/COSC%205130/G-SDES.pdf]
