def weight_parameters(z0, z1):
  if z1 < 0.5 or z0 > 3 or z1 > z0:
    raise
  params = [              # [a_low, a_high, b]
      [0.94, 0.14, 1.11], # 0.5 - 1.0
      [0.99, 0.51, 1.31], # 1.0 - 1.5
      [1.04, 0.62, 1.49], # 1.5 - 2.0
      [0.91, 0.67, 1.62]  # 2.0 - 3.0
  ]
  res = [[],[]]
  cutoff = [0.0, 1.0, 1.5, 2.0, 3.0]

  for i in range(len(cutoff)):
    if z0 <= cutoff[i] and res[0] == []:
      res[0] = [params[i-1], z0 - cutoff[i-1]]
    if z1 <= cutoff[i] and res[1] == []:
      res[1] = [params[i-1], cutoff[i] - z1]

  # Rounding needed for assertions
  [a_low, a_high, b] = [(res[0][0][i] * res[0][1] + res[1][0][i] * res[1][1])/(res[0][1] + res[1][1]) for i in range(3)]

  assert ((a_low < res[1][0][0]) and (a_low > res[0][0][0])) or ((a_low < res[0][0][0]) and (a_low > res[1][0][0])) or (a_low == res[0][0][0] == res[1][0][0])
  assert ((a_high < res[1][0][1]) and (a_high > res[0][0][1])) or ((a_high < res[0][0][1]) and (a_high > res[1][0][1])) or (a_high == res[0][0][1] == res[1][0][1])
  assert ((b < res[1][0][2]) and (b > res[0][0][2])) or ((b < res[0][0][2]) and (b > res[1][0][2])) or (b == res[0][0][2] == res[1][0][2])
  print(a_low, a_high, b)
