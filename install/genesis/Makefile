#
# GENESIS makefile
#
#
SOURCE=  main.f check.f diagno.f esource.f field.f incoherent.f \
 math.f partsim.f pushp.f loadbeam.f loadrad.f magfield.f \
 tdepend.f track.f string.f rpos.f scan.f source.f stepz.f \
 timerec.f initrun.f  input.f output.f mpi.f sdds.f
# output.f  \
#
# LIB=  -lmdbmth -lSDDS1 -lmdblib -lz 
#
#OBJECTS =$(SOURCE:.f=.o)
#
COMPILER = gfortran
#COMPILER = mpif77
#
#  executable name
#
EXECUTABLE = genesis
#executable = genesis_mpi 
#

LIB_DIR = $(HOME)/epics/extensions/lib/linux-x86_64
SDDS_FORTRAN_WRAPPER = $(HOME)/epics/extensions/src/SDDS/fortran/O.linux-x86_64/fortran_wrapper.o
LDFLAGS=$(SDDS_FORTRAN_WRAPPER) -L$(LIB_DIR) -lmdbmth -lSDDS1 -lmdblib -lz -lc -llzma
CFLAGS=-Wl,--build-id -O2 -ffixed-line-length-132 -Wall -fno-second-underscore -Wno-globals -Wno-unused


genesis: $(SOURCE)
	$(COMPILER) -g -w -O -Wall $(CFLAGS) -o $(EXECUTABLE) $(SOURCE) $(LDFLAGS)
	@echo ' ******* end of linking ****** '

clean:
	rm -f *~
	rm -f *.o *.obj genesis

install:
	cp ./$(EXECUTABLE) ~/bin/

single:
	cp mpi.f.single mpi.f
	cp mpif.h.single mpif.h

multi:
	cp mpi.f.multi mpi.f
	rm mpif.h










