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


N = 14  # predict from this many days of data
P = 60  # predict this many days from onset


DEATHS = [
    6,
    17,
    18,
    26,
    42,
    56,
    81,
    131,
    133,
    171,
    213,
    259,
    305,
    362,
    427,
    494,
    565,
    638,
    725,
    814,
    910,
    1018,
    1117,
    1368,
]


CASES = [
    332,
    555,
    653,
    941,
    1438,
    2118,
    2886,
    5578,
    6165,
    8235,
    9925,
    12038,
    14549,
    17491,
    20680,
    24630,
    28344,
    31532,
    34963,
    37592,
    40574,
    43141,
    45206,
    60328,
]


def quadratic(x, a, b, c):
    return a * x**2 + b * x + c


def main():
    fig = pyplotter.Figure(f"Cumulative cases and deaths", ncols=2)
    for i, (title, ydata) in enumerate(zip(["Cases", "Deaths"], [CASES, DEATHS])):
        # extrapolate with a second-degree polynomial
        xdata = np.arange(0, len(ydata))
        xdata_extrapolated = np.arange(0, P+1)
        popt, _ = scipy.optimize.curve_fit(quadratic, xdata[:N], ydata[:N])
        pstr = f"prediction: ${popt[0]:.0f}x^2 {popt[1]:+.0f}x {popt[2]:+.0f}$"
        # plot the observed data points + prediction curve
        fig.axes[i].scatter(xdata[:N], ydata[:N], color="blue", label=f"training data, N={N}")
        fig.axes[i].scatter(xdata[N:], ydata[N:], color="red", label=f"ground truth, N={len(ydata) - N}")
        fig.axes[i].plot(xdata_extrapolated, quadratic(xdata_extrapolated, *popt), color="green", alpha=0.5, label=pstr)
        # prettify the graph with ticks, grids, labels, etc.
        fig.axes[i].xaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(4))
        fig.axes[i].yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(4))
        fig.axes[i].set_xlabel("Days (starting from 2020-01-21)")
        fig.axes[i].ticklabel_format(axis="y", style="scientific", scilimits=(3, 3))
        fig.axes[i].grid(which="both")
        fig.axes[i].set_title(f"{title} (thousands)")
        fig.axes[i].legend()
    fig.show()


if __name__ == "__main__":
    main()
