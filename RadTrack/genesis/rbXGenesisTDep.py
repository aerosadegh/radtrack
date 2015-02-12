"""
Python class to emulate XGenesis postprocessing of GENESIS1.3 simulations.
Parses the GENESIS .out file

Copyright (c) RadiaBeam Technologies, 2015. All rights reserved.
"""
__author__ = 'swebb'
import numpy as np
from matplotlib import pyplot as plt
import scipy.interpolate as interp
from matplotlib.widgets import Slider

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
        self.data_label['Phase'] = u'\u03A6 [rad]'
        self.data_set['Rad. Size'] = -1
        self.data_label['Rad. Size'] = 'RMS radiation width [m]'
        self.data_set['Far Field'] = -1
        self.data_label['Far Field'] = u'dP/d\u03A9 [W/rad^2]'
        self.data_set['Energy'] = -1
        self.data_label['Energy'] = u'(\u03B3 - \u03B3\u2080)/mc^2'
        self.data_set['Energy Spread'] = -1
        self.data_label['Energy Spread'] = u'\u03C3\u2091 [keV]'
        self.data_set['X Beam Size'] = -1
        self.data_label['X Beam Size'] = u'\u03C3_x [m]'
        self.data_set['Y Beam Size'] = -1
        self.data_label['Y Beam Size'] =  u'\u03C3_y [m]'
        self.data_set['X Centroid'] = -1
        self.data_label['X Centroid'] = '<x> [m]'
        self.data_set['Y Centroid'] = -1
        self.data_label['Y Centroid'] = '<y> [m]'
        self.data_set['Bunching'] = -1
        self.data_label['Bunching'] = u'|<exp(i \u03B8)>|'
        self.data_set['Error'] = -1
        self.data_label['Error'] = u'\u0394P/P [%]'

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
                self.data_set[first_three_keys[idx]][lineIdx] = \
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
        self.yaxis_function = interp.interp2d(self.data_set['s'],
                                              self.data_set['z'],
                                              self.data_set[y_axis].T,
                                              kind='linear')

        self.fig, self.ax = plt.subplots()

        plt.subplots_adjust(bottom=0.25)
        slider_axis = plt.axes([0.2, 0.1, 0.65, 0.03])

        if x_axis == 's':
            self.x_axis = 's'
            numpoints = np.shape(self.data_set['s'])[0]
            initial_function = \
                np.reshape(self.yaxis_function(self.data_set['s'],
                                               self.data_set['z'][0]),
                           numpoints)
            self.sliderVar = Slider(slider_axis, 'z [m]',
                                    self.data_set['z'][0],
                                    self.data_set['z'][-1],
                                    valinit=self.data_set['z'][0])
            self.this_plot, = plt.plot(self.data_set['s'], initial_function)


        if x_axis == 'z':
            self.x_axis = 'z'
            numpoints = np.shape(self.data_set['z'])[0]
            initial_function = \
                np.reshape(self.yaxis_function(self.data_set['s'][0],
                                               self.data_set['z']),
                           numpoints)
            self.sliderVar = Slider(slider_axis, 's [m]',
                                    self.data_set['s'][0],
                                    self.data_set['s'][-1],
                                    valinit=self.data_set['s'][0])
            self.this_plot, = plt.plot(self.data_set['z'], initial_function)


        self.ax.set_ylabel(self.data_label[y_axis])
        self.ax.set_xlabel(self.data_label[x_axis])

        self.sliderVar.on_changed(self.update_plot)

        plt.show()

    def update_plot(self, val):

        if self.x_axis == 'z':
            s = self.sliderVar.val
            numpoints = np.shape(self.data_set['z'])[0]
            new_function = \
                np.reshape(self.yaxis_function(s,self.data_set['z']),
                           numpoints)

        if self.x_axis == 's':
            z = self.sliderVar.val
            numpoints = np.shape(self.data_set['s'])[0]
            new_function = \
                np.reshape(self.yaxis_function(self.data_set['s'],z),
                           numpoints)

        self.this_plot.set_ydata(new_function)

        self.fig.canvas.draw_idle()