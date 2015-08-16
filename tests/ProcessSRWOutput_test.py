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

def maxelements(seq):
    ''' Return list of position(s) of largest element '''
    max_indices = []
    if seq:
        max_val = seq[0]
        for i,val in ((i,val) for i,val in enumerate(seq) if val >= max_val):
            if val == max_val:
                max_indices.append(i)
            else:
                max_val = val
                max_indices = [i]

    return max_indices

def FindingSpectralMaxima(seq, deltI):
	print('size:',np.shape(seq)[0])
	if seq:
		j=0
		maxV=[]
		maxI=[]
		maxIj=0
		for i in xrange(0, np.shape(seq)[0]-deltI-1):
#			print(i, seq[i])
			if seq[i+1]>seq[i]:
				maxVj=seq[i+1]
				maxIj=i+1
#				print(maxIj)
			if (maxIj>0) & (i>maxIj+deltI):
				j=j+1
				maxV.append(maxVj)
				maxI.append(maxIj)
#				print(j,maxI,maxV)
				maxIj=1000000
	else:
		print('Input array is empty')
	return (maxV, maxI)

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
	I_radf=map(float,I_rad)
	maxI=max(I_radf)
#	print (I_radf)
	print('Spectral Amplitude, ph/s/mrad2',maxI)
	print(I_radf.index(max(I_radf)))
	maxIn=maxelements(I_radf)
	print(maxIn)
	(maxV, maxI)=FindingSpectralMaxima(I_radf,5)
	print(maxI, maxV)
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
	j=0
	for i in maxI:
		plt.scatter(e_p[i], maxV[j], color='red')
		j=j+1
	#    title(TitleP)
	#    xlabel(Xlab)
	#    ylabel(Ylab)
	
	grid()
	plt.show()
	plot(z_dist,x_trajectory)
	(maxVt, maxIt)=FindingSpectralMaxima(map(float,x_trajectory),20)
	print(maxIt, maxVt)
	j=0
	for i in maxIt:
		plt.scatter(z_dist[i], maxVt[j], color='red')
		j=j+1
	grid()
	plt.show()

test_1()