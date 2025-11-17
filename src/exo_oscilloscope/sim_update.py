"""Simulator functions for the exosuit oscilloscope."""

import time

import numpy as np
from loguru import logger

from exo_oscilloscope.data_classes import IMUData, MotorData, Quaternion, Vector3

GRAVITY = 9.81


def make_simulated_update(gui, start_time: float):  # pragma: no cover
    """Return an update callback that generates fake IMU data.

    :param gui: The ExoPlotter instance receiving plot updates.
    :param start_time: The start time for time offset calculation.
    :return: A no-argument callback function for the GUI timer.
    """

    def update() -> None:
        logger.trace("Simulating IMU update...")
        t = time.time() - start_time
        imu = IMUData(
            accel=GRAVITY * Vector3(np.sin(t), np.sin(t * 2), np.sin(t * 4)),
            gyro=180 * Vector3(np.cos(t), np.cos(t * 2), np.cos(t * 4)),
            mag=Vector3(np.cos(t), np.cos(t * 2), np.cos(t * 4)),
            quat=Quaternion(np.sin(t + 1), np.sin(t + 2), np.sin(t + 3), np.sin(t + 4)),
            timestamp=t,
        )
        motor = MotorData(
            position=np.sin(t), speed=np.sin(t), torque=np.sin(t), timestamp=t
        )
        gui.plot_left(imu, motor)
        gui.plot_right(imu, motor)

    return update
