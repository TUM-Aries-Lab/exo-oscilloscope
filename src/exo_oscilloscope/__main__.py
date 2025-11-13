"""Sample doc string."""

import argparse
import time

import numpy as np
from loguru import logger

from exo_oscilloscope.config.definitions import DEFAULT_LOG_LEVEL, LogLevel
from exo_oscilloscope.data_classes import IMUData, Quaternion, Vector3
from exo_oscilloscope.plotter import ExoPlotter
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
    logger.info("Starting the exo_oscilloscope pipeline")
    start_time = time.time()

    gui = ExoPlotter()

    def update():
        # fake data
        t = time.time() - start_time
        imu = IMUData(
            accel=Vector3(t * np.sin(t), np.sin(t * 2), np.sin(t * 4)),
            gyro=Vector3(np.cos(t), np.cos(t * 2), np.cos(t * 4)),
            mag=Vector3(np.cos(t), np.cos(t * 2), np.cos(t * 4)),
            quat=Quaternion(0.0, 0.0, 0.0, np.sin(t * 8)),
            timestamp=t,
        )
        gui.plot_left(imu)
        gui.plot_right(imu)

    timer = gui.QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(5)

    gui.run()

    gui.close()


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
