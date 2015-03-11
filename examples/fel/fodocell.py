__author__ = 'swebb'

from radtrack.fel.fodocell import fodocell

driftlength = 0.0227*27
focallength = driftlength/0.26

print 'drift length=', driftlength
print 'focal length=', focallength
print 'B =', 0.614/(focallength*5*0.0227*0.299)

myfodocell = fodocell(driftlength, focallength)
myfodocell.get_twiss_parameters()
avgbeta = myfodocell.compute_average_beta()
print avgbeta
phi = myfodocell.compute_phase_advance()
print phi
#myfodocell.plot_beta_function()
