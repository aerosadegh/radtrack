# -*- coding: utf-8 -*-
"""
Created on Fri Nov 08 22:09:04 2013

@author: Steven Wu
"""
import os
import os.path
import subprocess
print '==============================================================='
print '========     navigate to where                ================'
print '=========    ElegantExampleProgram is located ============='
# navigate to this directory

os.chdir( os.path.dirname(__file__) + '/betaMatching' )

#############################################
# Possible way to define where to go on all computers
# calling os.getcwd(ARG) navigates to
# the  Current Working Directory in in my Spyder IDE
#-------------------------------------------
#print 'pathlocation= ', dfdf
#print type( dfdf)
#dfdf
#print 'newpathlocation= ', dfdf.replace( '\\','/')
#os.getcwd( dfdf )
####################################################

#Do something with the config file. store to LSD?

########################################################
# --- run Elegant Simulation with specified .ele file
simulationPackage = 'Elegant'
configFile        = 'two.lte'
runFile           = 'two.ele'
runSimulation     = [ simulationPackage, runFile ]

print '********************************************************'
print '========================================================'
print '======    Calling Elegant from Python Environment ======'
print '======    running file ' + runFile
print '========================================================'

print 'BELOW IS OUTPUT FROM RUNNING ELEGANT SIMULATION:' + '\n'
subprocess.call( runSimulation )

print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
print '----- Elegant Simulation Finished --------------'

########################################################
########   ELEGANT SIMULATION FINISHED #################
########################################################

print '================================================'
print '======= Start Post Processing Results =========='
print '================================================'

#Define which result file to plot (*.twi)
#plotFile          = 'one.twi'
plotFile          = 'two.twi'

# Twiss Parameters: 6D phase space
parameters = ['nux', 'nuy', 'alphac']
columns    = [ 's',     'ElementName', 'ElementType',
               'betax', 'bety',        'psix',
               'psiy',  'etax',        'etay'    ]

#CHOOSE which axes to acquire data for (refer to columns (above)):
i = 0; j = 3
print 'Specified Columns to Plot:',
print '\t', columns[i],',', columns[j]
print '*****  Axis selected via:     columns[i], columns[j] *****',  '\n'

axesPlotStr = ','.join( [ columns[i], columns[j] ] )
#if more than 1 pair for plotting, display new axis

###############################################################
####  Use SDDSplot to plot Elegant Simulation Results   #########
###############################################################
sddsCall    = 'sddsplot'
axesToPlot  = ['-col=', axesPlotStr]
sddsPlotter = [sddsCall, plotFile, axesToPlot]
print 'CMD to plot using SDDS:'
print sddsPlotter, '\n'
subprocess.call( sddsPlotter  )

print '############################################'
print '#####   Used SDDS to plot results      #####'
print '############################################'


#########################################################################
####  Use SDDSprintout to acquire Elegant Simulation Results   #########
####  into Python environment for plotting            ###################
#########################################################################


#POPEN: acquire data into Python from SDDS
sddsCall     = 'sddsprintout'
xAxisInfo = ['-column=', columns[i] ]
yAxisInfo = ['-column=', columns[j] ]
zAxisInfo = ['-column=', columns[2] ]
#zAxisInfo is for hardcoding (explicitly define which columns to display)

sddsAcquire1 = [sddsCall, plotFile, xAxisInfo]
sddsAcquire2 = [sddsCall, plotFile, yAxisInfo]
sddsAcquire3 = [sddsCall, plotFile, zAxisInfo]
#sddsAcquire3 = "sddsprintout two.twi -columns=ElementName -columns='(betax,betay)'"
print 'CMD to acquire data from SDDS:'
print sddsAcquire1
####### sddsAcquire0 == an APS example which queries all information?
print '#############################################################'
print '#########  Acquiring data into Python environment   #########'
print '#########  from *.twi file.                         #########'
print '#############################################################'

cmd1 = subprocess.Popen( sddsAcquire1, stderr=subprocess.STDOUT, stdout=subprocess.PIPE )
cmd2 = subprocess.Popen( sddsAcquire2, stderr=subprocess.STDOUT, stdout=subprocess.PIPE )
cmd3 = subprocess.Popen( sddsAcquire3, stderr=subprocess.STDOUT, stdout=subprocess.PIPE )
#print 'cmd1len', len(cmd1),'\n', 'cmd2len', len(cmd2),'\n','cmd3len', len(cmd3),'\n',
axis1=[]; axis2=[]; axis3 = []
#*.strip() removes irrelevant whitespace and spacing (e.g. '\r\n')
for line in cmd1.stdout.readlines():
    axis1.append( line.strip() )
for line in cmd2.stdout.readlines():
    axis2.append( line.strip() )
for line in cmd3.stdout.readlines():
    axis3.append( line.strip() )

    #CANT GET LIST COMPREHENSION TO WORK?????????
#a1 = [ line.strip() for line in cmd1.stdout.readlines() ]
#print 'a1:', '\n', a1

print '=========Data is acquired into Python environment========'
print 'axis1:','\n',axis1, '\n'
print 'axis3:', '\n', '\n'.join(axis3)
print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
xLabel = axis1[2]
yLabel = axis2[2]
xUnits = axis1[3]
yUnits = axis2[3]
print xLabel, yLabel
#print axis1[5:]
x = [float( x ) for x in axis1[ 5: ] ]
y = [float( y ) for y in axis2[ 5: ] ]
#figure()
#plot( x,y )
#xlabel( xLabel + '(' + xUnits + ')' )
#ylabel( yLabel + '(' + yUnits + ')' )
#plt.plot(x,y)
#plt.show()
