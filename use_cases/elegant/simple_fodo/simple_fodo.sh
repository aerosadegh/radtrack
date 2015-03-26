#! /bin/bash

elegant *.ele


sddsplot -unsup=y -col=s,betax -graphic=line,type=0 *.twi -col=s,betay -graphic=line,type=1 *.twi -col=s,Profile -overlay=xmode=norm,yfact=0.1 -graphic=line,type=2 *.mag   &

#sddsplot *.bun -col=x,y -graphic=dot&
#sddsplot *.out -col=x,y -graphic=dot&


sddshist2d *.bun xybun.hist -col=x,y -xpar=81 -ypar=81 -smooth
sddscontour xybun.hist -shade -inter=8,8

sddshist2d *.out xyout.hist -col=x,y -xpar=81 -ypar=81 -smooth
sddscontour xyout.hist -shade -inter=8,8


