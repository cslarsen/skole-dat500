import math
import random

# Local imports
from galois import GF
import miller_rabin as mr

def get_global_params(bits):
    # Domain parameters
    # Choose a prime q so that p=2q+1 is also prime

    acc1 = mr.estimate_accuracy(bits-1)
    acc2 = mr.estimate_accuracy(bits)

    while True:
        q = mr.find_prime(bits-1, acc1)
        p = 2*q + 1 # used to prevent small subgroup attacks, se Stallings
        if mr.probably_prime(p, acc2):
            return q, p

def numbits(n):
    """Returns the number of bits requires to represent n."""
    return int(math.ceil(math.log(n, 2)))

def dh_exchange(address, puba):
    pass

def generate_keypair(p, q):
    # NOTE: need to look into 2 here, F(3) => 2 but F(2) => 1!!!!
    priv = random.randint(2, q-1)
    F = GF(p)
    g = F(3)
    print("g^q = %s" % g**q)
    pub = g**priv
    return priv, pub

def create_csprng(seed):
    pass

def encrypt(prng, plain):
    pass

def create_shared_key(g, puba, pubb):
    return g**puba

def send(address, data):
    pass

def main():
    bob = "some remote host"
    bits = 64
    print("Finding global %d-bit parameters" % bits)
    q, p = get_global_params(bits)
    print("Global parameters:")
    print("  q = 0x%x" % q)
    print("    = %d" % q)
    print("     (%d bits)" % numbits(q))
    print("  p = 2q+1")
    print("    = 0x%x" % p)
    print("    = %d" % p)
    print("     (%d bits)" % numbits(p))
    print("")

    F = GF(p)
    g = F(3)
    priva, puba = generate_keypair(p, q)
    print("Keys for Alice")
    print("  privkey = 0x%x" % priva)
    print("          = %d" % priva)
    print("  pubkey = 0x%x" % puba.val)
    print("          = %d" % puba.val)
    print("")

    privb, pubb = generate_keypair(p, q)
    print("Keys for Bob")
    print("  privkey = 0x%x" % privb)
    print("          = %d" % privb)
    print("  pubkey = 0x%x" % pubb.val)
    print("          = %d" % pubb.val)
    print("")

    pubb = dh_exchange(bob, puba)

    aliceKab = create_shared_key(g, puba, pubb)
    bobKab = create_shared_key(g, pubb, puba)
    print("Alice shared key: %d" % aliceKab.val)
    print("Bob shared key  : %d" % bobKab.val)

    csprng = create_csprng(Kab)

    plain = "hello world"
    cipher = encrypt(csprng, plain)
    send(cipher, bob)

if __name__ == "__main__":
    main()
