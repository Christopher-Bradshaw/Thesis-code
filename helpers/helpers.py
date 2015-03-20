import helpers.z_to_t as z_to_t

def find_nearest(some_list, some_val):
  index = 0
  for i in range(len(some_list)):
    if abs(some_list[i] - some_val) < abs(some_list[index] - some_val):
      index = i
  return(index)

# Given an index, returns the z value and the t value that that z corresponds to (wrt sfh)
def z_and_t_from_index_t_step(index, t_step, z_times):
  assert(t_step > 0)
  z0 = z_times[index]
  t0 = z_to_t.t_from_z(z0)
  try:
    z1 = z_times[index + t_step]
    t1 = z_to_t.t_from_z(z1)
  except IndexError:
    raise IndexError('t_step was too great')

  return(z0, t0, z1, t1)
