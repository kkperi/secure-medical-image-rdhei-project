import pytest
from cryptography.exceptions import InvalidTag

from medsteg.security import (
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


def test_encryption_uses_fresh_nonce():
    key = generate_key()
    original = b"test metadata"

    encrypted1 = encrypt_metadata(original, key)
    encrypted2 = encrypt_metadata(original, key)

    assert encrypted1 != encrypted2
    assert decrypt_metadata(encrypted1, key) == original
    assert decrypt_metadata(encrypted2, key) == original


def test_wrong_key_is_rejected():
    key1 = generate_key()
    key2 = generate_key()
    encrypted = encrypt_metadata(b"test metadata", key1)

    with pytest.raises(InvalidTag):
        decrypt_metadata(encrypted, key2)


def test_modified_ciphertext_is_rejected():
    key = generate_key()
    encrypted = bytearray(encrypt_metadata(b"test metadata", key))

    # Change the first ciphertext byte after the 12-byte nonce.
    encrypted[12] ^= 1

    with pytest.raises(InvalidTag):
        decrypt_metadata(bytes(encrypted), key)


def test_modified_authentication_tag_is_rejected():
    key = generate_key()
    encrypted = bytearray(encrypt_metadata(b"test metadata", key))

    # The final 16 bytes contain the GCM authentication tag.
    encrypted[-1] ^= 1

    with pytest.raises(InvalidTag):
        decrypt_metadata(bytes(encrypted), key)


def test_truncated_payload_is_rejected():
    key = generate_key()

    with pytest.raises(ValueError, match="too short"):
        decrypt_metadata(b"short", key)


@pytest.mark.parametrize("key", [b"", b"x" * 16, b"x" * 31, b"x" * 33])
def test_encryption_rejects_invalid_key_lengths(key):
    with pytest.raises(ValueError, match="32 bytes"):
        encrypt_metadata(b"test metadata", key)


@pytest.mark.parametrize("key", [b"", b"x" * 16, b"x" * 31, b"x" * 33])
def test_decryption_rejects_invalid_key_lengths(key):
    with pytest.raises(ValueError, match="32 bytes"):
        decrypt_metadata(b"x" * 40, key)
