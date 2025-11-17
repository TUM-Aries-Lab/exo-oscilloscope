"""Sample doc string."""

import numpy as np
from loguru import logger
from PySide6 import QtWidgets

from exo_oscilloscope.config.definitions import BUFFER_SIZE, MOTOR_COLORS
from exo_oscilloscope.data_classes import MotorData
from exo_oscilloscope.panels.plot_utils import make_plot


class MotorPanel:
    """UI container + buffers + curves for a single IMU."""

    def __init__(self, title_prefix: str) -> None:
        """Initialize the panel.

        :param title_prefix: prefix for title
        """
        logger.debug("Initializing Motor panel.")
        self.buffer_size = BUFFER_SIZE
        self.pens = MOTOR_COLORS

        # Buffers
        self.position_buf = np.zeros(self.buffer_size)
        self.time_buf = np.zeros(self.buffer_size)

        # Layout for this panel
        self.layout = QtWidgets.QVBoxLayout()

        # Create the 4 plot widgets
        self.position = make_plot(f"{title_prefix} Position", "deg")

        self.layout.addWidget(self.position)

        # Curves
        self.position_curve = self.position.plot(
            pen=self.pens[0], name="Motor Position"
        )

    def update(self, motor_data: MotorData) -> None:
        """Update this panel with new IMUData.

        :param motor_data: MotorData to update
        :return: None
        """
        # --- shift time once ---
        self.time_buf[:-1] = self.time_buf[1:]
        self.time_buf[-1] = motor_data.timestamp

        # --- shift data once per group, but DO NOT shift time again --
        self.position_buf[:-1] = self.position_buf[1:]

        # --- insert new values ---
        self.position_buf[-1] = motor_data.position

        # --- update curves ---
        self.position_curve.setData(self.time_buf, self.position_buf)
