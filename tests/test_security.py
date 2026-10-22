
import pytest
from cryptography.exceptions import InvalidTag

from src.medsteg.security import (
    generate_key,
    encrypt_metadata,
    decrypt_metadata,
)


def test_encryption_round_trip():
    key = generate_key()
    original = b'{"patient_id":"PATIENT_001"}'

    encrypted = encrypt_metadata(original, key)

    assert encrypted != original
    assert decrypt_metadata(encrypted, key) == original


def test_tampering_is_detected():
    key = generate_key()
    encrypted = bytearray(
        encrypt_metadata(b"test metadata", key)
    )

    encrypted[-1] ^= 1

    with pytest.raises(InvalidTag):
        decrypt_metadata(bytes(encrypted), key)


import pytest

from medsteg.security import decrypt_metadata, encrypt_metadata, generate_key


def test_wrong_key_cannot_decrypt_payload():
    key1 = generate_key()
    key2 = generate_key()

    encrypted = encrypt_metadata(b"test metadata", key1)

    with pytest.raises(Exception):
        decrypt_metadata(encrypted, key2)


def test_truncated_payload_is_rejected():
    key = generate_key()

    with pytest.raises(ValueError):
        decrypt_metadata(b"short", key)
