import helpers.z_to_t as z_to_t
import math
import statistics
import numpy as np
import helpers.helpers as h
import helpers.schechter as hs
import helpers.z_to_t as z_to_t
import copy

# Numbers of mergers per Gyr at specified start mass, ratio and redshift
def merger_correction(M, u, z):
  A0, n, a0, a1, b0, b1, y, g0, g1, M0 = 10**(-2.2287), 2.4644, 0.2241, -1.1759, -1.2595, 0.0611, -0.0477, 0.7668, 0.4695, 2e11
  A_z = A0*(1+z)**n
  a_z = a0*(1+z)**a1
  b_z = b0*(1+z)**b1
  g_z = g0*(1+z)**g1
  a_z = a0*(1+z)**a1
  res = A_z * (M/1e10)**a_z * (1 + (M/M0)**g_z) * u ** (b_z + y * math.log10(M/1e10))
  return(res)

# Integrate between u0 and u1 (u0 < u1)
def integrated_u_merger_correction(M, u0, u1, z):
  if u0 > u1:
    raise
  A0, n, a0, a1, b0, b1, y, g0, g1, M0 = 10**(-2.2287), 2.4644, 0.2241, -1.1759, -1.2595, 0.0611, -0.0477, 0.7668, 0.4695, 2e11
  A_z = A0*(1+z)**n
  a_z = a0*(1+z)**a1
  b_z = b0*(1+z)**b1
  g_z = g0*(1+z)**g1
  a_z = a0*(1+z)**a1
  res1, res2 = [A_z * (M/1e10)**a_z * (1 + (M/M0)**g_z) * i ** (1 + b_z + y * math.log10(M/1e10)) / ((1 + b_z + y * math.log10(M/1e10))) for i in [u0, u1]]
  return(res2 - res1)

# z0 > z1 (z1 came after/is more recent)
# u0 < u1
def integrated_uz_merger_correction(M, u0, u1, z0, z1):
  if z1 > z0:
    raise
  time_bins = 100
  # t0 > t1 (t1 is more recent)
  t0, t1 = z_to_t.t_from_z(z0), z_to_t.t_from_z(z1)
  time_step = (t0 - t1)/time_bins
  time_centers = h.bins_centers(time_bins, t1, t0)
  total_m = 0

  for t in time_centers:
    z = z_to_t.z_from_t(t)
    m_rate = integrated_u_merger_correction(M, u0, u1, z) # per Gyr
    total_m += m_rate * time_step
  return(total_m)

def correct_smf(z0, z1):
  m_step, m_start, m_end = 50, 2, 12
  test_masses = [i/m_step for i in range(int(m_start*m_step), int(m_end*m_step))]
  u_step = 10
  mass_ratio_ranges = [10**-(i/u_step) for i in range(5*u_step)]

  SMF = [10**hs.param_double_schechter(i, z1) for i in test_masses]
  uncorr_SMF = copy.copy(SMF)
  for i, m in enumerate(test_masses):
    y = SMF[i]
    for u in range(len(mass_ratio_ranges) - 1):
      u1, u0 = mass_ratio_ranges[u], mass_ratio_ranges[u+1]
      u_avg = statistics.mean([u0, u1])
      mu = integrated_uz_merger_correction(m, u0, u1, z0, z1)

      m1, m2 = math.log10(10**m/(u_avg + 1)), math.log10(10**m*u_avg/(u_avg + 1))
      assert round(math.log10(sum([10**m1, 10**m2])), 2) == round(m, 2)

      # Find where in the SMF these two will come
      m1, m2 = [int((mx - m_start) * m_step) for mx in [m1, m2]]
      for mx in [m1, m2]:
        if mx < 0:
          continue
        SMF[mx] += y * mu # some mult for width - appears no
      SMF[i] -= y * mu
  return(SMF, test_masses, uncorr_SMF) # return uncorr SMF for testing

def correct(mass, z0, z1):
  # Generate SMF
  delta_t = z_to_t.t_from_z(z0) - z_to_t.t_from_z(z1)
  SMF, test_masses, uncorr_SMF = correct_smf(z0, z1)

  # Compare to at z0
  target = 10**hs.param_double_schechter(mass, z0)
  # SMF is monotonically decreasing, so look though until less than target
  new_mass = np.interp(target, SMF[::-1], test_masses[::-1])
  ######### TEST
  '''
  pSMF, p_oldSMF = [[math.log10(i) for i in j] for j in [SMF, old_SMF]]
  z0_SMF = [hs.param_double_schechter(i, z0) for i in test_masses]
  graph.line([pSMF, p_oldSMF, z0_SMF], x=test_masses)
  plt.show()
  '''
  ########
  return((10**new_mass - 10 ** mass) / delta_t)
