"""Common definitions for this module."""

from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pyqtgraph as pg

np.set_printoptions(precision=3, floatmode="fixed", suppress=True)


# --- Directories ---
ROOT_DIR: Path = Path("src").parent
DATA_DIR: Path = ROOT_DIR / "data"
RECORDINGS_DIR: Path = DATA_DIR / "recordings"
LOG_DIR: Path = DATA_DIR / "logs"

# Default encoding
ENCODING: str = "utf-8"

DATE_FORMAT = "%Y-%m-%d_%H-%M-%S"

DUMMY_VARIABLE = "dummy_variable"


@dataclass
class LogLevel:
    """Log level."""

    trace: str = "TRACE"
    debug: str = "DEBUG"
    info: str = "INFO"
    success: str = "SUCCESS"
    warning: str = "WARNING"
    error: str = "ERROR"
    critical: str = "CRITICAL"

    def __iter__(self):
        """Iterate over log levels."""
        return iter(asdict(self).values())


DEFAULT_LOG_LEVEL = LogLevel.info
DEFAULT_LOG_FILENAME = "log_file"

PENS = [
    pg.mkPen("#1f77b4", width=2),  # blue
    pg.mkPen("#ff7f0e", width=2),  # orange
    pg.mkPen("#2ca02c", width=2),  # green
    pg.mkPen("#d62728", width=2),  # red
    pg.mkPen("#9467bd", width=2),  # purple
    pg.mkPen("#8c564b", width=2),  # brown
    pg.mkPen("#e377c2", width=2),  # pink
    pg.mkPen("#7f7f7f", width=2),  # gray
]
APP_NAME = "Exo-Oscilloscope"
BUFFER_SIZE = 200
