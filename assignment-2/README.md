DAT-510 Assignment 2
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

On a UNIX system, just type `make` and `libsdes.so` should be built.
