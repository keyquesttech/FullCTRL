from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from host.core.config import ConfigManager
from host.core.printer_state import PrinterStateManager
from host.core.serial_link import SerialLinkManager
from host.core.jobs import JobManager
from host.core.motion import MotionPlanner


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

