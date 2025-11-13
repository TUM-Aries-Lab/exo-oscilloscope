"""Sample doc string."""

import numpy as np
import pyqtgraph as pg
from numpy.typing import NDArray
from PySide6 import QtWidgets


def make_plot(title: str, y_label: str) -> pg.PlotWidget:
    """Make a plot with given title and Y-axis label."""
    plot = pg.PlotWidget(title=title)
    plot.showGrid(x=True, y=True, alpha=0.3)
    plot.addLegend()
    plot.setBackground("w")

    plot.setLabel("left", y_label)
    plot.setLabel("bottom", "Time (s)")

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
        self.time_buf = np.zeros(buffer_size)

        # Layout for this panel
        self.layout = QtWidgets.QVBoxLayout()

        # Create the 4 plot widgets
        self.accel_plot = make_plot(f"{title_prefix} Accelerometer", "m/s²")
        self.gyro_plot = make_plot(f"{title_prefix} Gyroscope", "deg/s")
        self.mag_plot = make_plot(f"{title_prefix} Magnetometer", "µT")
        self.quat_plot = make_plot(f"{title_prefix} Quaternion", "value")

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
    def _update(
        time_buf: NDArray, data_buf: NDArray, timestamp: float, values: tuple
    ) -> None:
        # Shift time left by one
        time_buf[:-1] = time_buf[1:]
        time_buf[-1] = timestamp

        # Shift data left by one
        data_buf[:, :-1] = data_buf[:, 1:]
        data_buf[:, -1] = values

    def update(self, imu) -> None:
        """Update this panel with new IMUData."""
        t = imu.timestamp

        # --- shift time once ---
        self.time_buf[:-1] = self.time_buf[1:]
        self.time_buf[-1] = t

        # --- shift data once per group, but DO NOT shift time again --
        self.accel_buf[:, :-1] = self.accel_buf[:, 1:]
        self.gyro_buf[:, :-1] = self.gyro_buf[:, 1:]
        self.mag_buf[:, :-1] = self.mag_buf[:, 1:]
        self.quat_buf[:, :-1] = self.quat_buf[:, 1:]

        # --- insert new values ---
        self.accel_buf[:, -1] = imu.accel.to_tuple()
        self.gyro_buf[:, -1] = imu.gyro.to_tuple()
        self.mag_buf[:, -1] = imu.mag.to_tuple()
        self.quat_buf[:, -1] = imu.quat.to_tuple()

        # --- update curves ---
        for i in range(3):
            self.accel_curves[i].setData(self.time_buf, self.accel_buf[i])
            self.gyro_curves[i].setData(self.time_buf, self.gyro_buf[i])
            self.mag_curves[i].setData(self.time_buf, self.mag_buf[i])

        for i in range(4):
            self.quat_curves[i].setData(self.time_buf, self.quat_buf[i])
