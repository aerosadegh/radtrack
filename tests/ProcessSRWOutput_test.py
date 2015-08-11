# -*- coding: utf-8 -*-
#C:\d from old\RadiaBeam\RadSoft\radtrack\tests>py.test ProcessSRWOutput_test.py
u"""PyTest for :mod:`radiasoft.AnalyticCalc`
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

import os
import numpy as np
from matplotlib.pylab import figure, plot, grid,plt
import pytest

from pykern.pkdebug import pkdc, pkdp
from pykern import pkunit
from pykern import pkyaml

from radtrack.srw import AnalyticCalc

def str2num(s):
    return ("." in s and [float(s)] or [int(s)])[0]

def test_1():
	d = pkunit.data_dir()
	## Testing actual SRW calculations 
	##Reading SRW data SPECTRUM
	IFileName="Spectrum.txt"
	f=open(str(d.join(IFileName)),"r")#,1000)
	e_p=[]
	I_rad=[]
	for line in f.readlines():
	    words = line.split()
	    e_p.append(words[0])
	    I_rad.append(words[1])
	print (np.shape(e_p))
	f.close()

	##Reading SRW data TRAJECTORY
	IFileName="Trajectory.txt"
	f=open(str(d.join(IFileName)),"r")#,10000)
	z_dist=[]
	x_trajectory=[]
	for line in f.readlines():
	    words = line.split()
	    z_dist.append(words[0])
	    x_trajectory.append(words[1])
	minX=min(map(float, x_trajectory))
	maxX=max(map(float, x_trajectory))
#	print (np.shape(z_dist))
	print ('Length of ID, m', max((map(float, z_dist))))
	print('Oscillation Amplitude, mm',(maxX-minX)/2)
#	print (x_trajectory[1:10])
	f.close()

	#Plotting
	plot(e_p,I_rad)
	#    title(TitleP)
	#    xlabel(Xlab)
	#    ylabel(Ylab)
	grid()
	plt.show()
	plot(z_dist,x_trajectory)
	grid()
	plt.show()

test_1()