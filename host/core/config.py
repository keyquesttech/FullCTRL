from pathlib import Path
from typing import Any, Dict

import yaml


class ConfigError(Exception):
    """Raised when configuration is invalid or cannot be loaded."""


class ConfigManager:
    """
    Manages printer configuration files on the host.

    Configuration is stored as YAML under the top-level config/ directory,
    typically in a file such as config/printer.yaml. The structure is
    intentionally generic so it can evolve without requiring firmware
    changes for every field.
    """

    def __init__(self, base_dir: Path | None = None) -> None:
        self.base_dir = base_dir or Path(__file__).resolve().parents[2]
        self.config_dir = self.base_dir / "config"
        self._printer_config: Dict[str, Any] = {}

    @property
    def printer_config_path(self) -> Path:
        return self.config_dir / "printer.yaml"

    def load_printer_config(self) -> Dict[str, Any]:
        """
        Load the current printer configuration from disk.

        This performs minimal validation for now; a dedicated validation
        layer can be added as the schema stabilises.
        """
        if not self.printer_config_path.exists():
            self._printer_config = {}
            return self._printer_config

        try:
            data = yaml.safe_load(self.printer_config_path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - thin wrapper
            raise ConfigError(f"Failed to load config: {exc}") from exc

        if not isinstance(data, dict):
            raise ConfigError("Printer configuration must be a mapping at the top level.")

        self._printer_config = data
        return self._printer_config

    def save_printer_config(self, cfg: Dict[str, Any]) -> None:
        """
        Persist the given printer configuration to disk.

        The caller is responsible for ensuring that the configuration has
        been validated.
        """
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.printer_config_path.write_text(
            yaml.safe_dump(cfg, sort_keys=True), encoding="utf-8"
        )
        self._printer_config = cfg

    def get_current_config(self) -> Dict[str, Any]:
        """
        Return the in-memory configuration if available, otherwise load it.
        """
        if not self._printer_config:
            return self.load_printer_config()
        return self._printer_config

