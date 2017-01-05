"""
Utility functions based on ECCrypto
"""

from dispersy.crypto import ECCrypto


def get_public_key(private_key):
    """
    Get the public key pertaining to a private_key
    :param private_key: The private key, encoded in HEX
    :return: Returns the public key encoded in HEX
    """
    eccrypto = ECCrypto()
    try:
        if eccrypto.is_valid_private_bin(private_key.decode("HEX")):
            priv = eccrypto.key_from_private_bin(private_key.decode("HEX"))
            return priv.pub().key_to_bin().encode("HEX")
        return None
    except TypeError:
        return None
