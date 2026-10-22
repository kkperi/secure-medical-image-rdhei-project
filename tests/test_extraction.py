
import pytest
from cryptography.exceptions import InvalidTag

from medsteg.bitstream import (
    bytes_to_bits,
    bits_to_bytes,
    frame_payload,
    unframe_payload,
)
from medsteg.extraction import recover_metadata
from medsteg.metadata import serialize_metadata
from medsteg.security import generate_key, encrypt_metadata


@pytest.fixture
def metadata():
    return {
        "patient_id": "PATIENT_001",
        "scan_id": "SCAN_001",
        "scan_date": "2026-10-21",
        "version": 1,
    }


@pytest.fixture
def framed_payload(metadata):
    key = generate_key()
    encrypted = encrypt_metadata(serialize_metadata(metadata), key)
    return metadata, key, frame_payload(encrypted)


def test_bytes_bits_round_trip():
    original = b"medical image metadata"
    assert bits_to_bytes(bytes_to_bits(original)) == original


def test_bits_to_bytes_rejects_invalid_bits():
    with pytest.raises(ValueError):
        bits_to_bytes("0102")


def test_bits_to_bytes_rejects_unaligned_bits():
    with pytest.raises(ValueError):
        bits_to_bytes("101")


def test_framing_round_trip():
    original = b"encrypted metadata"
    assert unframe_payload(frame_payload(original)) == original


def test_unframe_rejects_short_header():
    with pytest.raises(ValueError):
        unframe_payload("0" * 31)


def test_unframe_rejects_truncated_payload():
    framed = frame_payload(b"metadata")
    with pytest.raises(ValueError):
        unframe_payload(framed[:-8])


def test_recover_metadata_success(framed_payload):
    original, key, framed = framed_payload
    assert recover_metadata(framed, key) == original


def test_recover_metadata_rejects_wrong_key(framed_payload):
    _, _, framed = framed_payload
    wrong_key = generate_key()

    with pytest.raises(InvalidTag):
        recover_metadata(framed, wrong_key)


def test_recover_metadata_rejects_tampered_ciphertext(framed_payload):
    _, key, framed = framed_payload

    # Flip one ciphertext bit while leaving the length header intact.
    tampered = framed[:32] + (
        "1" if framed[32] == "0" else "0"
    ) + framed[33:]

    with pytest.raises(InvalidTag):
        recover_metadata(tampered, key)
