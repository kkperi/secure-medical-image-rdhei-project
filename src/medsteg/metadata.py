
import json
from datetime import date


REQUIRED_FIELDS = {
    "patient_id",
    "scan_id",
    "scan_date",
    "version",
}


def validate_metadata(metadata):
    if not isinstance(metadata, dict):
        raise ValueError("Metadata must be a dictionary")

    if set(metadata.keys()) != REQUIRED_FIELDS:
        raise ValueError("Metadata fields do not match the schema")

    for field in ("patient_id", "scan_id"):
        value = metadata[field]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Invalid {field}")

    try:
        date.fromisoformat(metadata["scan_date"])
    except (TypeError, ValueError):
        raise ValueError("scan_date must use YYYY-MM-DD format")

    if type(metadata["version"]) is not int or metadata["version"] != 1:
        raise ValueError("Unsupported metadata version")

    return metadata


def serialize_metadata(metadata):
    validate_metadata(metadata)

    return json.dumps(
        metadata,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
