import helpers.z_to_t as z_to_t
import math
import helpers.helpers as h

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

