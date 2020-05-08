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
N = 70   # predict from this many days of data
P = 110  # predict this many days from START_DATE

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
    3493,
    3598,
    3826,
    4023,
    4297,  # Mar 10
    4627,
    4980,
    5427,
    5841,
    6532,
    7180,
    8000,  # Mar 17
    8983,
    10077,
    11457,
    13101,
    14739,
    16671,
    19157,  # Mar 24
    21746,
    24691,
    28160,
    31831,
    35714,
    39334,  # Mar 30
    44043,
    49233,
    55503,
    61465,
    67531,
    72535,
    78141,  # Apr 6
    86033,
    92768,
    100434,
    107781,
    113989,
    119554,
    125193,  # Apr 13
    132601,
    140791,
    147789,
    156218,
    162894,
    167788,
    173277,  # Apr 20
    180561,
    187259,
    193964,
    200381,
    206482,
    210239,
    214748,  # Apr 27
    221436,
    228029,
    233824,
    239447,
    244644,
    248144,
    252240,  # May 4
    258026,
    264837,
    270426,  # May 7
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
    return np.clip(a * x**2 + b * x + c, 0, 5e6)


def cubic(x, a, b, c, d):
    return np.clip(a * x**3 + b * x**2 + c * x + d, 0, 5e6)


def main():
    fig = pyplottr.Figure(f"Cumulative cases and deaths", ncols=2)
    for i, (title, ydata) in enumerate(zip(["Cases", "Deaths"], [CASES, DEATHS])):
        # extrapolate with second-degree & third-degree polynomials
        xdata = np.arange(0, len(ydata))
        xdata_extrapolated = np.arange(0, P+1)
        pquad, _ = scipy.optimize.curve_fit(quadratic, xdata[:N], ydata[:N])
        pstr_quad = f"prediction: ${pquad[0]:.1f}x^2 {pquad[1]:+.1f}x {pquad[2]:+.0f}$"
        pcubic, _ = scipy.optimize.curve_fit(cubic, xdata[:N], ydata[:N])
        pstr_cubic = f"prediction: ${pcubic[0]:.2f}x^3 {pcubic[1]:+.1f}x^2 {pcubic[2]:+.0f}x {pcubic[3]:+.0f}$"
        # plot the observed data points + prediction curve
        fig.axes[i].scatter(xdata[:N], ydata[:N], color="blue", label=f"training data, N={N}")
        fig.axes[i].scatter(xdata[N:], ydata[N:], color="red", label=f"ground truth, N={len(ydata)}")
        fig.axes[i].plot(xdata_extrapolated, quadratic(xdata_extrapolated, *pquad), color="green", alpha=0.5, label=pstr_quad)
        fig.axes[i].plot(xdata_extrapolated, cubic(xdata_extrapolated, *pcubic), color="blue", alpha=0.5, label=pstr_cubic)
        # prettify the graph with ticks, grids, labels, etc.
        fig.axes[i].xaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(4))
        fig.axes[i].yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(4))
        fig.axes[i].set_xlabel(f"Days (starting from {START_DATE})")
        fig.axes[i].ticklabel_format(axis="y", style="scientific", scilimits=(3, 3))
        fig.axes[i].grid(which="both")
        fig.axes[i].set_title(f"{title} (thousands)")
        fig.axes[i].set_ylim(0, np.ceil(np.max(ydata) / 1e5) * 1e5)
        fig.axes[i].legend()
    fig.resize(1024, 768)
    fig.show()


if __name__ == "__main__":
    main()
