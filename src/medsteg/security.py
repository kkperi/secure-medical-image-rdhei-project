
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


NONCE_SIZE = 12


def generate_key():
    """Generate a new 256-bit AES key."""
    return AESGCM.generate_key(bit_length=256)


def encrypt_metadata(metadata_bytes, key):
    """Return nonce + authenticated ciphertext."""
    if len(key) != 32:
        raise ValueError("AES-256 key must be 32 bytes")

    nonce = os.urandom(NONCE_SIZE)
    ciphertext = AESGCM(key).encrypt(
        nonce,
        metadata_bytes,
        None,
    )

    return nonce + ciphertext


def decrypt_metadata(encrypted_payload, key):
    """Authenticate and decrypt the payload."""
    if len(key) != 32:
        raise ValueError("AES-256 key must be 32 bytes")

    if len(encrypted_payload) < NONCE_SIZE + 16:
        raise ValueError("Encrypted payload is too short")

    nonce = encrypted_payload[:NONCE_SIZE]
    ciphertext = encrypted_payload[NONCE_SIZE:]

    return AESGCM(key).decrypt(
        nonce,
        ciphertext,
        None,
    )
