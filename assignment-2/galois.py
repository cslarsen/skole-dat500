from miller_rabin import pow_mod

class IntMod(object):
    """Modulus integral arithmetic.

    Do not attempt to use this with floats, they will be converted to integers
    using ``int``.
    """
    def __init__(self, value, modulus):
        self.mod = modulus
        self.val = value % self.mod

    def _set(self, value):
        self.val = value % self.mod

    def __add__(self, n):
        return IntMod(self.val + int(n), self.mod)

    def __mul__(self, n):
        return IntMod(self.val * int(n), self.mod)

    def __sub__(self, n):
        return IntMod(self.val - int(n), self.mod)

    def __pow__(self, exponent):
        # We absolutely must do it this way, otherwise it will be too slow!
        result = pow_mod(self.val, int(exponent), self.mod)
        return IntMod(result, self.mod)

    def __div__(self, n):
        return IntMod(self.val / int(n), self.mod)

    def __floordiv__(self, n):
        return IntMod(self.val // int(n), self.mod)

    def __eq__(self, n):
        return self.val == int(n)

    def __neq__(self, n):
        return self.val != int(n)

    def __repr__(self):
        return "%d (mod %d)" % (self.val, self.mod)

    def __str__(self):
        return str(self.val)

    def __int__(self):
        return self.val

def GF(p):
    """Constructor for a finite Galois Field."""
    return lambda n: IntMod(n, p)

def test():
    q = 761
    p = 2*q + 1
    F = GF(p)
    g = F(3)
    x = 312
    X = g**x
    print("got %d" % X)
    print(" or %r" % X)

if __name__ == "__main__":
    test()
    # Example usage
    q = 761
    p = 2*q + 1
    F = GF(p)
    g = F(3)

    def check(result, expect):
        assert(result == expect)
        print(result)

    check(g**q, 1)
    x = 312
    X = g**x
    check(X, 26)
    y = 24
    Y = g**y
    check(Y, 1304)
    check(Y**x, 541)
    check(X**y, 541)

