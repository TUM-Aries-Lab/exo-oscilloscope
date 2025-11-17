"""Motor Panel with dynamic buffers + curves."""

from dataclasses import fields

import numpy as np
from loguru import logger
from PySide6 import QtWidgets

from exo_oscilloscope.config.definitions import BUFFER_SIZE, MOTOR_COLORS
from exo_oscilloscope.data_classes import MotorData
from exo_oscilloscope.panels.plot_utils import make_plot


class MotorPanel:
    """UI panel with dynamic buffers + curves for motor signals."""

    def __init__(self, title_prefix: str) -> None:
        logger.debug("Initializing Motor panel.")
        self.buffer_size = BUFFER_SIZE
        self.pens = MOTOR_COLORS

        # -----------------------------------------------------------
        # Discover motor signal names from dataclass
        # (ignore timestamp inherited from BaseData)
        # -----------------------------------------------------------
        self.signal_names = [f.name for f in fields(MotorData) if f.name != "timestamp"]

        # -----------------------------------------------------------
        # Buffers
        # -----------------------------------------------------------
        self.time_buf = np.zeros(self.buffer_size)
        self.buffers = {name: np.zeros(self.buffer_size) for name in self.signal_names}

        # -----------------------------------------------------------
        # Layout
        # -----------------------------------------------------------
        self.layout = QtWidgets.QVBoxLayout()

        # Single combined plot for all motor data
        self.plot_widget = make_plot(f"{title_prefix} Motor Signals", "Value")
        self.layout.addWidget(self.plot_widget)

        # -----------------------------------------------------------
        # Create curves dynamically
        # -----------------------------------------------------------
        self.curves = {}
        for i, name in enumerate(self.signal_names):
            curve = self.plot_widget.plot(
                pen=self.pens[i % len(self.pens)],
                name=name,
            )
            self.curves[name] = curve

    # ------------------------------------------------------------------
    def update(self, motor: MotorData) -> None:
        """Update this panel with new MotorData."""
        # ---- Shift time buffer ----
        self.time_buf[:-1] = self.time_buf[1:]
        self.time_buf[-1] = motor.timestamp

        # ---- Update each signal ----
        for name in self.signal_names:
            buf = self.buffers[name]
            buf[:-1] = buf[1:]
            buf[-1] = getattr(motor, name)

        # ---- Update curves ----
        for name in self.signal_names:
            self.curves[name].setData(self.time_buf, self.buffers[name])
