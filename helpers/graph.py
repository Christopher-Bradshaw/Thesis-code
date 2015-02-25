#!/usr/bin/python3
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import sys

def settings(info, af):
  if 'xlog' in info and info['xlog'] == True:
    af.set_xscale('log')
  if 'ylog' in info and info['ylog'] == True:
    af.set_yscale('log')
  if 'xlim' in info:
    af.set_xlim(info['xlim'])
  if 'ylim' in info:
    af.set_ylim(info['ylim'])
  if 'title' in info:
    plt.title(info['title'])
  if 'xlabel' in info:
    plt.xlabel(info['xlabel'])
  if 'ylabel' in info:
    plt.ylabel(info['ylabel'])
  if 'invert_xaxis' in info and info['invert_xaxis'] == True:
    af.invert_xaxis()
  return(af)

def actual_plot(x1, data, params, af):

  for i, y in enumerate(data):
    x = x1 if type(x1[0]) != list else x1[i]
    color = next(af._get_lines.color_cycle)

    marker = params['marker'] if 'marker' in params else None
    if type(marker) == list:
      marker = marker[i % len(marker)]

    linestyle = params['linestyle'] if 'linestyle' in params else '-'
    if type(linestyle) == list:
      linestyle = linestyle[i % len(linestyle)]

    yerr = params['yerr'] if 'yerr' in params else None
    if type(yerr) == list and i in yerr: # Yes error bars!
      errors = [[i[1] for i in params['yerr_vals']], [i[0] for i in params['yerr_vals']]]
      af.errorbar(x, y, yerr=errors, fmt="none", ecolor=color)

    xerr = params['xerr'] if 'xerr' in params else None
    if type(xerr) == list and i in xerr: # Yes error bars!
      errors = [[i[1] for i in params['xerr_vals']], [i[0] for i in params['xerr_vals']]]
      af.errorbar(x, y, xerr=errors, fmt="none", ecolor=color)

    plt.plot(x, y, marker=marker, linestyle=linestyle, color=color)

  return(af)

# data: a 2d array of data
# x: the x values of the data points
# info: general info about the plot
# params: specific info for this plot
def line(data, x=[], info={}, params={}, af1=None):
  if x == []:
    x = [i for i in range(1, len(data[0]) + 1)]

  if af1 == None:
    f1 = plt.figure()
    af1 = f1.add_subplot(111)

  af1 = settings(info, af1)

  for y in data:
    af1 = plt.plot(x, y, **params)

  if 'legend' in info:
    plt.legend(info['legend'], loc = "lower left")

  return(af1)

# Given two points, plots a line between them
# Each of these must be a list: start = [start.x, start.y]
def cut_line(start, end):
  plt.plot([start[0], end[0]], [start[1], end[1]], '--')

# Sets up a 2r x 4c plot with no white space
# Will hack a x/y label if they are provided in the params
def setup8(params={}):
  f1 = plt.figure(figsize = (2,4))
  gs = gridspec.GridSpec(2, 4)
  gs.update(wspace = 0, hspace = 0)
  if 'xlabel8' in params:
    f1.text(0.5, 0.05, params['xlabel8'], horizontalalignment='center', verticalalignment='center')
  if 'ylabel8' in params:
    f1.text(0.09, 0.5, params['ylabel8'], horizontalalignment='center', verticalalignment='center', rotation='vertical')
  return(gs)

# Mostly the same as line. Also takes the number of the plot (0-7) and the gs item created by setup8
def line8(data, x, num, gs, info={}, params={}):
  af = plt.subplot(gs[num])
  af = settings(info, af)

  if 'title8' in info:
    af.text(0.7, 0.8,info['title8'],horizontalalignment='center', verticalalignment='center', transform = af.transAxes)
  if num < 4:
    af.set_xticklabels([])
  if (num % 4):
    af.set_yticklabels([])

  for y in data:
    af = plt.plot(x, y, **params)

  if 'legend' in info:
    plt.legend(info['legend'], loc = "lower left")

# Sets up a 2r x 3c plot with no white space
# Will hack a x/y label if they are provided in the params
def setup6(params={}):
  f1 = plt.figure(figsize = (2,3))
  gs = gridspec.GridSpec(2, 3)
  gs.update(wspace = 0, hspace = 0)
  if 'xlabel6' in params:
    f1.text(0.5, 0.05, params['xlabel6'], horizontalalignment='center', verticalalignment='center')
  if 'ylabel6' in params:
    f1.text(0.09, 0.5, params['ylabel6'], horizontalalignment='center', verticalalignment='center', rotation='vertical')
  if 'legend6' in params:
    plt.legend(params['legend6'], loc = "lower left")
  return(gs)

# Mostly the same as line. Also takes the number of the plot (0-7) and the gs item created by setup8
def line6(data, x, num, gs, info={}, params={}):
  af = plt.subplot(gs[num])
  af = settings(info, af)

  if 'title6' in info:
    af.text(0.7, 0.8, info['title6'], horizontalalignment='center', verticalalignment='center', transform = af.transAxes)
  if num < 3:
    af.set_xticklabels([])
  if (num % 3):
    af.set_yticklabels([])

  af = actual_plot(x, data, params, af)

  if 'legend' in info:
    plt.legend(info['legend'], loc = "lower left")
