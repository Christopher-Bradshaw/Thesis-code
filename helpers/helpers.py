def find_nearest(some_list, some_val):
  index = 0
  for i in range(len(some_list)):
    if abs(some_list[i] - some_val) < abs(some_list[index] - some_val):
      index = i
  return(index)

