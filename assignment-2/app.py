import miller_rabin

def get_global_params(bits):
    # Domain parameters
    # Choose a prime q so that p=2q+1 is also prime

    accuracy = miller_rabin.estimate_accuracy(bits)

    while True:
        q = miller_rabin.find_prime(bits, accuracy)
        p = 2*q + 1
        if miller_rabin.probably_prime(p, accuracy):
            return q, p

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
    print("  p = 2q+1")
    print("    = 0x%x" % p)
    print("    = %d" % p)

    priva, puba = generate_keypair(p, q)
    pubb = dh_exchange(bob, puba)

    Kab = create_shared_key(puba, pubb)
    csprng = create_csprng(Kab)

    plain = "hello world"
    cipher = encrypt(csprng, plain)
    send(cipher, bob)

if __name__ == "__main__":
    main()
