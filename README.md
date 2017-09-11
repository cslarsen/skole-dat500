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

For fun, I optimized this in several steps. The original run took 1.5 minutes
with stock Python 2.7, and 2.6s JIT-compiled through pypy. I was able to make
the brute-forcing algorithm smarter by reducing the time complexity from
something like O(n^2) to something more like O(n), where n is the number of
bits in the key (20).

After that, the runtime dropped first to 30s for Python 2.7 and 1.6s for pypy,
then some more optimizations got it down to 10-11s for Python, 0.8s for pypy.
To push the envelope, I implemented SDES in C++. With the unoptimized
brute-force algorithm, it finds the key in less than 0.3s. I can probably get
it below a hundred milliseconds, but at the cost of memory usage. I don't think
it's worth it to spend more time on this, but it may be good later on.

Requirements
============

Python 2.7 or 3.3+ with standard libraries such as zlib.

The C++ implementation of SDES requires a C++ compiler such as clang++ or g++
(LLVM and GCC, respectively).

References
----------

  * (Cornell Cryptography)[https://www.math.cornell.edu/~mec/2003-2004/cryptography/subs/hints.html}
  * (Google 10000 English Words)[https://github.com/first20hours/google-10000-english]
  * (SDES explanation)[http://mercury.webster.edu/aleshunas/COSC%205130/G-SDES.pdf]
