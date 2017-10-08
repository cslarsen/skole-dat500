def get_global_params():
    pass

def dh_exchange(params, puba):
    pass

def generate_keypair(params):
    return None, None

def create_csprng(seed):
    pass

def encrypt(prng, plain):
    pass

def create_shared_key(params, puba, pubb):
    pass

def send(address, data):
    pass

def main():
    bob = "some remote host"
    params = get_global_params()
    priva, puba = generate_keypair(params)
    pubb = dh_exchange(params, puba)
    Kab = create_shared_key(params, puba, pubb)
    csprng = create_csprng(Kab)
    # now perform encryption
    plain = "hello"
    cipher = encrypt(csprng, plain)
    send(cipher, bob)

if __name__ == "__main__":
    main()
