"""Sample doc string."""

import pyqtgraph as pg


def make_plot(title: str, y_label: str) -> pg.PlotWidget:
    """Make a plot with given title and Y-axis label."""
    plot = pg.PlotWidget(title=title)
    plot.showGrid(x=True, y=True, alpha=0.3)
    plot.addLegend()
    plot.setBackground("w")

    plot.setLabel("left", y_label)
    plot.setLabel("bottom", "Time (s)")

    return plot
