#!/usr/bin/python3
import matplotlib.pyplot as plt

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

def setup():
  f1 = plt.figure()
  ax = f1.add_subplot(111)

  ax.axes.xaxis.set_ticklabels([])
  ax.axes.yaxis.set_ticklabels([])

  ax.set_xlabel('HO')
  ax.set_ylabel('YO')
  return(f1)

# as above but plots 8 to a graph (must be called 8 times)
def line8(data, x, num, f1, info={}, params={}):
  af = f1.add_subplot(241 + num)

  if 'xlim' in info:
    af.set_xlim(info['xlim'])
  if 'ylim' in info:
    af.set_ylim(info['ylim'])
  if 'title' in info:
    #plt.title(info['title'])
    af.text(0.7, 0.8,info['title'],horizontalalignment='center', verticalalignment='center', transform = af.transAxes)

  if num < 4:
    #af.axes.get_xaxis().set_ticks([])
    af.set_xticklabels([])
  if (num % 4):
    #af.axes.get_yaxis().set_ticks([])
    af.set_yticklabels([])

  for y in data:
    af = plt.plot(x, y, **params)

  if 'legend' in info:
    plt.legend(info['legend'], loc = "lower left")
  return f1
