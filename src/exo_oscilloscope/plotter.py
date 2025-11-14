"""Sample doc string."""

from typing import Callable

import pyqtgraph as pg
from loguru import logger
from PySide6 import QtCore, QtWidgets

from exo_oscilloscope.config.definitions import APP_NAME, BUFFER_SIZE
from exo_oscilloscope.data_classes import IMUData
from exo_oscilloscope.panel import IMUPanel


class ExoPlotter:
    """Main application class for the exoskeleton plotting UI."""

    def __init__(self, buffer_size: int = BUFFER_SIZE) -> None:
        logger.info("Starting the exosuit oscilloscope pipeline.")

        self.QtWidgets = QtWidgets
        self.QtCore = QtCore
        self.pg = pg
        self.name = APP_NAME
        self._timer: QtCore.QTimer | None = None
        self.app = self.QtWidgets.QApplication([])
        self.window = self.QtWidgets.QWidget()
        self.window.setWindowTitle(self.name)

        # Main layout
        self.main_layout = QtWidgets.QHBoxLayout()
        self.window.setLayout(self.main_layout)

        # Create IMU panels (no duplication!)
        self.left_panel = IMUPanel(title_prefix="Left", buffer_size=buffer_size)
        self.right_panel = IMUPanel(title_prefix="Right", buffer_size=buffer_size)

        # Add them to the layout
        self.main_layout.addLayout(self.left_panel.layout)
        self.main_layout.addLayout(self.right_panel.layout)

    # Update functions forward to the panel
    def plot_left(self, imu: IMUData) -> None:
        """Plot left IMU data."""
        self.left_panel.update(imu)

    def plot_right(self, imu: IMUData) -> None:
        """Plot right IMU data."""
        self.right_panel.update(imu)

    def run(
        self,
        update_callback: Callable[[], None] | None = None,
        delay_millisec: int = 5,
    ) -> None:
        """Run the GUI event loop.

        :param update_callback: Callback function that will be called repeatedly
        :param delay_millisec: Delay time in milliseconds between calls.
        """
        self.window.show()

        if update_callback is not None:
            timer = self.QtCore.QTimer()
            timer.timeout.connect(update_callback)
            timer.start(delay_millisec)
            self._timer = timer  # Keep a reference to prevent GC

        self.app.exec()

    def close(self) -> None:
        """Close the application."""
        logger.info(f"Closing {self.name}...")
        self.window.close()
        self.app.quit()
        logger.success(f"{self.name} is now closed.")
