#!/usr/bin/env python3
import sys

if __name__ == "__main__":
  f = open('sfh_data', 'r')
  for line in f:
    if line == '###\n':
      break

  legend = ['name', 'total'] + ["m" + str(i/10) for i in range(101, 65, -1)]
  res = []
  names = []
  totals = []
  locations = [6 + 5*i for i in range(37)]
  for line in f:
    x = [i for i in line[18:].split(' ') if i != '']
    totals.append(x[1])
    res.append([float(x[i]) for i in locations])
    names.append(line[:18].rstrip(' '))
  for i in res:
    print(i)
  print(names)
  print(totals)
  print(legend)
