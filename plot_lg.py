#!/usr/bin/env python3

import helpers.data as data
import helpers.graph as graph
import matplotlib.pyplot as plt
import numpy as np
"""
The following functions create plots based of the raw star formation history data
This data was pulled from the Weisz "Star formation history of LG galaxies" paper
"""
def plot_by_type(sfh, typ, info={}):
  to_plot = []
  for i in range(len(sfh.names)):
    if sfh.g_type[i] == typ:
      to_plot.append(sfh.mass[i])
  af1 = graph.line(to_plot, [10**i for i in sfh.legend], dict({'title': typ}, **info))
  graph.line([add_median(to_plot)], [10**i for i in sfh.legend], params={'linewidth': 4}, af1=af1)


def add_median(plotted):
  m = []
  for i in range(len(plotted[0])):
    m.append(np.median([p[i] for p in plotted]))
  return(m)

def plot_all():
  sfh = data.sfh()
  info = {'xlabel': r'$Lookback Time (Gyr)$', 'ylabel': r'$Cumulative SFH$', 'ylim': [0, 1], 'xlim': [10**sfh.legend[-1], 10**sfh.legend[0]], 'invert_xaxis': True}
  for i in set(sfh.g_type):
    plot_by_type(sfh, i, info)
  plt.show()

def average_sfh():
  masses = data.sfh().mass
  out = []
  for i in range(len(masses[0])):
    tmp = 0
    for galaxy in masses:
      tmp += galaxy[i]
    out.append(tmp / len(masses))
  return(out)

if __name__ == "__main__":
  plot_all()
