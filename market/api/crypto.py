from hashlib import sha1

from M2Crypto import EC
from market.dispersy.crypto import ECCrypto, _CURVES

_DEFAULT_CURVE = u'high'

def generate_key(curve=_DEFAULT_CURVE):
    """
    Generate public/private key with the given curve (defaults to 'high')
    Based on the implementation in `<market/dispersy/createkey.py>`

    :param _curve: unicode The curve level, can be 'very-low', 'low', 'medium', 'high'.
    :return: A tuple (public_key_bin(HEX), private_key_bin(HEX), public_key, private_key)
    """
    eccrypto = ECCrypto()

    private_pem = ""
    public_pem = ""

    ec = eccrypto.generate_key(curve)

    private_pem = ec.key_to_pem()
    public_pem = ec.pub().key_to_pem()
    private_bin = eccrypto.key_to_bin(ec)
    public_bin = eccrypto.key_to_bin(ec.pub())

    return (public_bin.encode("HEX"), private_bin.encode("HEX"), public_pem.strip(), private_pem.strip())




