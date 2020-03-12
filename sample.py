#!/usr/bin/python3 -B

"""
Demonstrates the usage of PyPlottr by plotting the number of
confirmed cases and deaths due to the 2020 corona virus, with
quadratic polynomial extrapolation into the future.

Data source: www.worldometers.info
"""

import scipy.optimize  # pip install scipy
import numpy as np     # pip install numpy
import matplotlib      # pip install matplotlib + apt install python3-tk
import pyplottr       # local import


START_DATE = "2020-01-21"
N = 14   # predict from this many days of data
P = 120  # predict this many days from START_DATE

DEATHS = [
    6,
    17,
    18,
    26,
    42,
    56,
    80,
    106,
    132,
    170,
    213,
    259,
    304,
    362,
    426,
    492,
    565,
    638,
    724,
    813,
    910,
    1018,
    1115,
    1383,
    1526,
    1669,
    1775,
    1873,
    2009,
    2126,
    2247,
    2360,
    2460,
    2618,
    2699,
    2763,
    2800,
    2858,
    2923,
    2977,
    3050,
    3117,
    3202,
    3285,
    3387,
    3494,
    3599,
    3827,
    4025,
    4296,  # Mar 10
    4628,
    4981,
    5428,
    5833,
    6520,
    7162,
    7979,  # Mar 17
    8951,
    10030,
    11386,
    13011,
    14640,
    16513,
    18894,  # Mar 24
    21282,
    24073,
    27343,
    30861,
    34065,
    37788,  # Mar 30
]


CASES = [
    332,
    580,
    845,
    1317,
    2015,
    2800,
    4581,
    6058,
    7813,
    9823,
    11950,
    14553,  # Feb 01
    17391,
    20630,
    24545,
    28266,
    31439,
    34876,
    37552,  # Feb 08
    40553,
    43099,
    45134,
    59287,  # Feb 12 (spike in statistics)
    64438,
    67100,
    69197,  # Feb 15
    71329,
    73332,
    75184,
    75700,
    76677,
    77673,
    78651,  # Feb 22
    79205,
    80087,
    80828,
    81820,
    83112,
    84615,
    86604,  # Feb 29
    88585,
    90443,
    93016,
    95314,
    98425,
    102050,
    106099,  # Mar 07
    109991,
    114381,
    118948,
    126214,  # Mar 11
    134576,
    145483,
    156653,
    169577,
    182490,
    198234,  # Mar 17
    218744,
    244902,
    275550,
    304979,
    337459,
    378830,
    422574,  # Mar 24
    471035,
    531865,
    596366,
    663127,
    723390,
    784794,  # Mar 30
]


def quadratic(x, a, b, c):
    return a * x**2 + b * x + c


def main():
    fig = pyplottr.Figure(f"Cumulative cases and deaths", ncols=2)
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
        fig.axes[i].set_xlabel(f"Days (starting from {START_DATE})")
        fig.axes[i].ticklabel_format(axis="y", style="scientific", scilimits=(3, 3))
        fig.axes[i].grid(which="both")
        fig.axes[i].set_title(f"{title} (thousands)")
        fig.axes[i].legend()
    fig.resize(1024, 768)
    fig.show()


if __name__ == "__main__":
    main()
