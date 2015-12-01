# Timur Shaftan
# Library -- plotting routines

from matplotlib.pyplot import figure
import numpy as np

def PlotColnS1(Xvector, Yvector,LineType,MarkerType,TitleP,Xlab,Ylab,dcp):
    # plotting multiple curves from coln using formats from B. Soliday's sdds-lib
    figure
    NumVecPlot=len(Yvector)
    for i in xrange(0,NumVecPlot):
        try:
            if np.shape(Ylab)[0] > 2:
                if Ylab[i][1]:
                    Ylabel=Ylab[i][2] + ", " + Ylab[i][1]
                else:
                    Ylabel=Ylab[i][2]
                dcp.ax.plot(Xvector, Yvector[i,:], LineType + MarkerType,label=Ylabel)
                legend( loc='upper left', numpoints = 1 )
            else:
                dcp.ax.plot(Xvector, Yvector[i][:], LineType + MarkerType)
        except ValueError:
            print "%d " %(i)               
    dcp.ax.set_title(TitleP)
    dcp.ax.set_xlabel(Xlab)
    dcp.ax.set_ylabel(Ylab[0])
    dcp.draw()
