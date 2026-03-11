## Scripts

- `install.sh` – one-command installer for Raspberry Pi OS Lite.

Intended usage on a fresh Pi:

```bash
git clone <repo-url> fullctrl
cd fullctrl
./scripts/install.sh
```

The installer will:

- Install core system packages (Python, nginx, ARM GCC, CMake).
- Create a Python virtual environment and install backend dependencies.
- Register and start a `fullctrl-backend.service` systemd unit on port 8080.

Firmware build and flashing helpers will be added alongside the MCU bring-up.

