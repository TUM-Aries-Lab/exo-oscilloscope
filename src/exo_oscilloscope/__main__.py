"""Sample doc string."""

import argparse

import numpy as np
from PySide6 import QtCore

from exo_oscilloscope.config.definitions import DEFAULT_LOG_LEVEL, LogLevel
from exo_oscilloscope.plotter import IMUOscilloscope
from exo_oscilloscope.utils import setup_logger


def main(
    log_level: str = DEFAULT_LOG_LEVEL, stderr_level: str = DEFAULT_LOG_LEVEL
) -> None:
    """Run the main pipeline.

    :param log_level: The log level to use.
    :param stderr_level: The std err level to use.
    :return: None
    """
    setup_logger(log_level=log_level, stderr_level=stderr_level)

    osc = IMUOscilloscope()

    # simulate IMU input
    t = 0.0

    def fake_data():
        nonlocal t
        t += 0.02

        # fake sine wave IMU
        s1 = np.sin(5 * t)
        s2 = np.sin(7 * t)
        s3 = np.sin(9 * t)

        accel = [s1 * 9, s2 * 9, s3 * 9]
        gyro = [s2 * 180, s3 * 180, s1 * 180]
        quat = [s1, s2, s3, 0.5]

        # left
        osc.update_left(accel, gyro, quat)

        # right (phase shifted)
        osc.update_right(accel, gyro, quat)

    sim_timer = QtCore.QTimer()
    sim_timer.timeout.connect(fake_data)
    sim_timer.start(20)

    osc.exit()


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser("Run the pipeline.")
    parser.add_argument(
        "--log-level",
        default=DEFAULT_LOG_LEVEL,
        choices=list(LogLevel()),
        help="Set the log level.",
        required=False,
        type=str,
    )
    parser.add_argument(
        "--stderr-level",
        default=DEFAULT_LOG_LEVEL,
        choices=list(LogLevel()),
        help="Set the std err level.",
        required=False,
        type=str,
    )
    args = parser.parse_args()

    main(log_level=args.log_level)
