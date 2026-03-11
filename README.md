## FullCTRL – Pi + SKR 3D Printer Host

This project provides a Raspberry Pi–hosted web-based 3D printer controller that
talks over USB to an SKR-mini-E3-V3.0 board. The Pi runs a backend service and
web UI; the SKR handles real-time motion, heaters, and IO.

### High-level layout

- `host/` – Python backend (FastAPI) running on the Raspberry Pi
- `web/` – Web frontend (React/Vite) served by the backend
- `firmware/` – SKR-mini-E3-V3.0 MCU firmware
- `config/` – Printer configuration (pin mappings, motion, thermal)
- `docs/` – Protocol and architecture documentation
- `scripts/` – Installation and helper scripts

For now this repository contains the initial architecture skeleton; many parts
are stubs intended to be fleshed out incrementally.

