"""
Core service layer for the FullCTRL backend.

This subpackage holds the main host-side abstractions:
- SerialLinkManager: low-level USB CDC serial handling and protocol framing.
- MotionPlanner: G-code parsing, lookahead, and move segmentation.
- PrinterStateManager: high-level view of printer state (positions, temps, job).
- ConfigManager: loading/validating printer configuration files.
- JobManager: orchestrates print jobs and real-time control sources.
"""

