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


"""
Remembering that the sfh masses are in a list [m_at_t_0, m_at_t_2 ... ]
Given index, and step finds rate of increase between m_at_t_index and m_at_t_(index + t_step)
Requires also the max values for each bin

So we have a list of masses: imp_mass = [ [start_1, end_1], [start_2, end_2], ... , [start_n, end_n]]
And a list of uncertainties: imp_mass_unc = [ [[start_+_1, start_-_1], [end_+_1, end_-_1]] ... ]  

These are binned by start mass. uncertainties should be binned in same way.

Each bin then calculates the average start and end mass and therefore the delta mass


"""
def sf_m_at_z(bin_maxes, index, t_step):
  sfh = data.sfh()
  masses, masses_unc = sfh.abs_mass()

  z0, t0, z1, t1 = z_and_t_from_index_t_step(index, t_step, sfh)
  imp_mass = [[galaxy[index], galaxy[index + t_step]] for galaxy in masses]
  imp_mass_unc = [[galaxy[index], galaxy[index + t_step]] for galaxy in masses_unc]

  # Bin each item, throw error if not binned or smaller than first bin
  bins, bins_unc = [[] for i in bin_maxes], [[] for i in bin_maxes]
  for j, item in enumerate(imp_mass): # for each galaxy
    for i in range(len(bin_maxes)): # scan through bins. Bin and break when appropriate
      if item[0] < bin_maxes[i]:
        if i == 0:
          print("Lower min bin!")
          sys.exit()
        bins[i].append(item)
        bins_unc[i].append(imp_mass_unc[j])
        break
    else:
      print("Increase max bin!")
      sys.exit()

  for i in range(len(bins)):
    # Make each bin the rate of change of mass in that bin
    start = np.mean([10**j[0] for j in bins[i]]) if len(bins[i]) else 0
    end = np.mean([10**j[1] for j in bins[i]]) if len(bins[i]) else 0
    bins[i] = (end - start) / (t0 - t1)
    # Make each bins_unc the uncertainty in that bin
    if len(bins_unc[i]) == 0:
      start_pos_unc, start_neg_unc, end_pos_unc, end_neg_unc = 0, 0, 0, 0
    else:
      start_pos_unc = math.sqrt(sum([(10**j[0][0])**2 for j in bins_unc[i]]))/len(bins_unc[i])
      start_neg_unc = math.sqrt(sum([(10**j[0][1])**2 for j in bins_unc[i]]))/len(bins_unc[i])
      end_pos_unc =   math.sqrt(sum([(10**j[1][0])**2 for j in bins_unc[i]]))/len(bins_unc[i])
      end_neg_unc =   math.sqrt(sum([(10**j[1][1])**2 for j in bins_unc[i]]))/len(bins_unc[i])

    diff_pos_unc = math.sqrt(start_pos_unc ** 2 + end_pos_unc ** 2)
    diff_neg_unc = math.sqrt(start_neg_unc ** 2 + end_neg_unc ** 2)

    bins_unc[i] = [diff_pos_unc/(t0-t1), diff_neg_unc/(t0-t1)]
  return(bins, bins_unc)

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
  z = [3, 2, 1, 0.5, 0.1, 0.01]
  info = {'xlim': [3.0, 9.0], 'ylim': [10, 100000000], 'ylog': True, 'xlabel6': r'$\mathregular{Start Mass \, log(M/M_\odot)}$', 'ylabel6': r'$\mathregular{\Delta M/\Delta t} \, M_\odot / Gyr$', 'legend6': ['Star Formation History', 'Parameterized Schechter Predictions']}
  params = {'marker': ['x', 'None'], 'linestyle': ['None', '-']}
  gs = graph.setup6(info)

  bin_maxes = [i for i in range(3, 9)]
  bin_step = bin_maxes[1] - bin_maxes[0]
  t_step_list = [1,1,1,3,5,15] # Time step
  sfh = data.sfh()
  for i in range(len(z)):
    # Setup
    t_step = t_step_list[i] # Compensates for dense observations at later times
    index = h.find_nearest(sfh.z_times, z[i])
    z0, t0, z1, t1 = z_and_t_from_index_t_step(index, t_step, sfh)
    title = str(round(z0, 3)) + '-' + str(round(z1, 4))

    # Get the growth vs mass data (at this z) from the SFH
    bins, bins_unc = sf_m_at_z(bin_maxes, index, t_step)
    s_bins = schechter_sf_m_at_z(bin_maxes, bin_step, index, t_step)

    # Plot these two things
    graph.line6([bins, s_bins], bin_maxes, i, gs, info=dict({'title6': 'Z = ' + title}, **info), params=dict({'yerr': [0], 'yerr_vals': bins_unc}, **params))
    #break
  plt.show()

if __name__ == "__main__":
  plot_sf_m_at_z()
