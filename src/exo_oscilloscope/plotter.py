"""Sample doc string."""

import pyqtgraph as pg
from loguru import logger
from PySide6 import QtCore, QtWidgets

from exo_oscilloscope.config.definitions import PENS
from exo_oscilloscope.data_classes import IMUData
from exo_oscilloscope.panel import IMUPanel

APP_NAME = "Exo-Oscilloscope"
BUFFER_SIZE = 500


class ExoPlotter:
    """Main application class for the exoskeleton plotting UI."""

    def __init__(self) -> None:
        self.QtWidgets = QtWidgets
        self.QtCore = QtCore
        self.pg = pg
        self.name = APP_NAME

        self.app = QtWidgets.QApplication([])
        self.window = QtWidgets.QWidget()
        self.window.setWindowTitle(self.name)

        # Main layout
        self.main_layout = QtWidgets.QHBoxLayout()
        self.window.setLayout(self.main_layout)

        # Create IMU panels (no duplication!)
        self.left_panel = IMUPanel("Left", BUFFER_SIZE, PENS)
        self.right_panel = IMUPanel("Right", BUFFER_SIZE, PENS)

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

    def run(self) -> None:
        """Run the main loop."""
        self.window.show()
        self.app.exec()

    def close(self) -> None:
        """Close the application."""
        logger.info(f"Closing {self.name}...")
        self.window.close()
        self.app.quit()
        logger.success(f"{self.name} is now closed.")
