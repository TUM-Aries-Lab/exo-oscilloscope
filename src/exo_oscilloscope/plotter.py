"""Sample doc string."""

import pyqtgraph as pg
from PySide6 import QtCore, QtWidgets


class ExoPlotter:
    """Main application class for the exoskeleton plotting UI."""

    def __init__(self) -> None:
        # Store references so the rest of the class can use them
        self.QtWidgets = QtWidgets
        self.QtCore = QtCore
        self.pg = pg

        # Initialize the Qt application
        self.app = QtWidgets.QApplication([])

        # Root window
        self.window = QtWidgets.QWidget()
        self.window.setWindowTitle("ExoPlotter")

        # Layout
        self.layout = QtWidgets.QVBoxLayout()
        self.window.setLayout(self.layout)

    def run(self) -> None:
        """Run the Qt event loop."""
        self.window.show()
        self.app.exec()
