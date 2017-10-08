import math
import random

# Local imports
from galois import GF
import miller_rabin as mr

def is_prime(n):
    accuracy = mr.estimate_accuracy(numbits(n))
    return mr.probably_prime(n, accuracy)

def get_global_params(bits):
    # Domain parameters
    # Choose a prime q so that p=2q+1 is also prime

    acc1 = mr.estimate_accuracy(bits-1)
    acc2 = mr.estimate_accuracy(bits)

    # TODO: Fix this
    fval = random.randint(2, 100000)

    while True:
        q = mr.find_prime(bits-1, acc1)
        p = 2*q + 1 # used to prevent small subgroup attacks, se Stallings
        if mr.probably_prime(p, acc2):
            return q, p, fval

def numbits(n):
    """Returns the number of bits requires to represent n."""
    return int(math.ceil(math.log(n, 2)))

def dh_exchange(address, puba):
    pass

def generate_keypair(fval, p, q, priv=None):
    # NOTE: need to look into 2 here, F(3) => 2 but F(2) => 1!!!!
    if priv is None:
        priv = random.randint(2, q-1)
    F = GF(p)
    g = F(fval)
    print("g^q = %s" % g**q)
    pub = g**priv
    return priv, pub

def create_csprng(seed):
    pass

def encrypt(prng, plain):
    pass

def create_shared_key(pubkey, privkey):
    return privkey**pubkey

def send(address, data):
    pass

def main():
    bob = "some remote host"
    bits = 128
    print("Finding global %d-bit parameters" % bits)
    q, p, fval= get_global_params(bits)
    #q = 761
    #p = 2*q + 1

    print("Global parameters:")
    print("  q = 0x%x" % q)
    print("    = %d" % q)
    print("      (%d bits)" % numbits(q))
    print("      prime(q): %s" % is_prime(q))
    print("  p = 2q+1")
    print("    = 0x%x" % p)
    print("    = %d" % p)
    print("      (%d bits)" % numbits(p))
    print("      prime(p): %s" % is_prime(p))
    print("  fval = 0x%x" % fval)
    print("       = %d" % fval)
    print("")

    #priva, puba = generate_keypair(p, q, 312)
    priva, puba = generate_keypair(fval, p, q)
    print("Keys for Alice")
    print("  privkey = 0x%x" % priva)
    print("          = %d" % priva)
    print("  pubkey  = 0x%x" % puba)
    print("          = %d" % puba)
    print("")

    #privb, pubb = generate_keypair(p, q, 24)
    privb, pubb = generate_keypair(fval, p, q)
    print("Keys for Bob")
    print("  privkey = 0x%x" % privb)
    print("          = %d" % privb)
    print("  pubkey  = 0x%x" % pubb)
    print("          = %d" % pubb)
    print("")

    #pubb = dh_exchange(bob, puba)

    aliceKab = create_shared_key(priva, pubb)
    bobKab = create_shared_key(privb, puba)
    print("Alice shared key: %d" % aliceKab)
    print("Bob shared key  : %d" % bobKab)

    assert(aliceKab == bobKab)

    csprng = create_csprng(aliceKab)

    plain = "hello world"
    cipher = encrypt(csprng, plain)
    send(cipher, bob)

if __name__ == "__main__":
    main()
