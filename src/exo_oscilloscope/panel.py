"""Sample doc string."""

import numpy as np
import pyqtgraph as pg
from PySide6 import QtWidgets

from exo_oscilloscope.config.definitions import BUFFER_SIZE, PENS

AXES = ["x", "y", "z"]
QUAT_AXES = ["x", "y", "z", "w"]


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

    def __init__(self, title_prefix: str) -> None:
        """Initialize the panel.

        :param title_prefix: prefix for title
        """
        self.buffer_size = BUFFER_SIZE
        self.pens = PENS

        # Buffers
        self.accel_buf = np.zeros((3, self.buffer_size))
        self.gyro_buf = np.zeros((3, self.buffer_size))
        self.mag_buf = np.zeros((3, self.buffer_size))
        self.quat_buf = np.zeros((4, self.buffer_size))
        self.time_buf = np.zeros(self.buffer_size)

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
            self.accel_plot.plot(pen=self.pens[i], name=f"accel_{ax}")
            for i, ax in enumerate(AXES)
        ]
        self.gyro_curves = [
            self.gyro_plot.plot(pen=self.pens[i], name=f"gyro_{ax}")
            for i, ax in enumerate(AXES)
        ]
        self.mag_curves = [
            self.mag_plot.plot(pen=self.pens[i], name=f"mag_{ax}")
            for i, ax in enumerate(AXES)
        ]
        self.quat_curves = [
            self.quat_plot.plot(pen=self.pens[i], name=f"quat_{ax}")
            for i, ax in enumerate(QUAT_AXES)
        ]

    def update(self, imu) -> None:
        """Update this panel with new IMUData.

        :param imu: IMUData to update
        :return: None
        """
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
