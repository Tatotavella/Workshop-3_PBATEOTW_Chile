#!/bin/bash
lammps_dir="$HOME/work/lammps-9Oct12/src"
#lammps_dir="$HOME/work/lammps-3Jun11/src"
project_dir="."

#lmp_name="lmp_serial_552_mod_frust_elec"
lmp_name="lmp_serial_552_long_input"
cp -v $project_dir/* $lammps_dir
pwd

cd  $lammps_dir
#make clean-all
#make yes-user-smd
#make yes-class2
make serial
cp -v $lammps_dir/lmp_serial $HOME/opt/bin/$lmp_name
pwd
