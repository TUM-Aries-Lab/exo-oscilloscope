"""Test the exo plotter."""

import os

from PySide6.QtCore import QTimer

from exo_oscilloscope.plotter import ExoPlotter

# Run Qt in headless mode (required for CI)
os.environ["QT_QPA_PLATFORM"] = "offscreen"


def test_plotter() -> None:
    """Test the plotter by auto-closing the GUI after starting."""
    gui = ExoPlotter()

    # Auto-close the app after 50 ms
    QTimer.singleShot(50, gui.close)

    # No update_callback → run once, event loop exits automatically
    gui.run(update_callback=None)

    # If we reach here, test passed (no hangs, no errors)
