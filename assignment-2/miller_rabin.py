"""
The Miller-Rabin primality tester.

This is a transliteration to Python from code I have made myself years ealiers,
taken from
https://github.com/cslarsen/miller-rabin/blob/master/miller-rabin.cpp

Written by Christian Stigen
"""

import random

def pow_mod(base, exponent, modulus):
    """Calculates a^x mod n

    This algorithm is taken from Bruce Schneier's book "Applied Cryptography".
    See http://en.wikipedia.org/wiki/Modular_exponentiation
    """

    # This is the ordinary way:
    # return a**x % n

    # This way *might* be faster. It *is* in C++ but I'm not sure if it is in
    # Python (TODO: Test if it is, use the fastest one).
    result = 1

    while exponent > 0:
        if (exponent & 1) == 1:
            result = base*result % modulus

        exponent >>= 1
        base = base**2 % modulus

    return result


def probably_prime(n, accuracy):
    """Performs the Miller-Rabin primality test.

    That means that if this returns False, it definitely is not a prime.
    However, if it returns True, it *may* me a prime number.
    """
    if n <= 1:
        return False

    if n == 2 or n == 3:
        return True

    # If n is not an odd number, it cannot be prime
    if not (n & 1):
        return False

    # Now write n-1 as d*2^s by factoring powers of 2 from n-1
    s = 0
    m = n - 1
    while (m & 1) == 0:
        s += 1
        m >>= 1
    # Integer division
    d = (n-1) // (1<<s)

    for i in range(accuracy):
        a = random.randint(2, n-2)
        x = pow_mod(a, d, n)

        if x == 1 or x == n-1:
            continue

        for r in range(s-1):
            x = pow_mod(x, 2, n)
            if x == 1:
                return False
            if x == n - 1:
                break

        if x == n-1:
            continue
        else:
            return False

    # n is probably prime
    return True

def find_prime(bits, accuracy):
    """Finds a random prime number with the given number of bits."""
    a = 1 << (bits-1)
    b = 1 << bits
    while True:
        # NOTE: We are using an insecure random number generator here. Does it
        # matter? Probably not, but worth noting.
        candidate = random.randint(a, b)
        if probably_prime(candidate, accuracy):
            return candidate

if __name__ == "__main__":
    num = 10
    print("Finding %d possible 512-bit prime numbers" % num)

    for n in range(num):
        candidate = find_prime(512, 500)
        print("Decimal:\n%d" % candidate)
        print("Binary:\n%s" % bin(candidate)[2:])
        print("Bits: %d" % len(bin(candidate)[2:]))
        print("")
