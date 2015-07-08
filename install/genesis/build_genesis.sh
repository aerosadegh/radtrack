#!/usr/bin/bash

# --- get the GENESIS 2.0 source code (build serial)
curl http://genesis.web.psi.ch/download/source/genesis_source_2.0_120629.tar.gz > genesis_source_2.0_120629.tar.gz
gunzip -c genesis_source_2.0_120629.tar.gz | tar -xv
mv Genesis_Current genesis
mkdir genesis/tar
mv genesis_source_2.0_120629.tar.gz genesis/tar
cd genesis
# The following line is required when compiling with
# gfortran version 4.9.2 but not with version 4.4.7
sed -i -- 's/-Wall/-Wall -freal-8-real-4/g' Makefile
make
cd ..

# --- build the GENESIS 2.0 source code with MPI
cp -r genesis genesis_mpi
cd genesis_mpi
cp mpi.f.multi mpi.f
rm -f mpif.h
rm -f genesis
# monkey patch the Makefile
sed -i -- 's/gfortran/mpif77/g' Makefile
make
mv genesis genesis_mpi
cd ..

# --- get the example input files
mkdir examples
cd examples
mkdir pegasus visa ttf lcls tesla
cd pegasus
curl http://genesis.web.psi.ch/download/inputfiles/pegasus.tar > pegasus.tar
tar -xvf pegasus.tar
cd ../visa
curl http://genesis.web.psi.ch/download/inputfiles/visa.tar > visa.tar
tar -xvf visa.tar
cd ../ttf
curl http://genesis.web.psi.ch/download/inputfiles/ttf.tar > ttf.tar
tar -xvf ttf.tar
mv "ttf Folder"/ttf* .
rm -fr "ttf Folder"
cd ../lcls
curl http://genesis.web.psi.ch/download/inputfiles/lcls.tar > lcls.tar
tar -xvf lcls.tar
cd ../tesla
curl http://genesis.web.psi.ch/download/inputfiles/tesla.tar > tesla.tar
tar -xvf tesla.tar
cd ..
cd ..
