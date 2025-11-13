"""Sample doc string."""

import numpy as np
import pyqtgraph as pg
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt


class IMUPlotWidget(QtWidgets.QWidget):
    """Plot widget containing accel, gyro, and quaternion plots for one IMU."""

    def __init__(self, title: str, buffer_size: int = 2000):
        super().__init__()

        self.buffer_size = buffer_size

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        title_label = QtWidgets.QLabel(f"<b>{title}</b>")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # create three plot widgets
        self.acc_plot = pg.PlotWidget(title="Accelerometer [m/s²]")
        self.gyr_plot = pg.PlotWidget(title="Gyroscope [deg/s]")
        self.quat_plot = pg.PlotWidget(title="Quaternion")

        layout.addWidget(self.acc_plot)
        layout.addWidget(self.gyr_plot)
        layout.addWidget(self.quat_plot)

        # Allocate buffers (acc:3, gyr:3, quat:4)
        self.acc_data = np.zeros((3, buffer_size))
        self.gyr_data = np.zeros((3, buffer_size))
        self.quat_data = np.zeros((4, buffer_size))

        # Create curve objects
        pens = ["r", "g", "b", "y"]
        self.acc_curves = [self.acc_plot.plot(pen=pens[i]) for i in range(3)]
        self.gyr_curves = [self.gyr_plot.plot(pen=pens[i]) for i in range(3)]
        self.quat_curves = [self.quat_plot.plot(pen=pens[i]) for i in range(4)]

        # y-axis ranges (adjust as needed)
        self.acc_plot.setYRange(-20, 20)
        self.gyr_plot.setYRange(-500, 500)
        self.quat_plot.setYRange(-1.5, 1.5)

    def update(self, accel, gyro, quat):
        """Append new IMU values to the scrolling buffer."""
        ax, ay, az = accel
        gx, gy, gz = gyro
        qw, qx, qy, qz = quat

        # roll buffers
        self.acc_data = np.roll(self.acc_data, -1, axis=1)
        self.gyr_data = np.roll(self.gyr_data, -1, axis=1)
        self.quat_data = np.roll(self.quat_data, -1, axis=1)

        # push new values
        self.acc_data[:, -1] = [ax, ay, az]
        self.gyr_data[:, -1] = [gx, gy, gz]
        self.quat_data[:, -1] = [qw, qx, qy, qz]

        # update curves
        for i in range(3):
            self.acc_curves[i].setData(self.acc_data[i])
            self.gyr_curves[i].setData(self.gyr_data[i])

        for i in range(4):
            self.quat_curves[i].setData(self.quat_data[i])


class IMUOscilloscope(QtWidgets.QWidget):
    """Two-sided oscilloscope for left and right IMU."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("IMU Oscilloscope")
        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        # LEFT + RIGHT IMU widgets
        self.left_imu = IMUPlotWidget("LEFT IMU")
        self.right_imu = IMUPlotWidget("RIGHT IMU")

        layout.addWidget(self.left_imu)
        layout.addWidget(self.right_imu)

        # timer for refreshing
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.redraw)
        self.timer.start(20)  # redraw every 20 ms

        self._dirty = False

    def redraw(self):
        """Only redraw when data changed."""
        if self._dirty:
            self._dirty = False

    # ------------------------
    #   PUBLIC UPDATE METHODS
    # ------------------------

    def update_left(self, accel, gyro, quat):
        """Update the left IMU."""
        self.left_imu.update(accel, gyro, quat)
        self._dirty = True

    def update_right(self, accel, gyro, quat):
        """Update the right IMU."""
        self.right_imu.update(accel, gyro, quat)
        self._dirty = True
