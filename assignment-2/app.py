import math
import random

# Local imports
from bbs import BlumBlumShub
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

    # TODO: This is not entirely correct
    generator = 2

    while True:
        q = mr.find_prime(bits-1, acc1)
        p = 2*q + 1 # used to prevent small subgroup attacks, se Stallings
        if mr.probably_prime(p, acc2):
            return q, p, generator

def numbits(n):
    """Returns the number of bits requires to represent n."""
    return int(math.ceil(math.log(n, 2)))

def dh_exchange(address, puba):
    pass

def generate_keypair(prng, generator, p, q, priv=None):
    if priv is None:
        # Allow to use a predefined private key
        priv = prng.randint(2, q-1)

    F = GF(p)
    g = F(generator)
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
    print("=== Finding global %d-bit parameters ===" % bits)
    q, p, generator = get_global_params(bits)
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
    print("      generator = %d" % generator)
    print("")

    print("Initializing Blum Blum Shub CSPRNG")
    bbs = BlumBlumShub.create(bits)
    print("  p = 0x%x" % bbs.p)
    print("    = %d" % bbs.p)
    print("      (%d bits)" % numbits(int(bbs.p)))
    print("  q = 0x%x" % bbs.q)
    print("    = %d" % bbs.q)
    print("      (%d bits)" % numbits(int(bbs.q)))
    print("  m = 0x%x" % bbs.m)
    print("      %d" % bbs.m)
    print("      (%d bits)" % numbits(int(bbs.m)))
    print("")

    #priva, puba = generate_keypair(p, q, 312)
    priva, puba = generate_keypair(bbs, generator, p, q)
    print("Keys for Alice")
    print("  privkey = 0x%x" % priva)
    print("          = %d" % priva)
    print("            (%d bits)" % numbits(int(priva)))
    print("  pubkey  = 0x%x" % puba)
    print("          = %d" % puba)
    print("            (%d bits)" % numbits(int(puba)))
    print("")

    #privb, pubb = generate_keypair(p, q, 24)
    privb, pubb = generate_keypair(bbs, generator, p, q)
    print("Keys for Bob")
    print("  privkey = 0x%x" % privb)
    print("          = %d" % privb)
    print("            (%d bits)" % numbits(int(privb)))
    print("  pubkey  = 0x%x" % pubb)
    print("          = %d" % pubb)
    print("            (%d bits)" % numbits(int(pubb)))
    print("")

    #pubb = dh_exchange(bob, puba)

    aliceKab = create_shared_key(priva, pubb)
    bobKab = create_shared_key(privb, puba)
    print("Alice shared key: %d" % aliceKab)
    print("Bob shared key  : %d" % bobKab)
    if aliceKab == bobKab:
        print("Shared key (hex): 0x%x" % aliceKab)
        print("                  (%d bits)" % numbits(int(aliceKab)))

    assert(aliceKab == bobKab)

    csprng = create_csprng(aliceKab)

    plain = "hello world"
    cipher = encrypt(csprng, plain)
    send(cipher, bob)

if __name__ == "__main__":
    main()
