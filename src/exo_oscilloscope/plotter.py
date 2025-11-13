"""Sample doc string."""

import numpy as np
import pyqtgraph as pg
from loguru import logger
from numpy.typing import NDArray
from PySide6 import QtCore, QtWidgets

APP_NAME = "Exo-Oscilloscope"
BUFFER_SIZE = 500

# Distinct, readable colors on white backgrounds
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


# Utility function to create a plot widget with standardized settings
def make_plot(title: str) -> pg.PlotWidget:
    """Make a plot with given title.

    :param title: Plot title.
    :return: Plot object.
    """
    plot = pg.PlotWidget(title=title)
    plot.showGrid(x=True, y=True, alpha=0.3)
    plot.addLegend()
    plot.setBackground("w")
    return plot


class ExoPlotter:
    """Main application class for the exoskeleton plotting UI."""

    def __init__(self) -> None:
        # Store references for easy access
        self.QtWidgets = QtWidgets
        self.QtCore = QtCore
        self.pg = pg
        self.name = APP_NAME

        # Initialize the Qt application
        self.app = QtWidgets.QApplication([])

        # Root window
        self.window = QtWidgets.QWidget()
        self.window.setWindowTitle(self.name)

        # Main horizontal layout: LEFT IMU | RIGHT IMU
        self.main_layout = QtWidgets.QHBoxLayout()
        self.window.setLayout(self.main_layout)

        # Panel layouts for left and right
        self.left_layout = QtWidgets.QVBoxLayout()
        self.right_layout = QtWidgets.QVBoxLayout()

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        # ---------------------------------------------------------
        # Internal buffers
        # ---------------------------------------------------------
        self.buffer_size = BUFFER_SIZE

        self.left_accel_buf = np.zeros((3, self.buffer_size))
        self.left_gyro_buf = np.zeros((3, self.buffer_size))
        self.left_mag_buf = np.zeros((3, self.buffer_size))
        self.left_quat_buf = np.zeros((4, self.buffer_size))

        self.right_accel_buf = np.zeros((3, self.buffer_size))
        self.right_gyro_buf = np.zeros((3, self.buffer_size))
        self.right_mag_buf = np.zeros((3, self.buffer_size))
        self.right_quat_buf = np.zeros((4, self.buffer_size))

        # ---------------------------------------------------------
        # Create LEFT IMU plot widgets
        # ---------------------------------------------------------
        self.left_accel_plot = make_plot("Left Accelerometer")
        self.left_gyro_plot = make_plot("Left Gyroscope")
        self.left_mag_plot = make_plot("Left Magnetometer")
        self.left_quat_plot = make_plot("Left Quaternion")

        self.left_layout.addWidget(self.left_accel_plot)
        self.left_layout.addWidget(self.left_gyro_plot)
        self.left_layout.addWidget(self.left_mag_plot)
        self.left_layout.addWidget(self.left_quat_plot)

        # ---------------------------------------------------------
        # Create RIGHT IMU plot widgets
        # ---------------------------------------------------------
        self.right_accel_plot = make_plot("Right Accelerometer")
        self.right_gyro_plot = make_plot("Right Gyroscope")
        self.right_mag_plot = make_plot("Right Magnetometer")
        self.right_quat_plot = make_plot("Right Quaternion")

        self.right_layout.addWidget(self.right_accel_plot)
        self.right_layout.addWidget(self.right_gyro_plot)
        self.right_layout.addWidget(self.right_mag_plot)
        self.right_layout.addWidget(self.right_quat_plot)

        # Curves (Left Right)
        self.left_accel_curves = [
            self.left_accel_plot.plot(pen=PENS[i], name=f"accel_{i}") for i in range(3)
        ]
        self.left_gyro_curves = [
            self.left_gyro_plot.plot(pen=PENS[i], name=f"gyro_{i}") for i in range(3)
        ]
        self.left_mag_curves = [
            self.left_mag_plot.plot(pen=PENS[i], name=f"mag_{i}") for i in range(3)
        ]
        self.left_quat_curves = [
            self.left_quat_plot.plot(pen=PENS[i], name=f"quat_{i}") for i in range(4)
        ]

        self.right_accel_curves = [
            self.right_accel_plot.plot(pen=PENS[i], name=f"accel_{i}") for i in range(3)
        ]
        self.right_gyro_curves = [
            self.right_gyro_plot.plot(pen=PENS[i], name=f"gyro_{i}") for i in range(3)
        ]
        self.right_mag_curves = [
            self.right_mag_plot.plot(pen=PENS[i], name=f"mag_{i}") for i in range(3)
        ]
        self.right_quat_curves = [
            self.right_quat_plot.plot(pen=PENS[i], name=f"quat_{i}") for i in range(4)
        ]

    # ---------------------------------------------------------------------
    # UPDATE METHODS
    # ---------------------------------------------------------------------
    def _update_buffers(self, buf: NDArray, values: tuple) -> NDArray:
        buf = np.roll(buf, -1, axis=1)
        buf[:, -1] = values
        return buf

    def plot_left(self, imu) -> None:
        """Plot IMUData to the LEFT panel."""
        self.left_accel_buf = self._update_buffers(
            self.left_accel_buf, imu.accel.to_tuple()
        )
        self.left_gyro_buf = self._update_buffers(
            self.left_gyro_buf, imu.gyro.to_tuple()
        )
        self.left_mag_buf = self._update_buffers(self.left_mag_buf, imu.mag.to_tuple())
        self.left_quat_buf = self._update_buffers(
            self.left_quat_buf, imu.quat.to_tuple()
        )

        for i in range(3):
            self.left_accel_curves[i].setData(self.left_accel_buf[i])
            self.left_gyro_curves[i].setData(self.left_gyro_buf[i])
            self.left_mag_curves[i].setData(self.left_mag_buf[i])

        for i in range(4):
            self.left_quat_curves[i].setData(self.left_quat_buf[i])

    def plot_right(self, imu) -> None:
        """Plot IMUData to the RIGHT panel."""
        self.right_accel_buf = self._update_buffers(
            self.right_accel_buf, imu.accel.to_tuple()
        )
        self.right_gyro_buf = self._update_buffers(
            self.right_gyro_buf, imu.gyro.to_tuple()
        )
        self.right_mag_buf = self._update_buffers(
            self.right_mag_buf, imu.mag.to_tuple()
        )
        self.right_quat_buf = self._update_buffers(
            self.right_quat_buf, imu.quat.to_tuple()
        )

        for i in range(3):
            self.right_accel_curves[i].setData(self.right_accel_buf[i])
            self.right_gyro_curves[i].setData(self.right_gyro_buf[i])
            self.right_mag_curves[i].setData(self.right_mag_buf[i])

        for i in range(4):
            self.right_quat_curves[i].setData(self.right_quat_buf[i])

    # ---------------------------------------------------------------------
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
