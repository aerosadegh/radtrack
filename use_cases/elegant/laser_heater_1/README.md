### Laser Heater use case #1

This use case is taken from the Elegant example subdirectory
   elegantExamples/lsrMdltr/example1/

The LSRMDLTR (stands for 'laser modulator') element is used with LCLS-like parameters.

### Command line syntax
elegant run.ele 
sddsplot -col=t,p run.out -graph=dot
sddshist2d run.out run.out.h2d -column=t,p -xparam=100 -yparam=100
sddscontour -shade run.out.h2d
