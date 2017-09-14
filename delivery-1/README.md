DAT-510 Assignment 1
====================

Everything here has been written by Christian Stigen. I have not reused code
from anywhere else.

Requirements
============

  * Python 2.7 or 3+, only standard libraries
  * A C++11 compiler, preferably gcc or clang on UNIX. That means you must have
    a gcc version later than 4.8 or something like that.
  * GNU Make

How to run with `make`
======================

The task solutions can be built and run by make:

    $ make task1
    $ make task2
    $ make task3

How to run manually
===================

You can run them manually as well. See below.

Task 1: Decipher polyalphabetic Vigenère cipher
-----------------------------------------------

    $ python vigenere.txt --verbose cipher-vigenere.txt

Task 2: Recover SDES key and plaintext
--------------------------------------

You need to build the C++ shared library that will be used by the Python
front-end:

    $ make libsdes.so

If you fail to build it, you can attempt to do it by hand:

    $ g++ -O3 -march=native -shared -fPIC sdes.cpp -olibsdes.so

If you are on Windows, I believe the code needs DLL declarations for the public
functions. I have not tested this. Please contact me if this is the case, and I
will fix it for you. The easiest way, though, is to find a UNIX machine and
compile there.

After building the above shared library, run the Python driver program:

    $ python bruteforce.py --sdes ctx1.txt

Task 3: Recover TripleSDES key and plaintext
--------------------------------------------

This also uses the SDES C++ library above, `libsdes.so`. See above
instructions. To run the Python front-end:

    $ python bruteforce.py ctx2.txt

Report
======

See the PDF file for the report with more details.
