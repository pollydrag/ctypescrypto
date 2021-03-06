"""
    Interface to the OpenSSL pseudo-random generator
"""

from ctypes import create_string_buffer, c_char_p, c_int, c_double
from ctypescrypto import libcrypto
from ctypescrypto.exception import LibCryptoError

__all__ = ['RandError', 'bytes', 'pseudo_bytes', 'seed', 'status']

class RandError(LibCryptoError):
    """ Exception raised when openssl function return error """
    pass

def bytes(num, check_result=False):
    """
    Returns num bytes of cryptographically strong pseudo-random
    bytes. If checkc_result is True, raises error if PRNG is not
    seeded enough
    """

    if num <= 0:
        raise ValueError("'num' should be > 0")
    buf = create_string_buffer(num)
    result = libcrypto.RAND_bytes(buf, num)
    if check_result and result == 0:
        raise RandError("Random Number Generator not seeded sufficiently")
    return buf.raw[:num]

def pseudo_bytes(num):
    """
    Returns num bytes of pseudo random data.  Pseudo- random byte
    sequences generated by pseudo_bytes() will be unique if
    they are of sufficient length, but are not necessarily
    unpredictable. They can be used for non-cryptographic purposes
    and for certain purposes in cryptographic protocols, but usually
    not for key generation etc.
    """
    if num <= 0:
        raise ValueError("'num' should be > 0")
    buf = create_string_buffer(num)
    libcrypto.RAND_pseudo_bytes(buf, num)
    return buf.raw[:num]

def seed(data, entropy=None):
    """
        Seeds random generator with data.
        If entropy is not None, it should be floating point(double)
        value estimating amount of entropy  in the data (in bytes).
    """
    if not isinstance(data, str):
        raise TypeError("A string is expected")
    ptr = c_char_p(data)
    size = len(data)
    if entropy is None:
        libcrypto.RAND_seed(ptr, size)
    else:
        libcrypto.RAND_add(ptr, size, entropy)

def status():
    """
    Returns 1 if random generator is sufficiently seeded and 0
    otherwise
    """

    return libcrypto.RAND_status()

libcrypto.RAND_add.argtypes = (c_char_p, c_int, c_double)
libcrypto.RAND_seed.argtypes = (c_char_p, c_int)
libcrypto.RAND_pseudo_bytes.argtypes = (c_char_p, c_int)
libcrypto.RAND_bytes.argtypes = (c_char_p, c_int)
