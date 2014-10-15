#!/usr/bin/python3

import data
import graph
import matplotlib.pyplot as plt
import math
def schechter(m, ms, os, a, dm):
  return dm * math.log(10) * os  * (10 ** ((m - ms) * (1 + a))) * (math.e ** (-10 ** (m - ms)))


def dub_schechter(m, ms, os1, os2, a1, a2, dm):
  a = math.log(10) * math.e ** (-10 ** (m - ms)) * 10 ** (m - ms)
  b = os1 * 10 ** ((m - ms) * a1) + os2 * 10 ** ((m - ms) * a2)
  return dm * a * b

if __name__ == "__main__":
  smf = data.smf()
  info = {'xlabel': r'$\mathregular{log(M/M_\odot)}$', 'ylabel': r'$\mathregular{log(\phi Mpc^3/dex)}$', 'legend': smf.z_range, 'xlim': [7.75, 12.25], 'ylim': [-5.75, -0.75]}
  params = {'marker': 'x'}

  # Looks good!
  '''
  graph.line(smf.smf, smf.mass, dict({'title': 'SMF'}, **info), params)
  graph.line(smf.sf_smf, smf.mass, dict({'title': "Star Forming SMF"}, **info), params)
  graph.line(smf.q_smf, smf.mass, dict({'title': "Quiescent SMF"}, **info), params)
  plt.show()
  '''

  # Put on single graph?
  info = {'xlabel': r'$\mathregular{log(M/M_\odot)}$', 'ylabel': r'$\mathregular{log(\phi Mpc^3/dex)}$', 'legend': ['SMF', 'SF_SMF', 'Q_SMF'], 'xlim': [7.75, 12.25], 'ylim': [-5.75, -0.75]}

  f1 = graph.setup()
  for i in range(len(smf.smf)):
    f1 = graph.line8([smf.smf[i], smf.sf_smf[i], smf.q_smf[i]], smf.mass, i, f1, dict({'title': smf.z_range[i]}, **info), params)
  plt.show()

  # S func is bad?
  """
  res = []
  x = []
  for j in range(75, 120):
    i = j / 10
    x.append(i)
    #res.append(dub_schechter(i, 10.78, -2.54, -4.29, -0.98, -1.90, 0.1))
    res.append(schechter(i, 11.05, -2.96, -1.35, 0.1))
    #res.append(schechter(i, 11.00, -2.93, -1.35))

  print(res)
  print(x)
  graph.line([res], x)
  plt.show()
  """
