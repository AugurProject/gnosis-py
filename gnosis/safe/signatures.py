from typing import List, Tuple, Union

from ethereum.utils import checksum_encode, ecrecover_to_pub, sha3
from hexbytes import HexBytes


def signature_split(signatures: Union[bytes, str], pos: int = 0) -> Tuple[int, int, int]:
    """
    :param signatures: signatures in form of {bytes32 r}{bytes32 s}{uint8 v}
    :param pos: position of the signature
    :return: Tuple with v, r, s
    """
    signatures = HexBytes(signatures)
    signature_pos = 65 * pos
    v = signatures[64 + signature_pos]
    r = int.from_bytes(signatures[signature_pos:32 + signature_pos], 'big')
    s = int.from_bytes(signatures[32 + signature_pos:64 + signature_pos], 'big')

    return v, r, s


def signature_to_bytes(vrs: Tuple[int, int, int]) -> bytes:
    """
    Convert signature to bytes
    :param vrs: tuple of v, r, s
    :return: signature in form of {bytes32 r}{bytes32 s}{uint8 v}
    """

    byte_order = 'big'
    v, r, s = vrs

    return (r.to_bytes(32, byteorder=byte_order) +
            s.to_bytes(32, byteorder=byte_order) +
            v.to_bytes(1, byteorder=byte_order))


def signatures_to_bytes(signatures: List[Tuple[int, int, int]]) -> bytes:
    """
    Convert signatures to bytes
    :param signatures: list of tuples(v, r, s)
    :return: 65 bytes per signature
    """
    return b''.join([signature_to_bytes(vrs) for vrs in signatures])


def get_signing_address(signed_hash: Union[bytes, str], v: int, r: int, s: int) -> str:
    """
    :return: checksummed ethereum address, for example `0x568c93675A8dEb121700A6FAdDdfE7DFAb66Ae4A`
    :rtype: str
    """
    encoded_64_address = ecrecover_to_pub(HexBytes(signed_hash), v, r, s)
    address_bytes = sha3(encoded_64_address)[-20:]
    return checksum_encode(address_bytes)
