from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from host.core.config import ConfigManager
from host.core.printer_state import PrinterStateManager
from host.core.serial_link import SerialLinkManager
from host.core.jobs import JobManager
from host.core.motion import MotionPlanner
from host.core.protocol import Frame, encode_frame


def create_app() -> FastAPI:
    """
    Application factory for the FullCTRL backend.

    This function wires together the core services and exposes a minimal
    subset of the intended API surface. It is deliberately small so it
    can serve as an integration point while the rest of the system is
    built out.
    """
    app = FastAPI(title="FullCTRL 3D Printer Host", version="0.1.0")

    # Core services
    config_manager = ConfigManager()
    serial_link = SerialLinkManager()
    printer_state = PrinterStateManager()
    motion_planner = MotionPlanner(printer_state=printer_state)
    job_manager = JobManager(
        motion_planner=motion_planner,
        serial_link=serial_link,
        printer_state=printer_state,
    )

    @app.get("/", response_class=HTMLResponse)
    async def root() -> str:
        return "<html><body><h1>FullCTRL backend is running.</h1></body></html>"

    @app.get("/api/printer/state")
    async def get_printer_state():
        return printer_state.snapshot()

    @app.post("/api/debug/ping")
    async def debug_ping():
        """
        Send a minimal ping frame over the serial link.

        This is useful for verifying that the Pi can talk to the SKR once
        firmware-side handling is in place.
        """
        try:
            serial_link.connect()
        except Exception as exc:  # pragma: no cover - thin wrapper around serial
            raise HTTPException(status_code=500, detail=str(exc)) from exc

        frame = Frame(msg_type=0x01, seq=1, payload=b"PING")
        encoded = encode_frame(frame)
        try:
            serial_link.send(encoded)
        except Exception as exc:  # pragma: no cover
            raise HTTPException(status_code=500, detail=str(exc)) from exc

        # For now we do not require a response; this endpoint only confirms
        # that sending does not raise an exception.
        return {"status": "sent", "bytes": len(encoded)}

    @app.post("/api/printer/command/home")
    async def home_all_axes():
        # Placeholder for high-level home command.
        # Eventually this will emit appropriate protocol messages and update state.
        return {"status": "not_implemented"}

    @app.websocket("/ws/telemetry")
    async def telemetry_ws(websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                # In a real implementation we would push periodic state updates here.
                # For now, echo any text we receive so the plumbing can be tested.
                data = await websocket.receive_text()
                await websocket.send_text(f"echo: {data}")
        except WebSocketDisconnect:
            # Client disconnected; nothing else to do.
            return

    return app


app = create_app()

