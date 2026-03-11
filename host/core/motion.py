from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from host.core.printer_state import PrinterStateManager


@dataclass
class GCodeCommand:
    raw: str


class MotionPlanner:
    """
    Host-side motion planner.

    The motion planner is responsible for:
    - Parsing G-code into an internal representation.
    - Performing lookahead and applying acceleration/jerk limits.
    - Segmenting motion into small blocks suitable for MCU execution.
    - Cooperating with real-time control (e.g. jog moves) and job queues.

    This is currently a thin skeleton focused on defining interfaces.
    """

    def __init__(self, printer_state: PrinterStateManager) -> None:
        self.printer_state = printer_state

    def enqueue_gcode_stream(self, lines: Iterable[str]) -> None:
        """
        Accept a stream of G-code lines associated with a print job.

        The details of queuing, segmentation, and communication with the
        MCU are intentionally left for later implementation so that we can
        stabilise the surrounding architecture first.
        """
        for line in lines:
            cmd = self.parse_gcode_line(line)
            self._handle_parsed_command(cmd)

    def parse_gcode_line(self, line: str) -> GCodeCommand:
        """
        Very small placeholder parser.

        A real implementation will need to handle comments, checksums,
        modal state, and numeric parameters.
        """
        cleaned = line.strip()
        return GCodeCommand(raw=cleaned)

    def _handle_parsed_command(self, cmd: GCodeCommand) -> None:
        """
        Handle a parsed G-code command.

        This is where motion planning and protocol encoding will be added.
        """
        _ = cmd  # placeholder until implemented

    def plan_realtime_jog(self, axes: dict[str, float]) -> List[bytes]:
        """
        Plan a short-horizon real-time jog move for the given axes.

        Returns a list of protocol frames (as bytes) to be sent to the MCU.
        The exact encoding will be defined alongside the protocol spec.
        """
        _ = axes
        return []

