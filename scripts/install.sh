#!/usr/bin/env bash
set -euo pipefail

# Basic installer skeleton for a fresh Raspberry Pi OS Lite system.
# This script is intended to be run after cloning the repository:
#   git clone <repo-url> fullctrl && cd fullctrl
#   ./scripts/install.sh

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y \
  python3 python3-venv python3-pip \
  git \
  nginx \
  gcc-arm-none-eabi make cmake \
  libusb-1.0-0-dev

echo "Setting up Python virtual environment..."
python3 -m venv "${REPO_DIR}/.venv"
source "${REPO_DIR}/.venv/bin/activate"
pip install --upgrade pip
pip install fastapi uvicorn pyyaml pyserial

echo "Creating systemd service for backend..."
sudo mkdir -p /etc/fullctrl
sudo tee /etc/systemd/system/fullctrl-backend.service >/dev/null <<EOF
[Unit]
Description=FullCTRL 3D printer backend
After=network.target

[Service]
Type=simple
WorkingDirectory=${REPO_DIR}
Environment=PATH=${REPO_DIR}/.venv/bin:/usr/bin:/bin
ExecStart=${REPO_DIR}/.venv/bin/uvicorn host.app:app --host 0.0.0.0 --port 8080
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

echo "Enabling and starting backend service..."
sudo systemctl daemon-reload
sudo systemctl enable fullctrl-backend.service
sudo systemctl restart fullctrl-backend.service

echo "Basic install complete. Backend should now be reachable on port 8080."

