#!/usr/bin/python3 -B

"""
Demonstrates the usage of PyPlotter by plotting the number of
confirmed cases and deaths due to the 2020 corona virus, with
quadratic polynomial extrapolation into the future.
"""

import scipy.optimize  # pip install scipy
import numpy as np     # pip install numpy
import matplotlib      # pip install matplotlib + apt install python3-tk
import pyplotter       # local import


N = 11  # predict from this many days of data
P = 60  # predict into this many days from onset


DEATHS = [
    0,
    18,
    26,
    42,
    56,
    81,
    106,
    133,
    171,
    213,
    259,
    305,
    362,
    427,
    494,
    565,
    636
]


CASES = [
    332,
    555,
    653,
    941,
    1438,
    2116,
    2886,
    4690,
    6165,
    8235,
    9926,
    12038,
    14549,
    17491,
    20704,
    24630,
    28353,
    30877
]


YDATA = DEATHS   # select: DEATHS | CASES
TYPE = "deaths"  # select: "deaths" | "cases"


def quadratic(x, a, b, c):
    return a * x**2 + b * x + c


def main():
    # extrapolate from observations
    xdata = np.arange(0, len(YDATA))
    xdata_extrapolated = np.arange(0, P+1)
    ydata = np.array(YDATA)
    popt, _ = scipy.optimize.curve_fit(quadratic, xdata[:N], ydata[:N])
    pstr = f"prediction: ${popt[0]:.0f}x^2 {popt[1]:+.0f}x {popt[2]:+.0f}$"
    # plot observed data points + prediction
    fig = pyplotter.Figure(f"Cumulative {TYPE}")
    fig.axes[0].scatter(xdata[:N], ydata[:N], color="blue", label="training data")
    fig.axes[0].scatter(xdata[N:], ydata[N:], color="red", label="ground truth")
    fig.axes[0].plot(xdata_extrapolated, quadratic(xdata_extrapolated, *popt), color="green", alpha=0.5, label=pstr)
    # prettify the graph with ticks, grids, labels, etc.
    fig.axes[0].xaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(2))
    fig.axes[0].yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(2))
    fig.axes[0].set_xlabel("Days (starting from 2020-01-22)")
    fig.axes[0].grid(which="both")
    fig.axes[0].legend()
    # make visible
    fig.show()


if __name__ == "__main__":
    main()
