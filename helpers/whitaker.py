# z0 > z1
def weight_parameters(z0, z1):
  if z1 < 0.5 or z0 > 3 or z1 > z0:
    raise

  params = [              # [a_low, a_high, b]
      [0.94, 0.14, 1.11], # 0.5 - 1.0
      [0.99, 0.51, 1.31], # 1.0 - 1.5
      [1.04, 0.62, 1.49], # 1.5 - 2.0
      [0.91, 0.67, 1.62]  # 2.0 - 3.0
  ]
  res = [[[0,0,0],0]] + [[i, 0] for i in params]
  cutoff = [0.0, 1.0, 1.5, 2.0, 3.0]
  for i in range(len(cutoff)):
    if z1 < cutoff[i]:
      res[i][1] = cutoff[i] - z1 - sum([res[i-j-1][1] for j in range(i)])
    if z0 < cutoff[i]:
      res[i][1] -= cutoff[i] - z0

  [a_low, a_high, b] = [sum([res[i][0][j] * res[i][1] for i in range(len(res))])/sum([res[i][1] for i in range(len(res))]) for j in range(3)]
  return(a_low, a_high, b)
