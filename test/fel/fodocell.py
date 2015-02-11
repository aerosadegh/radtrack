__author__ = 'swebb'

from RadTrack.fel.fodocell import fodocell

aspectratio = 1./1.5
Lfratio = 2.*(1-aspectratio)/(1+aspectratio)

driftlength  = 0.0227*20
focallength  = driftlength/Lfratio
quadlength   = 0.0227*5
quadstrength = 1/(focallength*quadlength)

print 'drift length=', driftlength
print 'focal length=', focallength
print 'B =', 0.614/(focallength*5*0.0227*0.299)

myfodocell = fodocell()
myfodocell.make_fodo_cell(driftlength, quadlength, quadstrength)
myfodocell.get_twiss_parameters()
avgbeta = myfodocell.compute_average_beta()
print u'<\u03B2> =', avgbeta
phi = myfodocell.compute_phase_advance()
print u'\u03A6 =', phi
#myfodocell.plot_beta_function()
