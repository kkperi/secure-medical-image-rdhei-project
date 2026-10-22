
from src.medsteg.metadata import (
    validate_metadata,
    serialize_metadata,
)


def test_valid_metadata_serializes():
    metadata = {
        "patient_id": "PATIENT_001",
        "scan_id": "SCAN_001",
        "scan_date": "2026-10-21",
        "version": 1,
    }

    validate_metadata(metadata)
    payload = serialize_metadata(metadata)

    assert isinstance(payload, bytes)
    assert b"PATIENT_001" in payload


def test_missing_field_is_rejected():
    metadata = {
        "patient_id": "PATIENT_001",
        "scan_id": "SCAN_001",
        "scan_date": "2026-10-21",
    }

    try:
        serialize_metadata(metadata)
        assert False, "Expected invalid metadata to fail"
    except ValueError:
        pass


import pytest

from medsteg.metadata import validate_metadata

def test_invalid_scan_date_is_rejected():
    metadata = {
        "patient_id": "PATIENT_001",
        "scan_id": "SCAN_001",
        "scan_date": "21-10-2026",
        "version": 1,
    }

    with pytest.raises(ValueError):
        validate_metadata(metadata)


def test_unsupported_version_is_rejected():
    metadata = {
        "patient_id": "PATIENT_001",
        "scan_id": "SCAN_001",
        "scan_date": "2026-10-21",
        "version": 2,
    }

    with pytest.raises(ValueError):
        validate_metadata(metadata)
