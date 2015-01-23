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
import copy
import mass_const_num_den as mcnd

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

##################################### end #####################################

#################################### start ####################################
"""
Remembering that the sfh masses are in a list [m_at_t_0, m_at_t_2 ... ]
Given index, and step finds rate of increase between m_at_t_index and m_at_t_(index + t_step)
Requires also the max values for each bin
"""
def sf_m_at_z(bin_maxes, index, t_step):
  sfh = data.sfh()
  masses = sfh.abs_mass()
  masses_unc = sfh.abs_mass_unc()

  z0, t0, z1, t1 = z_and_t_from_index_t_step(index, t_step, sfh)
  imp_mass = [[galaxy[index], galaxy[index + t_step]] for galaxy in masses]

  # Bin each item, throw error if not binned or smaller than first bin
  bins = [[] for i in bin_maxes]
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

  for i in range(len(bins)):
    start = np.mean([10**j[0] for j in bins[i]]) if len(bins[i]) else 0
    end = np.mean([10**j[1] for j in bins[i]]) if len(bins[i]) else 0
    bins[i] = (end - start) / (t0 - t1)
  return(bins)

# Given an index, returns the z value and the t value that that z corresponds to (wrt sfh)
def z_and_t_from_index_t_step(index, t_step, sfh):
  z0 = sfh.z_times[index]
  t0 = z_to_t.t_from_z(z0)
  try:
    z1 = sfh.z_times[index + t_step]
    t1 = z_to_t.t_from_z(z1)
  except IndexError:
    sys.exit('Index error')
  return(z0, t0, z1, t1)

# We want to see how much a galaxy that starts at mass x at z0 grows by z1
def schechter_sf_m_at_z(bin_maxes, bin_step, index, t_step):
  sfh = data.sfh()
  z0, t0, z1, t1 = z_and_t_from_index_t_step(index, t_step, sfh)
  bins = []
  for i in bin_maxes:
    m = i - bin_step/2
    m1 = mcnd.growth_over_time(m, z0, z1)
    bins.append( ((10 ** m1) - (10 ** m)) / (t0 - t1))
  return(bins)

def plot_sf_m_at_z():
  z = [3, 2, 1, 0.5, 0.1, 0.001]
  info = {'xlim': [3.0, 9.0], 'ylim': [10, 100000000], 'ylog': True, 'xlabel6': r'$\mathregular{Start \, log(M/M_\odot)}$', 'ylabel6': r'$\mathregular{(end \, mass - start \, mass)/\Delta t} (M_sun per Billion years)$', 'legend6': ['Star Formation History', 'Parameterized Schechter Predictions']}
  params = {'marker': ['x', 'None'], 'linestyle': ['None', '-']}
  gs = graph.setup6(info)

  bin_maxes = [i for i in range(3, 9)]
  bin_step = bin_maxes[1] - bin_maxes[0]
  t_step_list = [1,1,1,2,3,5] # Time step
  sfh = data.sfh()
  for i in range(len(z)):
    # Setup
    t_step = t_step_list[i] # Compensates for dense observations at later times
    index = h.find_nearest(sfh.z_times, z[i])
    z0, t0, z1, t1 = z_and_t_from_index_t_step(index, t_step, sfh)
    title = str(z0) + '-' + str(z1)

    # Get the growth vs mass data (at this z) from the SFH
    bins = sf_m_at_z(bin_maxes, index, t_step)
    s_bins = schechter_sf_m_at_z(bin_maxes, bin_step, index, t_step)

    # Plot these two things
    graph.line6([bins, s_bins], bin_maxes, i, gs, info=dict({'title6': 'Z = ' + title}, **info), params=params)
  plt.show()

##################################### end #####################################
if __name__ == "__main__":
  plot_sf_m_at_z()
  #plot_all()
