#!/usr/bin/env python3

import sys
import copy
import helpers.data as data
import helpers.graph as graph
import helpers.helpers as h
wh = h.weisz_helpers(True)
import helpers.schechter as hs
import matplotlib.pyplot as plt
import numpy as np
import math
import mass_const_num_den as mcnd

# Weisz
def sf_m_at_z(bin_maxes, index, t_step):
  sfh = data.sfh()
  masses, masses_unc = sfh.abs_mass()
  g_loc = sfh.get_loc()

  z0, t0, z1, t1 = h.z_and_t_from_index_t_step(index, t_step, sfh)
  gal_mass = [[galaxy[index], galaxy[index + t_step]] for galaxy in masses]
  gal_mass_unc = [[galaxy[index], galaxy[index + t_step]] for galaxy in masses_unc]

  # Bin each gal, throw error if not binned or smaller than first bin
  orig_bins, orig_bins_unc = [[[] for i in bin_maxes] for j in range(2)]
  for j, gal in enumerate(gal_mass): # for each galaxy
    for i in range(len(bin_maxes)): # scan through bins. Bin and break when appropriate
      if math.log10(gal[0]) < bin_maxes[i]:
        if i == 0:
          print("Lower min bin!")
          sys.exit()
        orig_bins[i].append([gal, g_loc[j]])
        orig_bins_unc[i].append([gal_mass_unc[j], g_loc[j]])
        break
    else:
      print("Increase max bin!")
      sys.exit()

  bins, bins_unc, bins_center, bins_center_unc = [[] for i in range(4)]
  # Ignore first bin - should always be empty
  for i in range(1, len(orig_bins)):
    # Make each bin the rate of change of mass in that bin
    bins.append(wh.average_growth_rate(sfh, orig_bins[i][:], t0, t1))
    # Make each bins_unc the uncertainty in that bin (assuming we are summing the things)
    bins_unc.append(wh.bin_uncertainty(sfh, orig_bins_unc[i][:], t0, t1))
    # Calc the avg start mass for each bin **LOG10**
    bins_center.append(wh.average_bin_start(sfh, orig_bins[i][:]))
    # Calc the uncertainty on this avg start mass
    bins_center_unc.append(wh.uncertainty_bin_start(sfh, orig_bins_unc[i][:], bins_center[-1]))

  return(bins, bins_unc, bins_center, bins_center_unc)

# We want to see how much a galaxy that starts at mass x at z0 grows by z1
def schechter_sf_m_at_z(bins_center, index, t_step):
  print(bins_center, index, t_step)
  ### OLD
  sfh = data.sfh()
  z0, t0, z1, t1 = h.z_and_t_from_index_t_step(index, t_step, sfh)
  o_bins = []
  for m in bins_center:
    m3 = mcnd.growth_over_time(m, z0, z1)
    o_bins.append( ((10 ** m3) - (10 ** m)) / (t0 - t1))

  print(o_bins)
  # Need to do this differently.
  # Determine the number density of m at z0 (1)
  # Generate an SMF at z1, correct for mergers (2)
  # Look through z1 SMF to find number density closest to number density of m0 (m1)
  ### NEW
  sfh = data.sfh()
  z0, t0, z1, t1 = h.z_and_t_from_index_t_step(index, t_step, sfh)
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

# This is the third option - sfr data
# The way we are doing this is fine for a sanity check but not really that nice.
# There are lots of issues with choosing values.
def sfr_data(ext_bins_center, z0, z1):
  # This is the raw data
  """
  sfr = data.sfr().data[0]
  sfr_x = [i[0] for i in sfr]
  sfr_y = [0.64e9*10**i[1] for i in sfr] # M sun per year
  """
  if 0.0 < z0 < 1.0: # NOT RIGHT - data is for > 0.5
    a_low0, a_high0, b0  = 0.94, 0.14, 1.11
    weight0 = z0
  elif 1.0 < z0 < 1.5:
    a_low0, a_high0, b0  = 0.99, 0.51, 1.31
    weight0 = z0 - 1.0
  elif 1.5 < z0 < 2.0:
    a_low0, a_high0, b0  = 1.04, 0.62, 1.49
    weight0 = z0 - 1.5
  else:
    #elif 2.0 < z0 < 3.0: # ALSO NOT RIGHT - only up to 2.5
    a_low0, a_high0, b0  = 0.91, 0.67, 1.62
    weight0 = z0 - 2.0

  if 0.0 < z1 < 1.0: # NOT RIGHT - data is for > 0.5
    a_low1, a_high1, b1  = 0.94, 0.14, 1.11
    weight1 = 1 - z1
  elif 1.0 < z1 < 1.5:
    a_low1, a_high1, b1  = 0.99, 0.51, 1.31
    weight1 = 1.5 - z1
  elif 1.5 < z1 < 2.0:
    a_low1, a_high1, b1  = 1.04, 0.62, 1.49
    weight1 = 2 - z1
  else:
    #elif 2.0 < z1 < 3.0: # ALSO NOT RIGHT - only up to 2.5
    a_low1, a_high1, b1  = 0.91, 0.67, 1.62
    weight1 = 3 - z1

  # Rounding needed for assertions
  a_low, a_high, b = [round((i[0] * weight0 + i[1] * weight1) / (weight0 + weight1), 3) for i in [[a_low0, a_low1], [a_high0, a_high1], [b0, b1]]]
  assert ((a_low < a_low1) and (a_low > a_low0)) or ((a_low < a_low0) and (a_low > a_low1)) or (a_low == a_low0 == a_low1)
  assert ((a_high < a_high1) and (a_high > a_high0)) or ((a_high < a_high0) and (a_high > a_high1)) or (a_high == a_high0 == a_high1)
  assert ((b < b1) and (b > b0)) or ((b < b0) and (b > b1)) or (b == b0 == b1)

  m_star = 10.2
  bins = []

  for mass in ext_bins_center:
    bins.append(10**(a_low * (mass - 10.2) + b) * 0.64e9)
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
    z0, t0, z1, t1 = h.z_and_t_from_index_t_step(index, t_step, sfh)
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
