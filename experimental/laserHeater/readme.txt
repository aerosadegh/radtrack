== Laser Heater readme ==

This directory contains a number of laser heater related tests that build up
 to the full laser heater with a laser mode, undulator, and ensemble of
 particles.

 The first test, paradoxically named 'laserHeater02', tracks an initially
 on-axis particle with zero transverse momentum through an undulator field
 without the laser field.

 The second test, more logically dubbed 'laserHeater03', adds a "physical"
 undulator with transverse focusing.

 Continuing the trend of asymptotically reasonable test names,
 'laserHeater04' simulates a single particle in the laser field for a 0,0
 Gaussian laser mode. Note that the Gaussian laser neglects magnetic motion
 as second order to the electric field quiver motion. This only works if the
  laser pulse is non-relativistic -- (E/omega m c) << 1.

 The final test, 'laserHeaterFull', combines an ideal undulator with a 0,0
 Gaussian laser mode and an ensemble of particles. This test demonstrates
 that the laser heater simulation can duplicate the particle distribution
 predicted by Z. Huang et al.


 For questions, contact Stephen Webb (swebb@radiasoft.net) or David
 Bruhwiler (bruhwiler@radiasoft.net)