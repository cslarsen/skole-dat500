"""
Implementation of the Blum Blum Shub algorithm.

Written by Christian Stigen
"""

import math
from miller_rabin import probably_prime, find_prime

def is_coprime(a, b):
    """Determines if the numbers are co-prime."""
    if a in (0,1) or b in (0,1):
        return False
    a, b = min(a, b), max(a, b)

    # Do not use floating point ops here, because then we drop accuracy
    quotient = b // a
    return quotient*a != b

def create_seed(length):
    # Read three bytes and use that to produce a 20-bit seed
    with open("/dev/urandom", "rb") as f:
        rbytes = f.read(length)
        seed = 0
        for n in range(length):
            byte = rbytes[n]
            if isinstance(byte, int):
                # Python 3.x
                seed = (seed << 8) | byte
            else:
                # Python 2.x
                seed = (seed << 8) | ord(rbytes[n])
        return seed

class BlumBlumShub(object):
    def __init__(self, seed, p, q, bits=8):
        """
        Args:
            seed: The initial seed, which must be coprime to p and q
            p: A prime number that is congruent to 3 (mod 4)
            q: Another prime congruent to 3 (mod 4)
            bits: The number of output bits in each number
        """

        # The two primes p and q should both be congruent to 3 (mod 4) and
        # gcd(phi(p), phi(q)) should be small (this makes the cycle length
        # large)
        self.p = p
        self.q = q
        self.m = self.p * self.q

        self.bits = bits

        # The seed must be coprime to pq, i.e. p and q should not be factors of
        # the seed, and should not be 1 or 0.
        self.seed = seed
        self.x = self.seed

        # Assert that the seed is not coprime to M
        if p == q:
            raise ValueError("p and q must be different")
        if not is_coprime(self.seed, self.p):
            raise ValueError("p and seed are not coprime")
        if not is_coprime(self.seed, self.q):
            raise ValueError("q and seed are not coprime")

    def __iter__(self):
        return self

    def _next(self):
        # Note that the very first number (the seed) is never returned
        self.x = self.x**2 % self.m
        return self.x

    def get_random_bits(self, bits):
        n = 0
        for _ in range(bits):
            n <<= 1
            n |= self._next() & 1
        return n

    def __next__(self):
        # Computes the next random number by taking the LSB of the next
        # generated number.
        return self.get_random_bits(self.bits)

    def next(self):
        # Function provided for Python 2 compatibility
        return self.__next__()

    def randint(self, start, stop):
        """Returns a uniformly random number in the given, inclusive range."""
        if stop <= start:
            raise ValueError("stop must be higher than start")

        # Number of bits we need
        bits = int(math.ceil(math.log(stop, 2)))

        while True:
            n = self.get_random_bits(bits)
            if start <= n <= stop:
                return n

    @staticmethod
    def create(prime_bits, accuracy=None, bits=8, seed=None):
        """Creates a Blum Blum Shub generator.

        Args:
            prime_bits: Number of bits in prime numbers p and q
            accuracy: Setting for the Miller-Rabin primality test used in
                      finding p and q. If None, use prime_bits as accuracy.
            bits: Number of output bits in generator
            seed: The initial seed of the generator. If None, will read a
                  random seed from /dev/urandom.
        """
        if accuracy is None:
            accuracy = int(math.ceil(0.5*math.log(2**prime_bits)))

        if seed in (0, 1):
            raise ValueError("The seed cannot be zero or one")

        if seed is None:
            length = prime_bits // 8
            assert(length > 0)
            seed = create_seed(length)

        def make_prime(seed, bits, accuracy):
            """Creates a prime number that is congruent to 3 (mod 4) and is
            coprime to the seed."""
            while True:
                p = find_prime(bits, accuracy)
                if (p % 4) != 3:
                    continue
                if not is_coprime(seed, p):
                    continue
                return p

        p = make_prime(seed, prime_bits, accuracy)
        q = make_prime(seed, prime_bits, accuracy)

        # NOTE: gcd(phi(p), phi(q)) should be small, because it makes the cycle
        # length large. We do not check that here.
        return BlumBlumShub(seed, p, q)

if __name__ == "__main__":
    print("Creating bbs generator")
    bbs = BlumBlumShub.create(32)
    print("p = %d" % bbs.p)
    print("q = %d" % bbs.q)
    print("seed = %d" % bbs.seed)

    for index, number in enumerate(bbs):
        if index > 10:
            break
        print(number)

    print("Known numbers:")
    bbs = BlumBlumShub(3, 11, 19)
    for i in range(10):
        print(bbs._next())
