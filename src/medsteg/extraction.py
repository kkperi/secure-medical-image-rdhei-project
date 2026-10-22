
import json

from medsteg.bitstream import unframe_payload
from medsteg.security import decrypt_metadata


def recover_metadata(tau_bits: str, metadata_key: bytes) -> dict:
    """
    Extract, authenticate, decrypt, and decode patient metadata
    from the reserved-room bitstream.

    tau_bits must begin with a 32-bit payload-length header.
    """
    # 1. Read the length header and extract encrypted bytes
    encrypted_payload = unframe_payload(tau_bits)

    # 2. Authenticate and decrypt using AES-GCM
    metadata_bytes = decrypt_metadata(
        encrypted_payload,
        metadata_key,
    )

    # 3. Convert decrypted JSON bytes into a Python dictionary
    recovered_metadata = json.loads(
        metadata_bytes.decode("utf-8")
    )

    if not isinstance(recovered_metadata, dict):
        raise ValueError("Recovered metadata must be a dictionary")

    return recovered_metadata
