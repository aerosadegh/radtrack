"""
Python class to emulate XGenesis postprocessing of GENESIS1.3 simulations.
Parses the GENESIS .out file

Copyright (c) RadiaBeam Technologies, 2015. All rights reserved.
"""
__author__ = 'swebb'
import numpy as np
from matplotlib import pyplot as plt
import scipy.interpolate as interp
from matplotlib.widgets import Slider, Button, RadioButtons


class RbXGenesisTDep:

    def __init__(self):
        self.file_open = False
        self.data_set = {}
        self.data_label = {}
        self.data_set['z']     = -1
        self.data_label['z'] = 'z [m]'
        self.data_set['aw']    = -1
        self.data_label['aw'] = 'a_w'
        self.data_set['QF']    = -1
        self.data_label['QF'] = 'dB/dx [T/m]'
        self.data_set['Power'] = -1
        self.data_label['Power'] = 'P [W]'
        self.data_set['Increment'] = -1
        self.data_label['Increment'] = '(1/P) dP/dz [m^-1]'
        self.data_set['p_mid'] = -1
        self.data_label['p_mid'] = '???'
        self.data_set['Phase'] = -1
        self.data_label['Phase'] = 'Phase [rad]'
        self.data_set['Rad. Size'] = -1
        self.data_label['Rad. Size'] = 'RMS radiation width [m]'
        self.data_set['Far Field'] = -1
        self.data_label['Far Field'] = 'dP/dW [W/rad^2]'
        self.data_set['Energy'] = -1
        self.data_label['Energy'] = '(E - E_0)/mc^2'
        self.data_set['Energy Spread'] = -1
        self.data_label['Energy Spread'] = 'RMS Gamma'
        self.data_set['X Beam Size'] = -1
        self.data_label['X Beam Size'] = 'RMS x size [m]'
        self.data_set['Y Beam Size'] = -1
        self.data_label['Y Beam Size'] =  'RMS y size [m]'
        self.data_set['X Centroid'] = -1
        self.data_label['X Centroid'] = '<x> [m]'
        self.data_set['Y Centroid'] = -1
        self.data_label['Y Centroid'] = '<y> [m]'
        self.data_set['Bunching'] = -1
        self.data_label['Bunching'] = '|< e^(i theta)>|'
        self.data_set['Error'] = -1
        self.data_label['Error'] = 'Delta P/P$ [%]'

        self.data_set['s'] = -1
        self.data_label['s'] = 's [m]'


    def parse_output(self, filename):
        """
        Parse a GENESIS .out file
        :param filename:
        :return:
        """

        genesis_file = open(filename, 'r')
        line = genesis_file.readline()

        # Find the required parameters
        reqdparams = ['nslice', 'zsep', 'xlamds']

        # Advance to find where the required parameters and number of steps
        # can be found in the GENESIS output
        while not 'entries per record' in line:
            line = genesis_file.readline()
            if any(x in line for x in reqdparams):
                if reqdparams[0] in line:
                    nslices = int(line.split()[-1].replace("D", "E"))
                if reqdparams[1] in line:
                    zsep = float(line.split()[-1].replace("D", "E"))
                if reqdparams[2] in line:
                    xlamds = float(line.split()[-1].replace("D", "E"))

        ds = zsep*xlamds
        self.data_set['s'] = np.arange(0., nslices*ds, ds)

        num_steps = int(line.split()[0])

        first_three_keys = ['z', 'aw', 'QF']
        last_keys = ['Power', 'Increment', 'p_mid', 'Phase', 'Rad. Size',
                     'Energy', 'Bunching', 'X Beam Size', 'Y Beam Size',
                     'Error', 'X Centroid', 'Y Centroid', 'Energy Spread',
                     'Far Field']

        for key in first_three_keys:
            self.data_set[key] = np.zeros(num_steps-1)

        for key in last_keys:
            self.data_set[key] = np.zeros((nslices, num_steps-1))

        # Advance to the first set of data
        while not 'z[m]' in line:
            line = genesis_file.readline()

        # Read in the first three keys first
        for lineIdx in range(0, num_steps-1):
            line = genesis_file.readline()
            for idx in range(0, len(first_three_keys)-1):
                self.data_set[first_three_keys[idx],lineIdx] = \
                    float(line.split()[idx])

        # Iterate over slices
        for slice in range(1, nslices):

            while not 'power' in line:
                line = genesis_file.readline()

            for lineIdx in range(0, num_steps-1):
                line = genesis_file.readline()
                for idx in range(0, len(last_keys)):
                    self.data_set[last_keys[idx]][slice, lineIdx] = \
                        float(line.split()[idx])

        genesis_file.close()


    def plot_data(self, x_axis, y_axis):
        """
        Plot data from the keys given as arguments
        :param x_axis:
        :param y_axis:
        :return: plot
        """
        if not x_axis =='z' or not x_axis == 's':
            msg = 'For time-dependent GENESIS simulations, the x-axis must ' \
                  'be either s or z.'
            Exception(msg)
        if not y_axis in self.data_set.keys():
            msg = 'Data type', y_axis, 'not recognized'
            Exception(msg)

        # Compute a spline function for the interpolation
        print self.data_set[y_axis]
        self.yaxis_function = interp.interp2d(self.data_set['s'],
                                              self.data_set['z'],
                                              self.data_set[y_axis])

        print 'y(0,0) =', self.yaxis_function(self.data_set['s'][0],
                                              self.data_set['z'][0])

        self.fig, self.ax = plt.subplots()

        slider_axis = plt.axes([0.25, 0.1, 0.65, 0.03])

        if x_axis == 's':
            self.x_axis = 's'
            self.sliderVar = Slider(slider_axis, 'z [m]',
                               self.data_set['z'][0], self.data_set['z'][-1])

            initial_function = self.yaxis_function(self.data_set['s'],
                                                   self.data_set['z'][0])

            self.this_plot, = plt.plot(self.data_set['s'], initial_function)


        if x_axis == 'z':
            self.x_axis = 'z'
            self.sliderVar = Slider(slider_axis, 's [m]',
                               self.data_set['s'][0], self.data_set['s'][-1])

            initial_function = self.yaxis_function(self.data_set['s'][0],
                                                   self.data_set['z'])

            self.this_plot, = plt.plot(self.data_set['z'], initial_function)

        self.sliderVar.on_changed(self.update_plot)

        #plt.xlabel(self.data_label[x_axis])
        #plt.ylabel(self.data_label[y_axis])
        plt.tight_layout()
        plt.show()

    def update_plot(self, newValue):

        if self.x_axis == 'z':
            self.this_plot.set_ydata(
                self.yaxis_function(self.data_set['z'],newValue))

        if self.x_axis == 's':
            self.this_plot.set_ydata(
                self.yaxis_function(newValue,self.data_set['s']))

        self.fig.canvas.draw_idle()