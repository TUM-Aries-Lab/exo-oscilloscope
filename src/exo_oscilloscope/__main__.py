"""Sample doc string."""

import argparse
import time

from loguru import logger

from exo_oscilloscope.config.definitions import DEFAULT_LOG_LEVEL, LogLevel
from exo_oscilloscope.plotter import ExoPlotter
from exo_oscilloscope.sim_update import make_simulated_update
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

    gui = ExoPlotter()

    try:
        start_time = time.time()
        update_callback = make_simulated_update(gui=gui, start_time=start_time)
        gui.run(update_callback=update_callback)
    except Exception as err:
        logger.error(f"{err}.")
    finally:
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

    main(log_level=args.log_level, stderr_level=args.stderr_level)
