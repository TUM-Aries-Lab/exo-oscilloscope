"""Test the exo plotter."""

import os

from PySide6.QtCore import QTimer

from exo_oscilloscope.plotter import ExoPlotter

# Run Qt in headless mode (required for CI)
os.environ["QT_QPA_PLATFORM"] = "offscreen"


def test_plotter() -> None:
    """Test the plotter by auto-closing the GUI after starting."""
    # Arrange
    close_millisec = 50

    # Act
    gui = ExoPlotter()
    QTimer.singleShot(close_millisec, gui.close)
    gui.run(update_callback=None)
