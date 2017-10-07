"""
Implementation of the Blum Blum Shub algorithm.

Written by Christian Stigen
"""

from miller_rabin import probably_prime, find_prime

def is_coprime(a, b):
    """Determines if the numbers are co-prime."""
    if a in (0,1) or b in (0,1):
        return False
    a, b = min(a, b), max(a, b)

    # Do not use floating point ops here, because then we drop accuracy
    div = b // a
    return div*a != b

def create_seed(length):
    # Read three bytes and use that to produce a 20-bit seed
    with open("/dev/urandom", "rb") as f:
        bytes = f.read(length)
        seed = 0
        for n in range(length):
            seed = seed << 8 | ord(bytes[n])
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

    def __next__(self):
        output = 0
        for n in range(self.bits):
            previous = self.x
            self.x = self.x**2 % self.m
            output = (output<<1) | (previous & 1)
        return output

    def next(self):
        # Python 2 compatibility
        return self.__next__()

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
            accuracy = prime_bits

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
    for index, number in enumerate(BlumBlumShub(3, 11, 19)):
        if index > 10:
            break
        print(number)
