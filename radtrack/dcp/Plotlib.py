# Timur Shaftan
# Library -- plotting routines

from matplotlib.pyplot import figure, show, savefig, plot, title, xlabel, ylabel
from matplotlib.pylab import *
from Servicelib import column

def PlotColn(Xvector, Yvector,LineType,LineColor,MarkerType,TitleP,Xlab,Ylab):
    #plotting a single curve in coln using my own sdds-lib
    figure
    plot(Xvector,Yvector,LineType+LineColor+MarkerType)
    title(TitleP)
    xlabel(Xlab)
    ylabel(Ylab)
    grid()
    plt.show()
    return 

def PlotColnS(Xvector, Yvector,LineType,MarkerType,TitleP,Xlab,Ylab):
    # plotting multiple curves from coln  using my own sdds-lib
    figure
    for i in range(np.shape(Yvector)[1]):
        plot(Xvector,[float(s) for s in column(Yvector,i)],LineType+MarkerType)
    title(TitleP)
    xlabel(Xlab)
    ylabel(Ylab)
    grid()
    plt.show()
    return 

def PlotColnS1(Xvector, Yvector,LineType,MarkerType,TitleP,Xlab,Ylab):
    # plotting multiple curves from coln using formats from B. Soliday's sdds-lib
    figure
#    NumVecPlot=len(Yvector)
    NumVecPlot=np.shape(Yvector)[0]
#    print NumVecPlot
#    print np.shape(Yvector)
#    print len(Yvector[:,1])
    for i in xrange(0,NumVecPlot):
        try:
#            plot(Xvector, Yvector[i][0][:],LineType+MarkerType)
            if Ylab:
                if Ylab[i][1]:
                    Ylabel=Ylab[i][2]+", "+Ylab[i][1]
                else:
                    Ylabel=Ylab[i][2]
                plot(Xvector, Yvector[i,:], LineType+MarkerType,label=Ylabel)
                legend( loc='upper left', numpoints = 1 )
            else:
                plot(Xvector, Yvector[i][:], LineType+MarkerType)
        except ValueError:
            print "%d " %(i)               
    title(TitleP)
    xlabel(Xlab)
    grid()
    plt.show()
    return 
    
def PlotColnS2(Xvector, Yvector1, Yvector2,LineType,MarkerType,TitleP,Xlab,Ylab,dcp):
    # plotting multiple curves from coln using twinx()
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    NumVecPlot=np.shape(Yvector1)[0]
    for i in xrange(0,NumVecPlot):
        try:
            if Ylab:
                if Ylab[i][1]:
                    Ylabel=Ylab[i][2]+", "+Ylab[i][1]
                else:
                    Ylabel=Ylab[i][2]
                dcp.ax.plot(Xvector, Yvector1[i,:], LineType+MarkerType,label=Ylabel)
                legend( loc='upper left', numpoints = 1 )
            else:
                dcp.ax.plot(Xvector, Yvector1[i][:], LineType+MarkerType)
        except ValueError:
            print "%d " %(i)  
    ax2 = dcp.ax.twinx()
    NumVecPlot1=np.shape(Yvector2)[0]
    for i in xrange(0,NumVecPlot1):
        try:
            if Ylab:
                if Ylab[i][1]:
                    Ylabel=Ylab[i][2]+", "+Ylab[i][1]
                else:
                    Ylabel=Ylab[i][2]
                ax2.plot(Xvector, Yvector2[i,:], '-'+'rx',label=Ylabel)
                legend( loc='upper left', numpoints = 1 )
            else:
                ax2.plot(Xvector, Yvector2[i][:], LineType+MarkerType)
        except ValueError:
            print "%d " %(i) 
    print np.max(Yvector2)
#    plt.ylim([np.min(Yvector2), np.max(Yvector2)])
    dcp.ax.set_title(TitleP)
    dcp.ax.set_xlabel(Xlab)
#    ax.grid()
#    plt.show()
    dcp.ax.grid()
    dcp.draw()
    return 
