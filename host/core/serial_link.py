from __future__ import annotations

from dataclasses import dataclass
from threading import Lock
from typing import Optional

import glob

import serial  # type: ignore[import-untyped]


@dataclass
class SerialSettings:
    port: Optional[str] = None
    baudrate: int = 250000
    timeout_s: float = 0.1


class SerialLinkManager:
    """
    Manages the low-level USB CDC serial connection to the SKR controller.

    The initial implementation only defines the interface and does not
    depend on any particular serial library. A concrete implementation
    can be added later (e.g. using pyserial) while tests can use in-memory
    fakes.
    """

    def __init__(self, settings: Optional[SerialSettings] = None) -> None:
        self.settings = settings or SerialSettings()
        self._lock = Lock()
        self._connected = False
        self._ser: Optional[serial.Serial] = None

    def connect(self) -> None:
        """
        Establish a connection to the SKR board.

        If a port is specified in settings, that is used directly.
        Otherwise this will attempt to auto-detect a suitable USB CDC
        device using common patterns (/dev/ttyACM*, /dev/ttyUSB*).
        """
        with self._lock:
            if self._connected and self._ser is not None and self._ser.is_open:
                return

            port = self.settings.port
            if port is None:
                candidates = glob.glob("/dev/ttyACM*") + glob.glob("/dev/ttyUSB*")
                if not candidates:
                    raise RuntimeError("No serial candidates found (ttyACM*/ttyUSB*).")
                port = candidates[0]

            self._ser = serial.Serial(
                port=port,
                baudrate=self.settings.baudrate,
                timeout=self.settings.timeout_s,
            )
            self._connected = True

    def disconnect(self) -> None:
        """Close the connection, if any."""
        with self._lock:
            if self._ser is not None and self._ser.is_open:
                self._ser.close()
            self._ser = None
            self._connected = False

    def is_connected(self) -> bool:
        with self._lock:
            return self._connected

    def send(self, payload: bytes) -> None:
        """
        Send a raw payload to the controller.

        Higher-level code is responsible for encoding protocol frames.
        """
        with self._lock:
            if not self._connected or self._ser is None or not self._ser.is_open:
                raise RuntimeError("Serial link is not connected.")
            self._ser.write(payload)

    def receive(self, max_bytes: int = 4096) -> bytes:
        """
        Receive up to max_bytes from the controller.

        This will be replaced by an event-driven reader in the future.
        """
        with self._lock:
            if not self._connected or self._ser is None or not self._ser.is_open:
                raise RuntimeError("Serial link is not connected.")
            return self._ser.read(max_bytes)

