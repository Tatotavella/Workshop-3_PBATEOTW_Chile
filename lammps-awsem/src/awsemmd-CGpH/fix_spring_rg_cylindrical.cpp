/* ----------------------------------------------------------------------
   LAMMPS - Large-scale Atomic/Molecular Massively Parallel Simulator
   http://lammps.sandia.gov, Sandia National Laboratories
   Steve Plimpton, sjplimp@sandia.gov

   Copyright (2003) Sandia Corporation.  Under the terms of Contract
   DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government retains
   certain rights in this software.  This software is distributed under
   the GNU General Public License.

   See the README file in the top-level LAMMPS directory.
------------------------------------------------------------------------- */

/* ----------------------------------------------------------------------
   Contributing author: Naveen Michaud-Agrawal (Johns Hopkins U)
                        Paul Crozier (SNL)
------------------------------------------------------------------------- */

#include "math.h"
#include "stdlib.h"
#include "string.h"
#include "fix_spring_rg_cylindrical.h"
#include "atom.h"
#include "update.h"
#include "group.h"
#include "respa.h"
#include "domain.h"
#include "error.h"

using namespace LAMMPS_NS;
using namespace FixConst;

/* ---------------------------------------------------------------------- */

FixSpringRGCylindrical::FixSpringRGCylindrical(LAMMPS *lmp, int narg, char **arg) :
  Fix(lmp, narg, arg)
{
  if (narg != 5) error->all(FLERR,"Illegal fix spring/rg/cylindrical command");

  k = atof(arg[3]);
  rg0_flag = 0;
  if (strcmp(arg[4],"NULL") == 0) rg0_flag = 1;
  else rg0 = atof(arg[4]);
}

/* ---------------------------------------------------------------------- */

int FixSpringRGCylindrical::setmask()
{
  int mask = 0;
  mask |= POST_FORCE;
  mask |= POST_FORCE_RESPA;
  return mask;
}

/* ---------------------------------------------------------------------- */

void FixSpringRGCylindrical::init()
{
  masstotal = group->mass(igroup);

  // if rg0 was specified as NULL, compute current Rg
  // only occurs on 1st run

  if (rg0_flag) {
    double xcm[3];
    group->xcm(igroup,masstotal,xcm);
    rg0 = group->cylindricalgyration(igroup,masstotal,xcm);
    rg0_flag = 0;
  }

  if (strstr(update->integrate_style,"respa"))
    nlevels_respa = ((Respa *) update->integrate)->nlevels;
}

/* ---------------------------------------------------------------------- */

void FixSpringRGCylindrical::setup(int vflag)
{
  if (strstr(update->integrate_style,"verlet"))
    post_force(vflag);
  else {
    ((Respa *) update->integrate)->copy_flevel_f(nlevels_respa-1);
    post_force_respa(vflag,nlevels_respa-1,0);
    ((Respa *) update->integrate)->copy_f_flevel(nlevels_respa-1);
  }
}

/* ---------------------------------------------------------------------- */

void FixSpringRGCylindrical::post_force(int vflag)
{
  // compute current Rg and center-of-mass

  double xcm[3];
  group->xcm(igroup,masstotal,xcm);
  double rg = group->cylindricalgyration(igroup,masstotal,xcm);

  // apply restoring force to atoms in group
  // f = -k*(r-r0)*mass/masstotal

  double dx,dy,term1;

  double **f = atom->f;
  double **x = atom->x;
  int *mask = atom->mask;
  int *type = atom->type;
  tagint *image = atom->image;
  double *mass = atom->mass;
  int nlocal = atom->nlocal;

  double massfrac;
  double xprd = domain->xprd;
  double yprd = domain->yprd;

  int xbox,ybox;
  for (int i = 0; i < nlocal; i++)
    if (mask[i] & groupbit) {
      term1 = 2.0 * k * (1.0 - rg0/rg);
      xbox = (image[i] & IMGMASK) - IMGMAX;
      ybox = (image[i] >> IMGBITS & IMGMASK) - IMGMAX;
      dx = (x[i][0] + xbox*xprd) - xcm[0];
      dy = (x[i][1] + ybox*yprd) - xcm[1];
      massfrac = mass[type[i]]/masstotal;
      f[i][0] -= term1*dx*massfrac;
      f[i][1] -= term1*dy*massfrac;
    }
}

/* ---------------------------------------------------------------------- */

void FixSpringRGCylindrical::post_force_respa(int vflag, int ilevel, int iloop)
{
  if (ilevel == nlevels_respa-1) post_force(vflag);
}
