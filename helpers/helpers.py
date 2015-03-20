import z_to_t
import math
import numpy as np


def find_nearest(some_list, some_val):
  index = 0
  for i in range(len(some_list)):
    if abs(some_list[i] - some_val) < abs(some_list[index] - some_val):
      index = i
  return(index)

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



"""
Remembering that the sfh masses are in a list [m_at_t_0, m_at_t_2 ... ]
Given index, and step finds rate of increase between m_at_t_index and m_at_t_(index + t_step)
Requires also the max values for each bin

So we have a list of masses: imp_mass = [ [start_1, end_1], [start_2, end_2], ... , [start_n, end_n]]
And a list of uncertainties: imp_mass_unc = [ [[start_+_1, start_-_1], [end_+_1, end_-_1]] ... ]  

These are binned by start mass. uncertainties should be binned in same way.

Each bin then calculates the average start and end mass and therefore the delta mass
"""

class weisz_helpers():
  # where b = [ [[m0i, m0f], type], [[m1i, m1f], type] ... ]
  def __init__(self, use_old = False):
    self.use_old = use_old
    print(self.use_old)

  def average_growth_rate(self, sfh, b, t0, t1):
    if self.use_old:
      start = np.mean([j[0][0] for j in b]) if len(b) else 0
      end = np.mean([j[0][1] for j in b]) if len(b) else 0
      return((end - start) / (t0 - t1))

    g_exp = sfh.g_exp
    g_actual = sfh.g_actual()
    count, mass = 0, 0
    for galaxy in b:
      ratio = g_exp[galaxy[1]] / g_actual[galaxy[1]]
      mass += (galaxy[0][1] - galaxy[0][0]) * ratio
      count += ratio

    return(mass / (count * (t0 - t1)))

  # where b = [ [[[u0i+, u0i-], [u0f+, u0f-] ], type] ... ]
  def bin_uncertainty(self, sfh, b, t0, t1):
    if len(b) == 0:
      return([0,0])
    if self.use_old:
      start_pos_unc = math.sqrt(sum([(j[0][0][0])**2 for j in b]))/len(b)
      start_neg_unc = math.sqrt(sum([(j[0][0][1])**2 for j in b]))/len(b)
      end_pos_unc =   math.sqrt(sum([(j[0][1][0])**2 for j in b]))/len(b)
      end_neg_unc =   math.sqrt(sum([(j[0][1][1])**2 for j in b]))/len(b)

      diff_pos_unc = math.sqrt(start_pos_unc ** 2 + end_pos_unc ** 2)
      diff_neg_unc = math.sqrt(start_neg_unc ** 2 + end_neg_unc ** 2)
      return([diff_pos_unc/(t0-t1), diff_neg_unc/(t0-t1)])

    g_exp = sfh.g_exp
    g_actual = sfh.g_actual()
    count, sp, sn, ep, en = [0 for i in range(5)]
    for galaxy in b:
      ratio = g_exp[galaxy[1]] / g_actual[galaxy[1]]
      count += ratio
      sp += (ratio * galaxy[0][0][0]) ** 2
      sn += (ratio * galaxy[0][0][1]) ** 2
      ep += (ratio * galaxy[0][1][0]) ** 2
      en += (ratio * galaxy[0][1][1]) ** 2
    sp, sn, ep, en = [math.sqrt(i) / count for i in [sp, sn, ep, en]]
    dp = math.sqrt(sp ** 2 + ep ** 2)
    dn = math.sqrt(sn ** 2 + en ** 2)
    return([dp/(t0-t1), dn/(t0-t1)])


  # where b = [ [[m0i, m0f], type], [[m1i, m1f], type] ... ]
  def average_bin_start(self, sfh, b):
    if self.use_old:
      return(math.log10(np.mean([i[0][0] for i in b])) if len(b) else '-inf')
    g_exp = sfh.g_exp
    g_actual = sfh.g_actual()
    count, mass = 0, 0
    for galaxy in b:
      ratio = g_exp[galaxy[1]] / g_actual[galaxy[1]]
      count += ratio
      mass += galaxy[0][0] * ratio

    return(math.log10(mass / count) if len(b) else '-inf')

  def uncertainty_bin_start(self, sfh, b, center):
    c = 10**center
    if len(b) == 0:
      return([-np.inf,np.inf])
    if self.use_old:
      start_pos_unc = math.sqrt(sum([(j[0][0][0])**2 for j in b]))/len(b)
      start_neg_unc = math.sqrt(sum([(j[0][0][1])**2 for j in b]))/len(b)

      start_pos_unc = math.log10(c + start_pos_unc) - center
      start_neg_unc = center - math.log10(c - start_neg_unc)
      return([start_pos_unc, start_neg_unc])

    g_exp = sfh.g_exp
    g_actual = sfh.g_actual()
    count, sp, sn = [0 for i in range(3)]
    for galaxy in b:
      ratio = g_exp[galaxy[1]] / g_actual[galaxy[1]]
      count += ratio
      sp += (ratio * galaxy[0][0][0]) ** 2
      sn += (ratio * galaxy[0][0][1]) ** 2
    sp, sn = [math.sqrt(i) / count for i in [sp, sn]]
    sp = math.log10(c + sp) - center
    sn = center - math.log10(c - sn)
    return([sp, sn])
