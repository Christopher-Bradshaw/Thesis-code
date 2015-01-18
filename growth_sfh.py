#!/usr/bin/env python3

import sys
import helpers.data as data
import helpers.graph as graph
import helpers.helpers as h
import helpers.schechter as hs
import matplotlib.pyplot as plt
import numpy as np
import math
import helpers.z_to_t as z_to_t

#################################### start ####################################
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
  for i in sfh.all_g_type:
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

##################################### end #####################################

#################################### start ####################################
"""
The following functions create plots based off the Weisz "SFH in LGG" data
It lets you plot the relationship between mass and star formation rate at various Z
"""
def sf_m_at_z(z):
  sfh = data.sfh()
  masses = sfh.abs_mass()

  t_step = 1
  index = h.find_nearest(sfh.z_times, z)
  z0 = sfh.z_times[index]
  t0 = z_to_t.t_from_z(z0)
  try:
    z1 = sfh.z_times[index + t_step]
    t1 = z_to_t.t_from_z(z1)
  except IndexError:
    sys.exit('Index error')

  #title = str(z0) + '-' + str(z1)
  # The mass at that Z and the one after
  imp_mass = [[obj[index], obj[index + t_step]] for obj in masses]

  # We now have masses at two Zs. Let's bin it!
  bin_range = range(3, 9)
  bin_maxes, bins = [i for i in bin_range], [[] for i in bin_range]

  for item in imp_mass:
    for i in range(len(bin_maxes)):
      if item[0] < bin_maxes[i]:
        if i == 0:
          print("Lower min bin!")
          sys.exit()
        bins[i].append(item)
        break
    else:
      print("Increase max bin!")
      sys.exit()

  for i in range(len(bins) - 1, -1, -1): # walk backwards through list
    if bins[i] == []:
      title = str(z0) + '-' + str(z1)
      bins.pop(i)
      bin_maxes.pop(i)
      continue

    # Check this
    start = np.mean([10**j[0] for j in bins[i]])
    end = np.mean([10**j[1] for j in bins[i]])
    #bins[i] = end/start # Ratio
    bins[i] = (end - start) / (t0 - t1) # Rate of change

  return(bins, bin_maxes, bin_maxes[1] - bin_maxes[0], [z0, z1], [t0, t1])

def schechter_sf_m_at_z(z0, z1, t0, t1, m0, m1):
  bs = [i/10. for i in range(10*m0, 10*m1)]
  out = bs
  for i in range(len(out)):
    out[i] = (hs.param_dub_schechter(out[i], z1) - hs.param_dub_schechter(out[i], z0)) / (t0 -t1)
  return(out, bs)

def plot_sf_m_at_z():
  z = [3, 2, 1, 0.5, 0.1, 0.001]
  info = {'xlim': [3.0, 9.0], 'ylim': [0, 1600000], 'xlabel': r'$\mathregular{Start \, log(M/M_\odot)}$', 'ylabel': r'$\mathregular{(end \, mass - start \, mass)/\Delta t}}$'}
  gs = graph.setup6(info)

  for i in range(len(z)):
    bins, bin_maxes, bin_step, [z0, z1], [t0, t1]= sf_m_at_z(z[i])
    print(bins, bin_maxes)
    title = str(z0) + '-' + str(z1)
    # Get the schecter numbers
    sch, bm= schechter_sf_m_at_z(z0, z1, t0, t1, bin_maxes[0] - bin_step, bin_maxes[-1])
    # Plot
    graph.line6([bins], bin_maxes, i, gs, info=dict({'title': 'Z = ' + title}, **info))
    graph.line6([sch], bm, i, gs, info=dict({'title': 'Z = ' + title}, **info))
    print(sch)
  plt.show()

##################################### end #####################################
if __name__ == "__main__":
  plot_sf_m_at_z()
  #plot_all()
