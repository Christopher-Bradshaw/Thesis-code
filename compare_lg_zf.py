#!/usr/bin/env python3

import sys
import copy
import helpers.data as data
import helpers.graph as graph
import helpers.helpers as h
import helpers.weisz as wh
import helpers.whitaker as h_whit
import helpers.schechter as hs
import matplotlib.pyplot as plt
import numpy as np
import math

# Weisz
def sf_m_at_z(bin_maxes, index, t_step):
  sfh = data.sfh()
  masses, masses_unc = sfh.abs_mass()
  g_loc = sfh.get_loc()

  z0, t0, z1, t1 = h.z_and_t_from_index_t_step(index, t_step, sfh.z_times)
  gal_mass =     [[galaxy[index], galaxy[index + t_step]] for galaxy in masses]
  gal_mass_unc = [[galaxy[index], galaxy[index + t_step]] for galaxy in masses_unc]

  # Bin each gal, throw error if not binned or smaller than first bin
  orig_bins, orig_bins_unc = [[[] for i in bin_maxes] for j in range(2)]
  for j, gal in enumerate(gal_mass): # for each galaxy
    for i in range(len(bin_maxes)): # scan through bins. Bin and break when appropriate
      if math.log10(gal[0]) < bin_maxes[i]:
        orig_bins[i].append([gal, g_loc[j]])
        orig_bins_unc[i].append([gal_mass_unc[j], g_loc[j]])
        break
    else:
      raise Exception("Check max bin sizing")
  if orig_bins[0]:
    raise Exception("Check min bin sizing")
  orig_bins, orig_bins_unc = orig_bins[1:], orig_bins_unc[1:]

  bins, bins_unc, bins_center, bins_center_unc = [[] for i in range(4)]
  for i in range(len(orig_bins)):
    g_actual = wh.g_actual_bins(orig_bins[i])
    bins.append(wh.average_growth_rate(sfh.g_exp, g_actual, orig_bins[i], t0, t1))
    bins_unc.append(wh.bin_uncertainty(sfh.g_exp, g_actual, orig_bins_unc[i], t0, t1))
    bins_center.append(wh.average_bin_start(sfh.g_exp, g_actual, orig_bins[i]))
    bins_center_unc.append(wh.uncertainty_bin_start(sfh.g_exp, g_actual, orig_bins_unc[i], bins_center[-1]))

  return(bins, bins_unc, bins_center, bins_center_unc)

# We want to see how much a galaxy that starts at mass x at z0 grows by z1
def schechter_sf_m_at_z(bins_center, index, t_step):
  print(bins_center, index, t_step)
  ### OLD
  sfh = data.sfh()
  z0, t0, z1, t1 = h.z_and_t_from_index_t_step(index, t_step, sfh.z_times)
  o_bins = []
  for m in bins_center:
    m3 = hs.growth_over_time(m, z0, z1)
    o_bins.append( ((10 ** m3) - (10 ** m)) / (t0 - t1))

  print(o_bins)
  return(o_bins)
  # Need to do this differently.
  # Determine the number density of m at z0 (1)
  # Generate an SMF at z1, correct for mergers (2)
  # Look through z1 SMF to find number density closest to number density of m0 (m1)
  ### NEW
  sfh = data.sfh()
  z0, t0, z1, t1 = h.z_and_t_from_index_t_step(index, t_step, sfh.z_times)
  bins = []
  for m in bins_center:
    # (1)
    target = hs.param_dub_schechter(m, z0) # This is the number density that we want
    # (2)
    step, SMF = 10, []
    test_masses = [i/step for i in range(int(3*step), int(12*step))]
    for i in test_masses:
      SMF.append(hs.param_dub_schechter(i, z1))

    # (3)
    old_SMF = copy.copy(SMF)

    for i in range(len(test_masses)):
      res = hs.integrated_merger_corr(test_masses[i], z0, z1)
      d_nd = sum([i[1] for i in res]) # delta number density
      ### Additive correction
      for j in res:
        parents = [math.log10(10**test_masses[i] / (j[0] + 1)), math.log10(10**test_masses[i] * j[0]/(j[0] + 1))]
        for k in parents:
          for l in range(len(test_masses)):
            if k > test_masses[l] > (k-1/step): # fixes silly spike at the beginning
              SMF[l] += j[1]
              break
      ### Negative correction
      SMF[i] -= d_nd

    graph.line([old_SMF, SMF], x=test_masses)
    # (4)
    for i in range(len(test_masses)):
      if SMF[i] < target:
        m1 = test_masses[i]
        break
    bins.append( ((10 ** m1) - (10 ** m)) / (t0 - t1))
    print(bins)
  ###
  return(bins)

