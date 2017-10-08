import math
import miller_rabin as mr

def get_global_params(bits):
    # Domain parameters
    # Choose a prime q so that p=2q+1 is also prime

    acc1 = mr.estimate_accuracy(bits-1)
    acc2 = mr.estimate_accuracy(bits)

    while True:
        q = mr.find_prime(bits-1, acc1)
        p = 2*q + 1
        if mr.probably_prime(p, acc2):
            return q, p

def numbits(n):
    """Returns the number of bits requires to represent n."""
    return int(math.ceil(math.log(n, 2)))

def dh_exchange(address, puba):
    pass

def generate_keypair(p, q):
    return None, None

def create_csprng(seed):
    pass

def encrypt(prng, plain):
    pass

def create_shared_key(puba, pubb):
    pass

def send(address, data):
    pass

def main():
    bob = "some remote host"
    bits = 256
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

    priva, puba = generate_keypair(p, q)
    pubb = dh_exchange(bob, puba)

    Kab = create_shared_key(puba, pubb)
    csprng = create_csprng(Kab)

    plain = "hello world"
    cipher = encrypt(csprng, plain)
    send(cipher, bob)

if __name__ == "__main__":
    main()
