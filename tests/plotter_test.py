"""Test the exo plotter."""

import os
import time

from loguru import logger
from PySide6.QtCore import QTimer

from exo_oscilloscope.plotter import ExoPlotter
from exo_oscilloscope.sim_update import make_simulated_update

# Run Qt in headless mode (required for CI)
os.environ["QT_QPA_PLATFORM"] = "offscreen"


def test_plotter() -> None:
    """Test the plotter by auto-closing the GUI after starting."""
    # Arrange
    close_millisec = 100

    # Act
    gui = ExoPlotter()

    try:
        start_time = time.time()
        update_callback = make_simulated_update(gui=gui, start_time=start_time)
        QTimer.singleShot(close_millisec, gui.close)
        gui.run(update_callback=update_callback)
    except Exception as err:
        logger.error(f"{err}.")
    finally:
        gui.close()
