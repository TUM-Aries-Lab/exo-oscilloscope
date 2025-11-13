"""Sample doc string."""

import numpy as np
import pyqtgraph as pg
from loguru import logger
from PySide6 import QtCore, QtWidgets

APP_NAME = "Exo-Oscilloscope"
BUFFER_SIZE = 500
PENS = ["r", "g", "b", "c", "m", "y", "k", "v"]


class ExoPlotter:
    """Main application class for the exoskeleton plotting UI."""

    def __init__(self) -> None:
        # Store references so the rest of the class can use them
        self.QtWidgets = QtWidgets
        self.QtCore = QtCore
        self.pg = pg
        self.name = APP_NAME

        # Initialize the Qt application
        self.app = QtWidgets.QApplication([])

        # Root window
        self.window = QtWidgets.QWidget()
        self.window.setWindowTitle(self.name)

        # Layout
        self.layout = QtWidgets.QVBoxLayout()
        self.window.setLayout(self.layout)

        # ---------------------------------------------------------
        # Internal buffers and plot widgets
        # ---------------------------------------------------------
        self.buffer_size = BUFFER_SIZE

        # buffers: shape (3, N) for accel/gyro/mag
        self.accel_buf = np.zeros((3, self.buffer_size))
        self.gyro_buf = np.zeros((3, self.buffer_size))
        self.mag_buf = np.zeros((3, self.buffer_size))
        self.quat_buf = np.zeros((4, self.buffer_size))

        # Create plot widgets
        self.accel_plot = pg.PlotWidget(title="Accelerometer")
        self.gyro_plot = pg.PlotWidget(title="Gyroscope")
        self.mag_plot = pg.PlotWidget(title="Magnetometer")
        self.quat_plot = pg.PlotWidget(title="Quaternion")

        self.layout.addWidget(self.accel_plot)
        self.layout.addWidget(self.gyro_plot)
        self.layout.addWidget(self.mag_plot)
        self.layout.addWidget(self.quat_plot)

        # Create curve lines
        self.accel_curves = [self.accel_plot.plot(pen=PENS[i]) for i in range(3)]
        self.gyro_curves = [self.gyro_plot.plot(pen=PENS[i]) for i in range(3)]
        self.mag_curves = [self.mag_plot.plot(pen=PENS[i]) for i in range(3)]
        self.quat_curves = [self.quat_plot.plot(pen=PENS[i]) for i in range(4)]

    # -------------------------------------------------------------
    # NEW METHOD — plot IMUData
    # -------------------------------------------------------------
    def plot_imu(self, imu) -> None:
        """Update the plots using a new IMUData sample.

        :param imu: IMUData instance containing accel, gyro, mag vectors.
        """
        # roll buffers left
        self.accel_buf = np.roll(self.accel_buf, -1, axis=1)
        self.gyro_buf = np.roll(self.gyro_buf, -1, axis=1)
        self.mag_buf = np.roll(self.mag_buf, -1, axis=1)
        self.quat_buf = np.roll(self.quat_buf, -1, axis=1)

        # push new values
        self.accel_buf[:, -1] = imu.accel.to_tuple()
        self.gyro_buf[:, -1] = imu.gyro.to_tuple()
        self.mag_buf[:, -1] = imu.mag.to_tuple()
        self.quat_buf[:, -1] = imu.quat.to_tuple()

        # update curves
        for i in range(3):
            self.accel_curves[i].setData(self.accel_buf[i])
            self.gyro_curves[i].setData(self.gyro_buf[i])
            self.mag_curves[i].setData(self.mag_buf[i])

        for i in range(4):
            self.quat_curves[i].setData(self.quat_buf[i])

    def run(self) -> None:
        """Run the Qt event loop."""
        self.window.show()
        self.app.exec()

    def close(self) -> None:
        """Close the window and stop the Qt event loop."""
        logger.info(f"Closing {self.name}...")
        self.window.close()
        self.app.quit()
        logger.success(f"{self.name} is now closed.")
