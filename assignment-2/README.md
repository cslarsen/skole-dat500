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
  * Python 2.7 only --- Python 3 is not fully supported

The C++ code can be compiled on Windows as well, but I don't have access to it,
so I haven't been able to test the code. But, in general, what you need to make
it work is:

  * Add DLL `__declspec(dllexport)` to public functions in `sdes.cpp`
  * Set the environment variable `LIBSDES_BASE=sdes.dll`

How to build the shared library
===============================

On a UNIX system, just type `make` and `libsdes.so` should be built.

How to run the program
=======================

Start the client by specifying an open port number to listen to:

    $ python app.py --port=3333

On another machine (or in another window on the same machine), start a client
with:

    $ python app.py --remote-host=127.0.0.1 --port=3333

After a while, key exchange will take place. Next, an encrypted chat session is
started.

To see other options for controlling which IKE cyclic group to use, see

    $ python app.py --help

Other programs
==============

To see the C++ version of the Miller-Rabin primality tester, run the following
commands:

    $ make primes
    $ time ./primes

