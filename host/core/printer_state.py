from __future__ import annotations

from dataclasses import dataclass, field, asdict
from threading import Lock
from typing import Dict, Literal, TypedDict


PrinterStatus = Literal["idle", "printing", "paused", "error"]


@dataclass
class AxisState:
    position_mm: float = 0.0


@dataclass
class HeaterState:
    current_temp_c: float = 0.0
    target_temp_c: float = 0.0
    is_on: bool = False


@dataclass
class PrinterState:
    status: PrinterStatus = "idle"
    axes: Dict[str, AxisState] = field(
        default_factory=lambda: {axis: AxisState() for axis in ("X", "Y", "Z", "E")}
    )
    heaters: Dict[str, HeaterState] = field(
        default_factory=lambda: {"hotend": HeaterState(), "bed": HeaterState()}
    )
    active_job: str | None = None
    progress: float = 0.0


class PrinterStateSnapshot(TypedDict):
    status: PrinterStatus
    axes: Dict[str, Dict[str, float]]
    heaters: Dict[str, Dict[str, float | bool]]
    active_job: str | None
    progress: float


class PrinterStateManager:
    """
    Thread-safe container for the current high-level printer state.

    This does not attempt to model every possible firmware detail; it is a
    host-side view suitable for API responses and UI updates. The serial
    link and motion planner are responsible for driving updates into this
    object as messages are exchanged with the MCU.
    """

    def __init__(self) -> None:
        self._state = PrinterState()
        self._lock = Lock()

    def snapshot(self) -> PrinterStateSnapshot:
        with self._lock:
            state_dict = asdict(self._state)

        axes = {
            name: {"position_mm": axis["position_mm"]}
            for name, axis in state_dict["axes"].items()
        }
        heaters = {
            name: {
                "current_temp_c": heater["current_temp_c"],
                "target_temp_c": heater["target_temp_c"],
                "is_on": heater["is_on"],
            }
            for name, heater in state_dict["heaters"].items()
        }

        return PrinterStateSnapshot(
            status=state_dict["status"],
            axes=axes,
            heaters=heaters,
            active_job=state_dict["active_job"],
            progress=state_dict["progress"],
        )

    def update_axis_position(self, axis: str, position_mm: float) -> None:
        with self._lock:
            if axis not in self._state.axes:
                self._state.axes[axis] = AxisState()
            self._state.axes[axis].position_mm = position_mm

    def update_heater(
        self, name: str, current_temp_c: float | None = None, target_temp_c: float | None = None
    ) -> None:
        with self._lock:
            heater = self._state.heaters.setdefault(name, HeaterState())
            if current_temp_c is not None:
                heater.current_temp_c = current_temp_c
            if target_temp_c is not None:
                heater.target_temp_c = target_temp_c
            heater.is_on = heater.target_temp_c > 0.0

    def set_status(self, status: PrinterStatus) -> None:
        with self._lock:
            self._state.status = status

    def set_active_job(self, job_name: str | None, progress: float = 0.0) -> None:
        with self._lock:
            self._state.active_job = job_name
            self._state.progress = progress

