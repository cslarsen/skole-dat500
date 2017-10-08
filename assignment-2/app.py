def get_global_params():
    pass

def dh_exchange(address, puba):
    pass

def generate_keypair(params):
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
    params = get_global_params()

    priva, puba = generate_keypair(params)
    pubb = dh_exchange(bob, puba)

    Kab = create_shared_key(puba, pubb)
    csprng = create_csprng(Kab)

    plain = "hello world"
    cipher = encrypt(csprng, plain)
    send(cipher, bob)

if __name__ == "__main__":
    main()
