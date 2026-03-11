from __future__ import annotations

"""
Host-side helpers for encoding and decoding protocol frames.

The layout matches docs/protocol.md:

  sync (2 bytes)   : 0xAA, 0x55
  version (1 byte) : 0x01
  type (1 byte)    : message type
  seq (2 bytes)    : sequence number
  length (2 bytes) : payload length N
  payload (N bytes)
  crc16 (2 bytes)  : CRC16-CCITT over version..payload
"""

from dataclasses import dataclass
from typing import Final


SYNC0: Final[int] = 0xAA
SYNC1: Final[int] = 0x55
VERSION: Final[int] = 0x01


@dataclass
class Frame:
    msg_type: int
    seq: int
    payload: bytes


def _crc16_ccitt(data: bytes, initial: int = 0xFFFF) -> int:
    crc = initial
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
            crc &= 0xFFFF
    return crc


def encode_frame(frame: Frame) -> bytes:
    length = len(frame.payload)
    header = bytes(
        [
            SYNC0,
            SYNC1,
            VERSION,
            frame.msg_type & 0xFF,
            frame.seq & 0xFF,
            (frame.seq >> 8) & 0xFF,
            length & 0xFF,
            (length >> 8) & 0xFF,
        ]
    )
    crc_input = header[2:] + frame.payload
    crc = _crc16_ccitt(crc_input)
    crc_bytes = bytes([crc & 0xFF, (crc >> 8) & 0xFF])
    return header + frame.payload + crc_bytes

