#!/usr/bin/env python3

"""
This takes the data.smf (raw zfourge data) and data.schechter (that data fit to schechter funcs)
and plots graphs with it
"""

import helpers.data as data
import helpers.graph as graph
import matplotlib.pyplot as plt
import helpers.schechter as h
import sys

if __name__ == "__main__":

  # Plot SUBSET raw data
  smf = data.smf()
  for i in range(1,3):
    info = {'xlabel': r'$\mathregular{log(M/M_\odot)}$', 'ylabel': r'$\mathregular{log(\phi / Mpc^3/dex)}$', 'legend': smf.z_range[-i:], 'xlim': [7.75, 12.25], 'ylim': [-5.75, -0.75]}
    params = {'marker': 'x'}
    graph.line(smf.smf[-i:], smf.mass, dict({'title': 'SMF'}, **info), params)
  plt.show()

  # Plot raw data: total, quiescent, star forming
  smf = data.smf()
  info = {'xlabel': r'$\mathregular{log(M/M_\odot)}$', 'ylabel': r'$\mathregular{log(\phi / Mpc^3/dex)}$', 'legend': smf.z_range, 'xlim': [7.75, 12.25], 'ylim': [-5.75, -0.75]}
  params = {'marker': 'x'}

  graph.line(smf.smf, smf.mass, dict({'title': 'SMF'}, **info), params)
  graph.line(smf.sf_smf, smf.mass, dict({'title': "Star Forming SMF"}, **info), params)
  graph.line(smf.q_smf, smf.mass, dict({'title': "Quiescent SMF"}, **info), params)

  # Plot raw data: all 8 z bins on same graph
  info = {'legend': ['SMF', 'SF_SMF', 'Q_SMF'], 'xlim': [7.75, 12.25], 'ylim': [-5.75, -0.75], 'xlabel8': r'$\mathregular{log(M/M_\odot)}$', 'ylabel8': r'$\mathregular{log(\phi / Mpc^3/dex)}$'}
  params = {'marker': 'x'}
  gs = graph.setup8(info)
  for i in range(len(smf.smf)):
    graph.line8([smf.smf[i], smf.sf_smf[i], smf.q_smf[i]], smf.mass, i, gs, dict({'title8': smf.z_range[i]}, **info), params)



  ### Plot schechter fits: single and double, quiescent, star forming and total
  # These all come directly from the Zfourge schechter values
  s = data.schechter()
  info = {'xlabel8': r'$\mathregular{log(M/M_\odot)}$', 'ylabel8': r'$\mathregular{log(\phi / Mpc^3/dex)}$', 'legend': s.z_range, 'xlim': [7.75, 12.25], 'ylim': [-5.75, -0.75]}
  x = [i/10 for i in range(75, 125)]

  for each in [['', s.double], ['Star forming', s.sf_double], ['Quiescent', s.q_double]]:
    res = []
    for i in each[1]:
      res.append([])
      for j in x:
        res[-1].append(h.double_schechter(j, *i[:-1]))

    graph.line(res, x, dict({'title': each[0] + ' Double'}, **info))

  for each in [['', s.single], ['Star forming', s.sf_single], ['Quiescent', s.q_single]]:
    res = []
    for i in each[1]:
      res.append([])
      for j in x:
        res[-1].append(h.schechter(j, *i[:3]))

    graph.line(res, x, dict({'title': each[0] + ' Single'}, **info))


  s = data.schechter()
  ### Plot parameterised schechter function
  info = {'xlabel': r'$\mathregular{log(M/M_\odot)}$', 'ylabel': r'$\mathregular{log(\phi / Mpc^3/dex)}$', 'legend': s.z_range, 'xlim': [7.75, 12.25], 'ylim': [-5.75, -0.75]}
  x = [i/10 for i in range(75, 125)]
  res = []
  for i in s.z_avg: # For each z value
    res.append([])
    for j in x: # Lots of points!
      res[-1].append(h.param_double_schechter(j, i))
  graph.line(res, x, dict({'title': 'Paramaterized Double Schecter'}, **info))

  """ Only do 2"""
  ### Plot parameterised schechter function
  info = {'xlabel': r'$\mathregular{log(M/M_\odot)}$', 'ylabel': r'$\mathregular{log(\phi / Mpc^3/dex)}$', 'legend': [s.z_range[2], s.z_range[6]], 'xlim': [7.75, 11.25], 'ylim': [-5.75, -0.75]}
  x = [i/10 for i in range(75, 125)]
  res = []
  for i in [s.z_avg[2], s.z_avg[6]]: # For each z value
    res.append([])
    for j in x: # Lots of points!
      res[-1].append(h.param_double_schechter(j, i))
  graph.line(res, x, dict({'title': 'Paramaterized Double Schecter'}, **info))

  # Show everything
  plt.show()