# This is the third option - sfr data. NB: z0 > z1
def sfr_data(ext_bins_center, z0, z1):
  a_low, a_high, b = h_whit.weight_parameters(z0, z1)
  m_star = 10.2
  bins = [10**(a_low * (mass - 10.2) + b) * 0.64e9 for mass in ext_bins_center]
  return(bins)

def plot_sf_m_at_z():
  z = [3, 2, 1, 0.5, 0.1, 0.01]
  info = {'xlim': [3.0, 9.0], 'ylim': [10, 100000000], 'ylog': True, 'xlabel6': r'$\mathregular{Start Mass \, log(M/M_\odot)}$', 'ylabel6': r'$\mathregular{\Delta M/\Delta t} \, M_\odot / Gyr$', 'legend6': ['Star Formation History', 'Parameterized Schechter Predictions']}
  params = {'marker': ['x', 'None', 'None'], 'linestyle': ['None', '-', '-']}
  gs = graph.setup6(info)

  bin_maxes = [i for i in range(3, 9)]
  bin_step = bin_maxes[1] - bin_maxes[0]
  t_step_list = [1,1,1,3,5,15] # Time step
  sfh = data.sfh()
  for i in range(len(z)):
    t_step = t_step_list[i] # Compensates for dense observations at later times
    # work out the start indicies
    index = h.find_nearest(sfh.z_times, z[i])
    z0, t0, z1, t1 = h.z_and_t_from_index_t_step(index, t_step, sfh.z_times)
    title = str(round(z0, 3)) + '-' + str(round(z1, 4))

    # Get the growth vs mass data (at this z) from the SFH
    bins, bins_unc, bins_center, bins_center_unc = sf_m_at_z(bin_maxes, index, t_step)
    ext_bins_center = [3] + bins_center + [8]
    s_bins = schechter_sf_m_at_z(ext_bins_center, index, t_step)
    sanity_bins = sfr_data(ext_bins_center, z0, z1)

    # Plot these two things
    # Shows that I can interpolate...
    #if z1 > 0.5:
    #  graph.line6([bins, s_bins, sanity_bins, sanity_bins1, sanity_bins2], [bins_center, ext_bins_center, ext_bins_center, ext_bins_center, ext_bins_center], i, gs, info=dict({'title6': 'Z = ' + title}, **info), params=dict({'yerr': [0], 'yerr_vals': bins_unc, 'xerr': [0], 'xerr_vals': bins_center_unc}, **params))
    if z1 > 0.5:
      graph.line6([bins, s_bins, sanity_bins], [bins_center, ext_bins_center, ext_bins_center], i, gs, info=dict({'title6': 'Z = ' + title}, **info), params=dict({'yerr': [0], 'yerr_vals': bins_unc, 'xerr': [0], 'xerr_vals': bins_center_unc}, **params))
    else:
      graph.line6([bins, s_bins], [bins_center, ext_bins_center], i, gs, info=dict({'title6': 'Z = ' + title}, **info), params=dict({'yerr': [0], 'yerr_vals': bins_unc, 'xerr': [0], 'xerr_vals': bins_center_unc}, **params))
    plt.show()
  plt.show()

if __name__ == "__main__":
  if sys.version[0] != '3':
    sys.exit()
  plot_sf_m_at_z()
