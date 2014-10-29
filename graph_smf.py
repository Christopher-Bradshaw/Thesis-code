#!/usr/bin/python3

import data
import graph
import matplotlib.pyplot as plt
import math
import sys
def schechter(m, ms, a, phi_s):
  phi_s = 10 ** phi_s
  ret = math.log(10) * phi_s * (10 ** ((m - ms) * (1 + a))) * (math.e ** (-10 ** (m - ms)))
  return(math.log10(ret))


def dub_schechter(m, ms, a1, phi_s1, a2, phi_s2):
  phi_s1 = 10 ** phi_s1
  phi_s2 = 10 ** phi_s2

  a = math.log(10) * math.e ** (-10 ** (m - ms)) * 10 ** (m - ms)
  b = phi_s1 * 10 ** ((m - ms) * a1) + phi_s2 * 10 ** ((m - ms) * a2)
  return(math.log10(a * b))

if __name__ == "__main__":
  """
  smf = data.smf()
  info = {'xlabel': r'$\mathregular{log(M/M_\odot)}$', 'ylabel': r'$\mathregular{log(\phi Mpc^3/dex)}$', 'legend': smf.z_range, 'xlim': [7.75, 12.25], 'ylim': [-5.75, -0.75]}
  params = {'marker': 'x'}
  graph.line(smf.smf, smf.mass, dict({'title': 'SMF'}, **info), params)
  graph.line(smf.sf_smf, smf.mass, dict({'title': "Star Forming SMF"}, **info), params)
  graph.line(smf.q_smf, smf.mass, dict({'title': "Quiescent SMF"}, **info), params)

  info = {'legend': ['SMF', 'SF_SMF', 'Q_SMF'], 'xlim': [7.75, 12.25], 'ylim': [-5.75, -0.75], 'xlabel': r'$\mathregular{log(M/M_\odot)}$', 'ylabel': r'$\mathregular{log(\phi Mpc^3/dex)}$'}
  params = {'marker': 'x'}
  gs = graph.setup8(info)
  for i in range(len(smf.smf)):
    graph.line8([smf.smf[i], smf.sf_smf[i], smf.q_smf[i]], smf.mass, i, gs, dict({'title': smf.z_range[i]}, **info), params)
  """



  ### Plot schechter
  s = data.schechter()
  info = {'xlabel': r'$\mathregular{log(M/M_\odot)}$', 'ylabel': r'$\mathregular{log(\phi Mpc^3/dex)}$', 'legend': s.z_range, 'xlim': [7.75, 12.25], 'ylim': [-5.75, -0.75]}
  x = [i/10 for i in range(75, 125)]

  for each in [['', s.double], ['Star forming', s.sf_double], ['Quiescent', s.q_double]]:
    res = []
    for i in each[1]:
      res.append([])
      for j in x:
        res[-1].append(dub_schechter(j, *i))

    graph.line(res, x, dict({'title': each[0] + ' Double'}, **info))


  for each in [['', s.single], ['Star forming', s.sf_single], ['Quiescent', s.q_single]]:
    res = []
    for i in each[1]:
      res.append([])
      for j in x:
        res[-1].append(schechter(j, *i))

    graph.line(res, x, dict({'title': each[0] + ' Single'}, **info))
  plt.show()
