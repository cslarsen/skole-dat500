"""
Implementation of the Blum Blum Shub algorithm.

Written by Christian Stigen
"""

class BlumBlumShub(object):
    def __init__(self, seed, p, q):
        """
        Args:
            p, q: Two large prime numbers
        """

        # The two primes p and q should both be congruent to 3 (mod 4) and
        # gcd(phi(p), phi(q)) should be small (this makes the cycle length
        # large)
        self.m = p*q

        # The seed must be coprime to pq, i.e. p and q should not be factors of
        # the seed, and should not be 1 or 0.
        self.seed = seed
        self.x = self.seed

        self.even_parity_bit = 0b011010
        self.odd_parity_bit = 0b100101
        self.lsb = 0b110000

    def __iter__(self):
        return self

    def __next__(self):
        self.x = self.x**2 % self.m
        return self.x

    def next(self):
        # Python 2 compatibility
        return self.__next__()


if __name__ == "__main__":
    bbs = BlumBlumShub(3, 11, 19)
    for index, number in enumerate(BlumBlumShub(3, 11, 19)):
        if index > 10:
            break
        print(number)
