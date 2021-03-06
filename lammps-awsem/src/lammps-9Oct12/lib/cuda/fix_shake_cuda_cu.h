/* ----------------------------------------------------------------------
   LAMMPS - Large-scale Atomic/Molecular Massively Parallel Simulator 

   Original Version:
   http://lammps.sandia.gov, Sandia National Laboratories
   Steve Plimpton, sjplimp@sandia.gov 

   See the README file in the top-level LAMMPS directory. 

   ----------------------------------------------------------------------- 

   USER-CUDA Package and associated modifications:
   https://sourceforge.net/projects/lammpscuda/ 

   Christian Trott, christian.trott@tu-ilmenau.de
   Lars Winterfeld, lars.winterfeld@tu-ilmenau.de
   Theoretical Physics II, University of Technology Ilmenau, Germany 

   See the README file in the USER-CUDA directory. 

   This software is distributed under the GNU General Public License.
------------------------------------------------------------------------- */
#include "cuda_shared.h"

extern "C" void Cuda_FixShakeCuda_Init(cuda_shared_data* sdata,X_FLOAT dtv, F_FLOAT dtfsq,
						void* shake_flag,void* shake_atom,void* shake_type, void* xshake,
						void* bond_distance,void* angle_distance,void* virial,
						int max_iter,X_FLOAT tolerance);
extern "C" void Cuda_FixShakeCuda_UnconstrainedUpdate(cuda_shared_data* sdata);
extern "C" void Cuda_FixShakeCuda_Shake(cuda_shared_data* sdata,int vflag,int vflag_atom,int* list,int nlist);
extern "C" int Cuda_FixShakeCuda_PackComm(cuda_shared_data* sdata,int n,int iswap,void* buf_send,int* pbc,int pbc_flag);
extern "C" int Cuda_FixShakeCuda_PackComm_Self(cuda_shared_data* sdata,int n,int iswap,int first,int* pbc,int pbc_flag);
extern "C" void Cuda_FixShakeCuda_UnpackComm(cuda_shared_data* sdata,int n,int first,void* buf_recv);

