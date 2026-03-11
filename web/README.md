## Web UI

The web frontend provides:

- A **dashboard** showing printer status, temperatures, axis positions,
  print progress, and an emergency stop control.
- A **manual control** panel for jogging axes and extruder with
  “hold-to-move” buttons.
- A **G-code console** for sending ad-hoc commands and viewing responses.
- A **configuration editor** for modifying `config/printer.yaml` via the
  backend API.
- A **jobs** view for uploading G-code files and starting/stopping prints.

### Data flows

- The UI connects to:
  - `GET /api/printer/state` for initial state.
  - `GET /ws/telemetry` for continuous updates (temperatures, position,
    active job, progress).
  - `POST /api/printer/command/*` for high-level actions (home, move,
    set temperatures, emergency stop).
  - `POST /api/printer/gcode` for one-off G-code commands.
  - `GET/POST /api/config/printer` to load and save configuration.
  - `POST /api/jobs/upload` and `/api/jobs/start` to manage jobs.

- Jogging (“hold-to-move”):
  - When a jog button is pressed, the UI opens or uses an existing
    WebSocket connection and sends frequent `jog` messages with target
    velocities per axis.
  - When the button is released (or on `mouseup`/`touchend`/disconnect),
    the UI sends a `jog_stop` message, and the backend forwards an
    `RT_STOP_MOTION` command to the MCU.

An actual implementation can be created with React/Vite and compiled into
static assets served by the backend.

