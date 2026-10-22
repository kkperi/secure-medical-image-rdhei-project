
HEADER_BITS = 32


def bytes_to_bits(data: bytes) -> str:
    """Convert bytes into a string of binary bits."""
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")

    return "".join(format(byte, "08b") for byte in data)


def bits_to_bytes(bits: str) -> bytes:
    """Convert a byte-aligned binary string into bytes."""
    if not isinstance(bits, str):
        raise TypeError("bits must be a string")

    if any(bit not in "01" for bit in bits):
        raise ValueError("Bitstream must contain only 0 and 1")

    if len(bits) % 8 != 0:
        raise ValueError("Bitstream must be byte-aligned")

    return bytes(
        int(bits[i:i + 8], 2)
        for i in range(0, len(bits), 8)
    )


def frame_payload(encrypted_payload: bytes) -> str:
    """
    Prefix encrypted payload bits with a 32-bit length header.

    The header stores the payload length in bits.
    """
    payload_bits = bytes_to_bits(encrypted_payload)
    payload_length = len(payload_bits)

    if payload_length >= 2**HEADER_BITS:
        raise ValueError("Payload is too large for the length header")

    header = format(payload_length, f"0{HEADER_BITS}b")
    return header + payload_bits


def unframe_payload(tau_bits: str) -> bytes:
    """Read the length header and recover the encrypted payload."""
    if not isinstance(tau_bits, str):
        raise TypeError("tau_bits must be a string")

    if len(tau_bits) < HEADER_BITS:
        raise ValueError("Bitstream is too short to contain a header")

    header = tau_bits[:HEADER_BITS]

    if any(bit not in "01" for bit in header):
        raise ValueError("Length header must contain only 0 and 1")

    payload_length = int(header, 2)

    if payload_length % 8 != 0:
        raise ValueError("Payload length in header is not byte-aligned")

    payload_end = HEADER_BITS + payload_length

    if payload_end > len(tau_bits):
        raise ValueError("Bitstream is truncated; payload is incomplete")

    payload_bits = tau_bits[HEADER_BITS:payload_end]
    return bits_to_bytes(payload_bits)
