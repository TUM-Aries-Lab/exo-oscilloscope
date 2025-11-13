"""Sample doc string."""

import numpy as np
import pyqtgraph as pg
from numpy.typing import NDArray
from PySide6 import QtWidgets

APP_NAME = "Exo-Oscilloscope"
BUFFER_SIZE = 500


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


class IMUPanel:
    """UI container + buffers + curves for a single IMU."""

    def __init__(self, title_prefix: str, buffer_size: int, pens: list) -> None:
        self.buffer_size = buffer_size
        self.pens = pens

        # Buffers
        self.accel_buf = np.zeros((3, buffer_size))
        self.gyro_buf = np.zeros((3, buffer_size))
        self.mag_buf = np.zeros((3, buffer_size))
        self.quat_buf = np.zeros((4, buffer_size))

        # Layout for this panel
        self.layout = QtWidgets.QVBoxLayout()

        # Create the 4 plot widgets
        self.accel_plot = make_plot(f"{title_prefix} Accelerometer")
        self.gyro_plot = make_plot(f"{title_prefix} Gyroscope")
        self.mag_plot = make_plot(f"{title_prefix} Magnetometer")
        self.quat_plot = make_plot(f"{title_prefix} Quaternion")

        self.layout.addWidget(self.accel_plot)
        self.layout.addWidget(self.gyro_plot)
        self.layout.addWidget(self.mag_plot)
        self.layout.addWidget(self.quat_plot)

        # Curves
        self.accel_curves = [
            self.accel_plot.plot(pen=pens[i], name=f"accel_{i}") for i in range(3)
        ]
        self.gyro_curves = [
            self.gyro_plot.plot(pen=pens[i], name=f"gyro_{i}") for i in range(3)
        ]
        self.mag_curves = [
            self.mag_plot.plot(pen=pens[i], name=f"mag_{i}") for i in range(3)
        ]
        self.quat_curves = [
            self.quat_plot.plot(pen=pens[i], name=f"quat_{i}") for i in range(4)
        ]

    @staticmethod
    def _update(buf: NDArray, values: tuple) -> None:
        # Shift everything left by 1
        buf[:, :-1] = buf[:, 1:]
        # Insert the newest values
        buf[:, -1] = values

    def update(self, imu) -> None:
        """Update this panel with new IMUData."""
        self._update(self.accel_buf, imu.accel.to_tuple())
        self._update(self.gyro_buf, imu.gyro.to_tuple())
        self._update(self.mag_buf, imu.mag.to_tuple())
        self._update(self.quat_buf, imu.quat.to_tuple())

        for i in range(3):
            self.accel_curves[i].setData(self.accel_buf[i])
            self.gyro_curves[i].setData(self.gyro_buf[i])
            self.mag_curves[i].setData(self.mag_buf[i])

        for i in range(4):
            self.quat_curves[i].setData(self.quat_buf[i])
