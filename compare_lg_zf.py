#!/usr/bin/env python3

import sys
from multiprocessing import Pool
import helpers.data as data
import helpers.graph as graph
import helpers.helpers as h
import helpers.weisz as wh
import helpers.whitaker as h_whit
import helpers.schechter as hs
import helpers.merger_correction as hmc
import helpers.z_to_t as z_to_t
import matplotlib.pyplot as plt
import numpy as np
import math

# Weisz
def sf_m_at_z(bin_maxes, index, t_step):
  locs = ['A', 'L', 'G'] #ALG or a subset
  if locs != ['A', 'L', 'G']:
    print('WARNING, only using {}'.format(locs))
  sfh = data.sfh()
  masses, masses_unc = sfh.abs_mass()
  g_loc = sfh.get_loc()

  z0, t0, z1, t1 = h.z_and_t_from_index_t_step(index, t_step, sfh.z_times)
  gal_mass =     [[galaxy[index], galaxy[index + t_step]] for galaxy in masses]
  gal_mass_unc = [[galaxy[index], galaxy[index + t_step]] for galaxy in masses_unc]
  print(z0)

  # Bin each gal, throw error if not binned or smaller than first bin
  orig_bins, orig_bins_unc = [[[] for i in bin_maxes] for j in range(2)]
  for j, gal in enumerate(gal_mass): # for each galaxy
    if g_loc[j] not in locs:
      continue
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
  for i in orig_bins:
    print(i)
    print(len(i))
    print('')
  sys.exit()

  bins, bins_unc, bins_center, bins_center_unc = [[] for i in range(4)]
  for i in range(len(orig_bins)):
    g_actual = wh.g_actual_bins(orig_bins[i])
    bins.append(wh.average_growth_rate(sfh.g_exp, g_actual, orig_bins[i], t0, t1))
    bins_unc.append(wh.bin_uncertainty(sfh.g_exp, g_actual, orig_bins_unc[i], t0, t1))
    bins_center.append(wh.average_bin_start(sfh.g_exp, g_actual, orig_bins[i]))
    bins_center_unc.append(wh.uncertainty_bin_start(sfh.g_exp, g_actual, orig_bins_unc[i], bins_center[-1]))

  return(bins, bins_unc, bins_center, bins_center_unc)

def sf_m_at_z_fit(bins, bins_center, ext_bins_center):
  l_bins, l_bins_c = [], []
  for i, val in enumerate(bins):
    if val != 0:
      l_bins.append(math.log10(val))
      l_bins_c.append(bins_center[i])
  try:
    co_eff = np.polyfit(l_bins_c, l_bins, 1)
  except TypeError as e:
    if e.args[0] == 'expected non-empty vector for x':
      return([0 for i in ext_bins_center])
    else:
      print(e.args)
      sys.exit('bad error')

  fit_bins = [10**(co_eff[0] * i + co_eff[1]) for i in ext_bins_center]
  return(fit_bins)

# We want to see how much a galaxy that starts at mass x at z0 grows by z1
def schechter_sf_m_at_z(bins_center, z0, z1):
  pool = Pool(processes=4)
  bins = pool.starmap(hmc.correct, [[i, z0, z1] for i in bins_center])
  return(bins)


# This is the third option - sfr data. NB: z0 > z1
def sfr_data(ext_bins_center, z0, z1):
  a_low, a_high, b = h_whit.weight_parameters(z0, z1)
  m_star = 10.2
  bins = [10**(a_low * (mass - 10.2) + b) * 0.64e9 for mass in ext_bins_center]
  return(bins)

def plot_sf_m_at_z():
  info = {'xlim': [3.0, 10.0], 'ylim': [10, 1e10], 'ylog': True, 'xlabel6': r'$\mathregular{Start Mass \, log(M/M_\odot)}$', 'ylabel6': r'$\mathregular{\Delta M/\Delta t} \, M_\odot / Gyr$', 'legend6': ['Star Formation History', 'Parameterized Schechter Predictions', 'Whitaker SFR']}
  params = {'marker': ['x', 'None', 'None', 'None'], 'linestyle': ['None', '-', '-', '-'], 'color': ['b', 'g', 'r', 'b']}
  params2 = {'marker': ['x', 'None', 'None'], 'linestyle': ['None', '-', '-'], 'color': ['b', 'g', 'b']}
  gs = graph.setup6(info)

  bin_maxes, z, t_step_list  = [i for i in range(3, 9)], [3, 2, 1, 0.5, 0.1, 0.01], [1,1,1,3,5,15]
  sfh = data.sfh()
  ss = data.schechter_growth()

  e = []
  for i in range(len(z)):
    t_step = t_step_list[i] # Compensates for dense observations at later times
    index = h.find_nearest(sfh.z_times, z[i])
    z0, t0, z1, t1 = h.z_and_t_from_index_t_step(index, t_step, sfh.z_times)
    print(z0)
    if z0 > 3:
      raise Exception('Z too high')

    bins, bins_unc, bins_center, bins_center_unc = sf_m_at_z(bin_maxes, index, t_step)
    ext_bins_center = [3] + bins_center + [8, 8.5, 9, 9.5]
    bins_fit = sf_m_at_z_fit(bins, bins_center, ext_bins_center)

    start_z = [i for i, x in enumerate(ss.z) if x == z0] # indicies for this start_z on record
    steps = [x for i, x in enumerate(start_z) if t_step == ss.t_step[x]]
    if len(steps) == 1 and 0:
      print('Shortcut')
      s_bins = ss.d[steps[0]]
      ext_bins_center_s = ss.e[steps[0]]
    else:
      s_bins = schechter_sf_m_at_z(ext_bins_center, z0, z1)
      ext_bins_center_s = ext_bins_center

    if z0 > 0.5:
      sanity_bins = sfr_data(ext_bins_center, z0, z1)

    infoz = dict({'title6': 'Z = ' + str(round(z0, 3)) + '-' + str(round(z1, 4))}, **info)

    if z1 > 0.5:
      p = dict({'yerr':[0], 'yerr_vals': bins_unc, 'xerr':[0], 'xerr_vals': bins_center_unc}, **params)
      graph.line6(
          [bins, s_bins, sanity_bins, bins_fit],
          [bins_center, ext_bins_center_s, ext_bins_center, ext_bins_center],
          i, gs, info=infoz, params=p)
    else:
      p = dict({'yerr':[0], 'yerr_vals': bins_unc, 'xerr':[0], 'xerr_vals': bins_center_unc}, **params2)
      graph.line6(
          [bins, s_bins, bins_fit],
          [bins_center, ext_bins_center_s, ext_bins_center],
          i, gs, info=infoz, params=p)
  plt.show()

if __name__ == "__main__":
  if sys.version[0] != '3':
    sys.exit()
  plot_sf_m_at_z()
