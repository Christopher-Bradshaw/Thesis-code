import math

"""
Remembering that the sfh masses are in a list [m_at_t_0, m_at_t_2 ... ]
Given index, and step finds rate of increase between m_at_t_index and m_at_t_(index + t_step)
Requires also the max values for each bin

So we have a list of masses: imp_mass = [ [start_1, end_1], [start_2, end_2], ... , [start_n, end_n]]
And a list of uncertainties: imp_mass_unc = [ [[start_+_1, start_-_1], [end_+_1, end_-_1]] ... ]  

These are binned by start mass. uncertainties should be binned in same way.

Each bin then calculates the average start and end mass and therefore the delta mass
"""

# where b = [ [[m0i, m0f], type], [[m1i, m1f], type] ... ]

def g_actual_bins(bins):
  if len(bins) == 0:
    return({'A': 0, 'G': 0, 'L': 0})
  bins = [i[1] for i in bins]
  totals = {'A': bins.count('A'), 'G': bins.count('G'), 'L': bins.count('L')}
  percs = {k: v/sum(totals.values()) for k, v in totals.items()}
  return(percs)


def average_growth_rate(g_exp, g_actual, b, t0, t1):
  count, mass = 0, 0
  for galaxy in b:
    ratio = g_exp[galaxy[1]] / g_actual[galaxy[1]]
    mass += (galaxy[0][1] - galaxy[0][0]) * ratio
    count += ratio
  return(mass / (count * (t0 - t1)) if len(b) else 0)

# where b = [ [[[u0i+, u0i-], [u0f+, u0f-] ], type] ... ]
def bin_uncertainty(g_exp, g_actual, b, t0, t1):
  count, sp, sn, ep, en = [0 for i in range(5)]
  for galaxy in b:
    ratio = g_exp[galaxy[1]] / g_actual[galaxy[1]]
    count += ratio
    sp += (ratio * galaxy[0][0][0]) ** 2
    sn += (ratio * galaxy[0][0][1]) ** 2
    ep += (ratio * galaxy[0][1][0]) ** 2
    en += (ratio * galaxy[0][1][1]) ** 2
  sp, sn, ep, en = [math.sqrt(i) / count if i else 0 for i in [sp, sn, ep, en]]
  dp = math.sqrt(sp ** 2 + ep ** 2)
  dn = math.sqrt(sn ** 2 + en ** 2)
  return([dp/(t0-t1), dn/(t0-t1)])


# where b = [ [[m0i, m0f], type], [[m1i, m1f], type] ... ]
def average_bin_start(g_exp, g_actual, b):
  count, mass = 0, 0
  for galaxy in b:
    ratio = g_exp[galaxy[1]] / g_actual[galaxy[1]]
    count += ratio
    mass += galaxy[0][0] * ratio
  return(math.log10(mass / count) if len(b) else 0)

def uncertainty_bin_start(g_exp, g_actual, b, center):
  c = 10**center
  count, sp, sn = [0 for i in range(3)]
  for galaxy in b:
    ratio = g_exp[galaxy[1]] / g_actual[galaxy[1]]
    count += ratio
    sp += (ratio * galaxy[0][0][0]) ** 2
    sn += (ratio * galaxy[0][0][1]) ** 2
  sp, sn = [math.sqrt(i) / count if i else 0 for i in [sp, sn]]
  sp = math.log10(c + sp) - center
  sn = center - math.log10(c - sn)
  return([sp, sn])
