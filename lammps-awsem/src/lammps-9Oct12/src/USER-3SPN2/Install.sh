# Install/unInstall package files in LAMMPS

if (test $1 = 1) then

  # New files that I have added
  cp angle_3spn2_stacking.cpp ..
  cp angle_3spn2_stacking.h ..
  cp dihedral_3spn2.cpp ..
  cp dihedral_3spn2.h ..  
  cp base_pair.h ..
  cp base_pair.cpp ..
  cp pair_3spn2.cpp ..
  cp pair_3spn2.h ..

elif (test $1 = 0) then

  rm -f ../angle_3spn2_stacking.cpp 
  rm -f ../angle_3spn2_stacking.h 
  rm -f ../dihedral_3spn2.cpp
  rm -f ../dihedral_3spn2.h 
  rm -f ../base_pair.cpp
  rm -f ../base_pair.h
  rm -f ../pair_3spn2.cpp
  rm -f ../pair_3spn2.h

fi
