"""
Python interface for the C++ Simplified DES (SDES) symmetric cipher.

This module wraps the shared library libsdes.so, which must reside in a library
path or in the current directory. If the module reports errors loading
libsdes.so, you can specify an environment variable LIBSDES_PATH to the
directory containing it.

Written by Christian Stigen
"""

import ctypes
import os

LIBSDES_PATH = os.getenv("LIBSDES_PATH", os.getcwd())
libsdes = ctypes.CDLL(os.path.join(LIBSDES_PATH, "libsdes.so"))

uint8ptr = ctypes.POINTER(ctypes.c_uint8)

# The bruteforce_result struct
class BruteforceResult(ctypes.Structure):
    _fields_ = [("count", ctypes.c_uint32),
                ("key", ctypes.c_uint32)]

class Buffer(ctypes.Structure):
    _fields_ = [("length", ctypes.c_uint32),
                ("data", ctypes.POINTER(ctypes.c_uint8))]

_bruteforce_3sdes_key = libsdes.bruteforce_3sdes_key
_bruteforce_3sdes_key.argtypes = [ctypes.POINTER(ctypes.c_uint8),
        ctypes.c_uint32, ctypes.c_uint8, ctypes.c_uint8]
_bruteforce_3sdes_key.restype = BruteforceResult

def bruteforce_3sdes_key(ciphertext, start, stop):
    raw = (ctypes.c_uint8*len(ciphertext)).from_buffer_copy(ciphertext)
    bf = _bruteforce_3sdes_key(raw, len(raw), start, stop)
    return bf

_triplesdes_decrypt_buffer = libsdes.triplesdes_decrypt_buffer
_triplesdes_decrypt_buffer.argtypes = [ctypes.c_uint16, ctypes.c_uint16,
        ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint8)]
_triplesdes_decrypt_buffer.restype = ctypes.POINTER(Buffer)

def triplesdes_decrypt_buffer(k1, k2, ciphertext):
    raw = (ctypes.c_uint8*len(ciphertext)).from_buffer_copy(ciphertext)
    result = _triplesdes_decrypt_buffer(k1, k2, len(raw), raw)
    length = result.contents.length
    plaintext = "".join(chr(c) for c in result.contents.data[:length])
    return plaintext

p10 = libsdes.p10
p10.argtypes = [ctypes.c_uint16]
p10.restype = ctypes.c_uint16

p8 = libsdes.p8
p8.argtypes = [ctypes.c_uint16]
p8.restype = ctypes.c_uint8

p4 = libsdes.p4
p4.argtypes = [ctypes.c_uint8]
p4.restype = ctypes.c_uint8

ip = libsdes.ip
ip.argtypes = [ctypes.c_uint8]
ip.restype = ctypes.c_uint8

revip = libsdes.revip
revip.argtypes = [ctypes.c_uint8]
revip.restype = ctypes.c_uint8

ep = libsdes.ep
ep.argtype = [ctypes.c_uint8]
ep.restype = ctypes.c_uint8

sw = libsdes.sw
sw.argtypes = [ctypes.c_uint8]
sw.restype = ctypes.c_uint8

rol5 = libsdes.rol5
rol5.argtypes = [ctypes.c_uint8]
rol5.restype = ctypes.c_uint8

shiftl5 = libsdes.shiftl5
shiftl5.argtypes = [ctypes.c_uint16]
shiftl5.restype = ctypes.c_uint16

S0 = libsdes.S0
S0.argtypes = [ctypes.c_uint8, ctypes.c_uint8]
S0.restype = ctypes.c_uint8

S1 = libsdes.S1
S1.argtypes = [ctypes.c_uint8, ctypes.c_uint8]
S1.restype = ctypes.c_uint8

create_subkeys = libsdes.create_subkeys
create_subkeys.argtypes = [ctypes.c_uint32]
create_subkeys.restype = ctypes.c_uint32

Fmap = libsdes.Fmap
Fmap.argtypes = [ctypes.c_uint8, ctypes.c_uint8]
Fmap.restype = ctypes.c_uint8

fK = libsdes.fK
fK.argtypes = [ctypes.c_uint16, ctypes.c_uint8]
fK.restype = ctypes.c_uint8

encrypt = libsdes.encrypt
encrypt.argtypes = [ctypes.c_uint32, ctypes.c_uint8]
encrypt.restype = ctypes.c_uint8

decrypt = libsdes.decrypt
decrypt.argtypes = [ctypes.c_uint32, ctypes.c_uint8]
decrypt.restype = ctypes.c_uint8

triplesdes_encrypt = libsdes.triplesdes_encrypt
triplesdes_encrypt.argtypes = [ctypes.c_uint16, ctypes.c_uint16, ctypes.c_uint8]
triplesdes_encrypt.restype = ctypes.c_uint8

triplesdes_decrypt = libsdes.triplesdes_decrypt
triplesdes_decrypt.argtypes = [ctypes.c_uint16, ctypes.c_uint16, ctypes.c_uint8]
triplesdes_decrypt.restype = ctypes.c_uint8
