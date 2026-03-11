from __future__ import annotations

from dataclasses import dataclass
from threading import Lock
from typing import Optional


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

    def connect(self) -> None:
        """
        Establish a connection to the SKR board.

        This is a placeholder; in a full implementation this would probe
        for USB serial devices, choose the correct one, and open it.
        """
        with self._lock:
            # TODO: implement real serial discovery and connection.
            self._connected = True

    def disconnect(self) -> None:
        """Close the connection, if any."""
        with self._lock:
            # TODO: close the underlying serial port.
            self._connected = False

    def is_connected(self) -> bool:
        with self._lock:
            return self._connected

    def send(self, payload: bytes) -> None:
        """
        Send a raw payload to the controller.

        Higher-level code is responsible for encoding protocol frames.
        """
        if not self.is_connected():
            raise RuntimeError("Serial link is not connected.")

        # TODO: write to underlying serial port.
        _ = payload  # placeholder to keep linters quiet

    def receive(self, max_bytes: int = 4096) -> bytes:
        """
        Receive up to max_bytes from the controller.

        This will be replaced by an event-driven reader in the future.
        """
        if not self.is_connected():
            raise RuntimeError("Serial link is not connected.")

        # TODO: read from underlying serial port.
        _ = max_bytes
        return b""

