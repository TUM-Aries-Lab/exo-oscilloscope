"""Sample doc string."""

from typing import Callable

import pyqtgraph as pg
from loguru import logger
from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget

from exo_oscilloscope.config.definitions import APP_NAME
from exo_oscilloscope.data_classes import IMUData, MotorData
from exo_oscilloscope.panels import IMUPanel, MotorPanel


class ExoPlotter:
    """Main application class for the exoskeleton plotting UI."""

    def __init__(self) -> None:
        logger.info("Starting the exosuit oscilloscope pipeline.")

        self.pg = pg
        self.name = APP_NAME
        self._timer: QTimer | None = None

        # Qt application + main window
        self.app = QApplication([])
        self.app.setFont(QFont("Helvetica"))

        self.window = QWidget()
        self.window.setWindowTitle(self.name)

        # Main horizontal layout
        self.main_layout = QHBoxLayout()
        self.window.setLayout(self.main_layout)

        # Create IMU and motor panels
        self.left_imu = IMUPanel("Left")
        self.right_imu = IMUPanel("Right")
        self.left_motor = MotorPanel("Left")
        self.right_motor = MotorPanel("Right")

        # Create stacked columns for left and right side
        self.left_column = QVBoxLayout()
        self.right_column = QVBoxLayout()

    def _initialize_panels(self):
        logger.debug("Initialize the plot panels.")

        # Left side stack
        self.left_column.addLayout(self.left_imu.layout)
        self.left_column.addLayout(self.left_motor.layout)

        # Right side stack
        self.right_column.addLayout(self.right_imu.layout)
        self.right_column.addLayout(self.right_motor.layout)

        # Add columns to main horizontal layout
        self.main_layout.addLayout(self.left_column)
        self.main_layout.addLayout(self.right_column)

    def plot_left(self, imu: IMUData, motor: MotorData) -> None:
        """Plot left IMU and motor data."""
        self.left_imu.update(imu)
        self.left_motor.update(motor)

    def plot_right(self, imu: IMUData, motor: MotorData) -> None:
        """Plot right IMU and motor data."""
        self.right_imu.update(imu)
        self.right_motor.update(motor)

    def run(
        self,
        update_callback: Callable[[], None] | None = None,
        delay_millisecond: int = 5,
    ) -> None:
        """Run the GUI event loop."""
        logger.debug("Running the exosuit oscilloscope pipeline.")
        self.window.show()
        self._initialize_panels()

        if update_callback is not None:
            timer = QTimer()
            timer.timeout.connect(update_callback)
            timer.start(delay_millisecond)
            self._timer = timer  # Keep timer alive

        self.app.exec()

    def close(self) -> None:
        """Close the application."""
        logger.info(f"Closing {self.name}...")
        self.window.close()
        self.app.quit()
        logger.success(f"{self.name} is now closed.")
