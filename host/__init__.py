"""
Host backend package for the FullCTRL 3D printer controller.

This package is intended to run on a Raspberry Pi 4 and expose:
- A REST API for configuration and high-level commands.
- WebSocket endpoints for telemetry and real-time control.
- A serial link manager for talking to the SKR-mini-E3-V3.0 board.
"""

