DAT-510 Assignment 1
====================

This contains the PDF report and code for the first assignment.

Everything here has been written by Christian Stigen. I have not reused code
from anywhere else.

Requirements
============

You will need a *UNIX* system with:

  * A C++11 compiler for the SDES back-end code, preferably gcc or clang.
  * GNU Make to build the C++ code
  * Python 2.7 or 3+, to run the SDES front-end and the other programs. It only
    uses standard libraries.

The C++ code can be compiled on Windows as well, but I don't have access to it,
so I haven't been able to test the code. But, in general, what you need to make
it work is:

  * Add DLL `__declspec(dllexport)` to public functions in `sdes.cpp`
  * Set the environment variable `LIBSDES_BASE=sdes.dll`

How to build the shared library
===============================

On a UNIX system, just type `make`, and `libsdes.so` should be built.

If you fail to build it, you can attempt to do it by hand:

    $ g++ -O3 -march=native -shared -fPIC sdes.cpp -olibsdes.so

How to run the code
===================

To recover the Vigenère cipher, run

    $ python vigenere.py --verbose cipher-vigenere.txt

To complete the SDES tables in tasks 1 and 2:

    $ python task1.py
    $ python task2.py

To recover the 10-bit SDES key and plaintext:

    $ python bruteforce.py --sdes ctx1.txt

To crack the 20-bit TripleSDES key and recover the plaintext:

    $ python bruteforce.py ctx2.txt

Files in this directory
=======================

    bruteforce.py          SDES and TripleSDES cracker
    cipher-vigenere.txt    The polyalphabetic cipher
    csdes.py               Bindings to C++ SDES implementation
    ctx1.txt               SDES ciphertext
    ctx2.txt               TripleSDES ciphertext
    Makefile               For building the C++ library
    README.md              This file
    sdes.cpp               C++ SDES implementation
    task1.py               Fills out SDES tables
    task2.py               Fills out TripleSDES tables
    util.py                Utility functions
    vigenere.py            Vigenere cipher cracker

Report
======

See the PDF file for the report with more details.
