from __future__ import annotations

from pathlib import Path
from typing import Iterable

from host.core.motion import MotionPlanner
from host.core.printer_state import PrinterStateManager
from host.core.serial_link import SerialLinkManager


class JobManager:
    """
    Coordinates print jobs and real-time motion/control streams.

    Responsibilities:
    - Store uploaded G-code files on disk.
    - Manage a single active job at a time.
    - Feed job G-code into the MotionPlanner.
    - Reserve space for a high-priority real-time control path (jogging,
      emergency stop) that can pre-empt jobs.
    """

    def __init__(
        self,
        motion_planner: MotionPlanner,
        serial_link: SerialLinkManager,
        printer_state: PrinterStateManager,
        jobs_dir: Path | None = None,
    ) -> None:
        self.motion_planner = motion_planner
        self.serial_link = serial_link
        self.printer_state = printer_state
        self.jobs_dir = jobs_dir or Path(__file__).resolve().parents[2] / "jobs"
        self.jobs_dir.mkdir(parents=True, exist_ok=True)

    def store_job(self, name: str, gcode_lines: Iterable[str]) -> Path:
        """
        Persist a G-code job to disk.
        """
        path = self.jobs_dir / f"{name}.gcode"
        with path.open("w", encoding="utf-8") as fp:
            for line in gcode_lines:
                fp.write(line.rstrip("\n") + "\n")
        return path

    # Placeholders for job lifecycle operations. Implementations will be
    # added as the motion and protocol layers mature.
    def start_job(self, path: Path) -> None:  # pragma: no cover - stub
        _ = path

    def pause_job(self) -> None:  # pragma: no cover - stub
        ...

    def resume_job(self) -> None:  # pragma: no cover - stub
        ...

    def cancel_job(self) -> None:  # pragma: no cover - stub
        ...

