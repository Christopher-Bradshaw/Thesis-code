#!/usr/bin/python3
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# data: a 2d array of data
# x: the x values of the data points
# info: general info about the plot
# params: specific info for this plot

def line(data, x, info={}, params={}):
  f1 = plt.figure()
  af1 = f1.add_subplot(111)

  if 'xlim' in info:
    af1.set_xlim(info['xlim'])
  if 'ylim' in info:
    af1.set_ylim(info['ylim'])
  if 'title' in info:
    plt.title(info['title'])
  if 'xlabel' in info:
    plt.xlabel(info['xlabel'])
  if 'ylabel' in info:
    plt.ylabel(info['ylabel'])

  for y in data:
    af1 = plt.plot(x, y, **params)

  if 'legend' in info:
    plt.legend(info['legend'], loc = "lower left")

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
  if 'xlabel' in params:
    f1.text(0.5, 0.05, params['xlabel'], horizontalalignment='center', verticalalignment='center')
  if 'ylabel' in params:
    f1.text(0.09, 0.5, params['ylabel'], horizontalalignment='center', verticalalignment='center', rotation='vertical')
  return(gs)

# Mostly the same as line. Also takes the number of the plot (0-7) and the gs item created by setup8
def line8(data, x, num, gs, info={}, params={}):
  af = plt.subplot(gs[num])

  if 'xlim' in info:
    af.set_xlim(info['xlim'])
  if 'ylim' in info:
    af.set_ylim(info['ylim'])
  if 'title' in info:
    af.text(0.7, 0.8,info['title'],horizontalalignment='center', verticalalignment='center', transform = af.transAxes)
  if num < 4:
    af.set_xticklabels([])
  if (num % 4):
    af.set_yticklabels([])

  for y in data:
    af = plt.plot(x, y, **params)

  if 'legend' in info:
    plt.legend(info['legend'], loc = "lower left")
