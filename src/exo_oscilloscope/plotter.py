"""Sample doc string."""

from typing import Callable

import pyqtgraph as pg
from loguru import logger
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QHBoxLayout, QWidget

from exo_oscilloscope.config.definitions import APP_NAME
from exo_oscilloscope.data_classes import IMUData
from exo_oscilloscope.panels import IMUPanel


class ExoPlotter:
    """Main application class for the exoskeleton plotting UI."""

    def __init__(self) -> None:
        logger.info("Starting the exosuit oscilloscope pipeline.")

        self.pg = pg
        self.name = APP_NAME
        self._timer: QTimer | None = None

        # Qt application + main window
        self.app = QApplication([])
        self.window = QWidget()
        self.window.setWindowTitle(self.name)

        # Main layout
        self.main_layout = QHBoxLayout()
        self.window.setLayout(self.main_layout)

        # Create IMU panels
        self.left_panel = IMUPanel(title_prefix="Left")
        self.right_panel = IMUPanel(title_prefix="Right")

        # Add panels to the layout
        self.main_layout.addLayout(self.left_panel.layout)
        self.main_layout.addLayout(self.right_panel.layout)

    def plot_left(self, imu: IMUData) -> None:
        """Plot left IMU data."""
        self.left_panel.update(imu)

    def plot_right(self, imu: IMUData) -> None:
        """Plot right IMU data."""
        self.right_panel.update(imu)

    def run(
        self,
        update_callback: Callable[[], None] | None = None,
        delay_millisecond: int = 5,
    ) -> None:
        """Run the GUI event loop.

        :param update_callback: Repeated callback for simulation or live data.
        :param delay_millisecond: Delay between timer callbacks.
        """
        self.window.show()

        if update_callback is not None:
            timer = QTimer()
            timer.timeout.connect(update_callback)
            timer.start(delay_millisecond)
            self._timer = timer  # Keep reference so it does not get garbage collected

        self.app.exec()

    def close(self) -> None:
        """Close the application."""
        logger.info(f"Closing {self.name}...")
        self.window.close()
        self.app.quit()
        logger.success(f"{self.name} is now closed.")
