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

def FindingArrayMaxima(seq, deltI):
	pkdc('size:',np.shape(seq)[0])
	if seq:
		j=0
		maxV=[]
		maxI=[]
		maxIj=0
		for i in xrange(0, np.shape(seq)[0]-deltI-1):
			pkdc(i, seq[i])
			if seq[i+1]>seq[i]:
				maxVj=seq[i+1]
				maxIj=i+1
				pkdc(maxIj)
			if (maxIj>0) & (i>maxIj+deltI):
				j=j+1
				maxV.append(maxVj)
				maxI.append(maxIj)				
				maxIj=1000000
	else:
		print('Input array is empty')
	pkdc('Maximum # and Intensity of UR harmoncis: ',maxI,maxV)
	return (maxV, maxI)

def Path_Length(x,y):
	Path_Len=0
	for i in xrange(0, np.shape(x)[0]-1):
		Path_Len=Path_Len+ np.sqrt((y[i+1]-y[i])**2*1E-6 + (x[i+1]-x[i])**2) 
	return (Path_Len) 

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
	pkdc(I_radf)
	print('Spectral Amplitude, ph/s/mrad2',maxI)
	pkdc(I_radf.index(max(I_radf)))
	maxIn=maxelements(I_radf)
	(maxV, maxI)=FindingArrayMaxima(I_radf,5)
	print(maxI, maxV)
	f.close()

	##Reading SRW data TRAJECTORY
	IFileName="Trajectory.txt"
	f=open(str(d.join(IFileName)),"r")#,10000)
	z_dist=[]
	x_traj=[]
	for line in f.readlines():
	    words = line.split()
	    z_dist.append(words[0])
	    x_traj.append(words[1])
	x_trajectory=map(float, x_traj)
	z_distance=map(float, z_dist)
	minX=min(x_trajectory)
	maxX=max(x_trajectory)
	minZ=min(z_distance)
	maxZ=max(z_distance)
	print ('Length of ID, m', maxZ-minZ)
	print('Oscillation Amplitude, mm',(maxX-minX)/2)
	L_trajectory=Path_Length(z_distance, x_trajectory)
	print('Length of Trajectory, m', L_trajectory)
	f.close()

	##Plotting
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
	plot(z_dist,x_trajectory,'.b',linestyle="-")
	(maxVt, maxIt)=FindingArrayMaxima(map(float,x_trajectory),20)
	pkdc(maxIt, maxVt)
	j=0
	for i in maxIt:
		plt.scatter(z_dist[i], maxVt[j], color='red')
		j=j+1
	grid()
	plt.show()

test_1()