#
# Class for management of an image sequence.
# The 'right' key advances through an image sequence.
#    (e.g. on a Dell laptop, this is 'alt-right-arrow')
# The 'left' key goes backward through image sequence.
#    (e.g. on a Dell laptop, this is 'alt-left-arrow')
#  
# Copyright (c) 2013 RadiaBeam Technologies. All rights reserved
# 
# python imports
import math

# SciPy imports
import matplotlib.pyplot as plt
import numpy as np

class RbPlotImageSequence(object):
    """Creates a series of axes in a figure where only one is displayed at any
    given time. Which plot is displayed is controlled by the arrow keys."""
    def __init__(self):
        self.fig = plt.figure()
        self.axes = []
        self._i = 0 # Currently displayed axes index
        self._n = 0 # Last created axes index
        self.fig.canvas.mpl_connect('key_press_event', self.on_keypress)

    def __iter__(self):
        while True:
            yield self.new()

    def new(self):
        # The label needs to be specified so that a new axes will be created
        # instead of "add_axes" just returning the original one.
        ax = self.fig.add_axes([0.15, 0.1, 0.8, 0.8], 
                               visible=False, label=self._n)
        self._n += 1
        self.axes.append(ax)
        return ax

    def on_keypress(self, event):
        if event.key == 'right':
            self.next_plot()
        elif event.key == 'left':
            self.prev_plot()
        else:
            return
        self.fig.canvas.draw()

    def next_plot(self):
        self.axes[self._i].set_visible(False)
        if self._i < len(self.axes)-1:
            self._i += 1
        else:
            self._i = 0
        self.axes[self._i].set_visible(True)

    def prev_plot(self):
        self.axes[self._i].set_visible(False)
        if self._i > 0:
            self._i -= 1
        else:
            self._i = len(self.axes)-1
        self.axes[self._i].set_visible(True)

    def show(self):
        self.axes[self._i].set_visible(True)
        plt.show()
